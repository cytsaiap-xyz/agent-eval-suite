"""
Event Scheduler Module

A complex scheduling system with multiple features that need comprehensive testing.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from enum import Enum
from typing import List, Optional, Dict, Set, Tuple
import heapq
from zoneinfo import ZoneInfo


class RecurrenceType(Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class EventPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Event:
    """Represents a scheduled event."""
    id: str
    title: str
    start: datetime
    end: datetime
    timezone: str = "UTC"
    priority: EventPriority = EventPriority.MEDIUM
    recurrence: RecurrenceType = RecurrenceType.NONE
    recurrence_end: Optional[date] = None
    snoozed_until: Optional[datetime] = None
    dismissed: bool = False
    tags: Set[str] = field(default_factory=set)

    def __post_init__(self):
        if self.end <= self.start:
            raise ValueError("Event end must be after start")
        if self.recurrence != RecurrenceType.NONE and self.recurrence_end is None:
            # Default recurrence end to 1 year from start
            self.recurrence_end = (self.start + timedelta(days=365)).date()

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    def is_active(self, at_time: datetime) -> bool:
        """Check if event is active at given time."""
        if self.dismissed:
            return False
        if self.snoozed_until and at_time < self.snoozed_until:
            return False
        return self.start <= at_time < self.end

    def overlaps(self, other: 'Event') -> bool:
        """Check if this event overlaps with another."""
        return (self.start < other.end and self.end > other.start)

    def get_local_start(self) -> datetime:
        """Get start time in event's timezone."""
        tz = ZoneInfo(self.timezone)
        return self.start.astimezone(tz)

    def get_local_end(self) -> datetime:
        """Get end time in event's timezone."""
        tz = ZoneInfo(self.timezone)
        return self.end.astimezone(tz)


class Scheduler:
    """Event scheduler with conflict detection and recurrence."""

    def __init__(self, default_timezone: str = "UTC"):
        self.default_timezone = default_timezone
        self._events: Dict[str, Event] = {}
        self._priority_queue: List[Tuple[datetime, str]] = []
        self._conflicts: Dict[str, Set[str]] = {}

    def add_event(self, event: Event) -> bool:
        """Add an event to the scheduler."""
        if event.id in self._events:
            raise ValueError(f"Event with id {event.id} already exists")

        self._events[event.id] = event
        heapq.heappush(self._priority_queue, (event.start, event.id))
        self._update_conflicts(event)
        return True

    def remove_event(self, event_id: str) -> bool:
        """Remove an event from the scheduler."""
        if event_id not in self._events:
            return False

        del self._events[event_id]
        self._conflicts.pop(event_id, None)

        # Remove from other events' conflict sets
        for conflicts in self._conflicts.values():
            conflicts.discard(event_id)

        return True

    def get_event(self, event_id: str) -> Optional[Event]:
        """Get an event by ID."""
        return self._events.get(event_id)

    def get_events_in_range(self, start: datetime, end: datetime) -> List[Event]:
        """Get all events within a time range."""
        result = []
        for event in self._events.values():
            if event.start < end and event.end > start:
                if not event.dismissed:
                    result.append(event)
        return sorted(result, key=lambda e: e.start)

    def get_events_on_date(self, target_date: date, timezone: str = None) -> List[Event]:
        """Get all events on a specific date."""
        tz = ZoneInfo(timezone or self.default_timezone)

        day_start = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=tz)
        day_end = day_start + timedelta(days=1)

        return self.get_events_in_range(day_start, day_end)

    def _update_conflicts(self, event: Event):
        """Update conflict tracking for an event."""
        conflicts = set()
        for other_id, other in self._events.items():
            if other_id != event.id and event.overlaps(other):
                conflicts.add(other_id)
                if other_id not in self._conflicts:
                    self._conflicts[other_id] = set()
                self._conflicts[other_id].add(event.id)

        if conflicts:
            self._conflicts[event.id] = conflicts

    def get_conflicts(self, event_id: str) -> Set[str]:
        """Get IDs of events that conflict with given event."""
        return self._conflicts.get(event_id, set())

    def has_conflicts(self, event_id: str) -> bool:
        """Check if an event has any conflicts."""
        return event_id in self._conflicts and len(self._conflicts[event_id]) > 0

    def snooze_event(self, event_id: str, duration: timedelta) -> bool:
        """Snooze an event for a duration."""
        event = self._events.get(event_id)
        if not event:
            return False

        event.snoozed_until = datetime.now(ZoneInfo("UTC")) + duration
        return True

    def dismiss_event(self, event_id: str) -> bool:
        """Dismiss an event."""
        event = self._events.get(event_id)
        if not event:
            return False

        event.dismissed = True
        return True

    def get_next_occurrence(self, event: Event, after: datetime) -> Optional[datetime]:
        """Get next occurrence of a recurring event."""
        if event.recurrence == RecurrenceType.NONE:
            return None

        current = event.start
        while current <= after:
            current = self._advance_recurrence(current, event.recurrence)

            if event.recurrence_end and current.date() > event.recurrence_end:
                return None

        return current

    def _advance_recurrence(self, dt: datetime, recurrence: RecurrenceType) -> datetime:
        """Advance datetime by recurrence interval."""
        if recurrence == RecurrenceType.DAILY:
            return dt + timedelta(days=1)
        elif recurrence == RecurrenceType.WEEKLY:
            return dt + timedelta(weeks=1)
        elif recurrence == RecurrenceType.MONTHLY:
            # Handle month advancement properly
            month = dt.month + 1
            year = dt.year
            if month > 12:
                month = 1
                year += 1

            # Handle day overflow (e.g., Jan 31 -> Feb 28)
            day = min(dt.day, self._days_in_month(year, month))
            return dt.replace(year=year, month=month, day=day)
        elif recurrence == RecurrenceType.YEARLY:
            # Handle leap year (Feb 29 -> Feb 28 in non-leap year)
            year = dt.year + 1
            day = dt.day
            if dt.month == 2 and dt.day == 29 and not self._is_leap_year(year):
                day = 28
            return dt.replace(year=year, day=day)
        else:
            return dt

    def _days_in_month(self, year: int, month: int) -> int:
        """Get number of days in a month."""
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif month in (4, 6, 9, 11):
            return 30
        elif month == 2:
            return 29 if self._is_leap_year(year) else 28
        else:
            raise ValueError(f"Invalid month: {month}")

    def _is_leap_year(self, year: int) -> bool:
        """Check if a year is a leap year."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def merge_overlapping(self, event_ids: List[str]) -> Optional[Event]:
        """Merge multiple overlapping events into one."""
        events = [self._events.get(eid) for eid in event_ids]
        events = [e for e in events if e is not None]

        if len(events) < 2:
            return None

        # Verify all events actually overlap
        for i, e1 in enumerate(events):
            for e2 in events[i+1:]:
                if not e1.overlaps(e2):
                    raise ValueError("Cannot merge non-overlapping events")

        # Create merged event
        min_start = min(e.start for e in events)
        max_end = max(e.end for e in events)
        max_priority = max(e.priority.value for e in events)
        all_tags = set()
        for e in events:
            all_tags.update(e.tags)

        merged = Event(
            id=f"merged_{events[0].id}",
            title=f"Merged: {', '.join(e.title for e in events)}",
            start=min_start,
            end=max_end,
            priority=EventPriority(max_priority),
            tags=all_tags
        )

        # Remove old events
        for event_id in event_ids:
            self.remove_event(event_id)

        # Add merged event
        self.add_event(merged)

        return merged

    def get_free_slots(self, start: datetime, end: datetime,
                       min_duration: timedelta = timedelta(minutes=30)) -> List[Tuple[datetime, datetime]]:
        """Find free time slots in a range."""
        events = self.get_events_in_range(start, end)

        if not events:
            if end - start >= min_duration:
                return [(start, end)]
            return []

        # Sort events by start time
        events.sort(key=lambda e: e.start)

        slots = []

        # Check slot before first event
        if events[0].start > start:
            slot_duration = events[0].start - start
            if slot_duration >= min_duration:
                slots.append((start, events[0].start))

        # Check slots between events
        for i in range(len(events) - 1):
            slot_start = events[i].end
            slot_end = events[i + 1].start
            if slot_end > slot_start:
                slot_duration = slot_end - slot_start
                if slot_duration >= min_duration:
                    slots.append((slot_start, slot_end))

        # Check slot after last event
        if events[-1].end < end:
            slot_duration = end - events[-1].end
            if slot_duration >= min_duration:
                slots.append((events[-1].end, end))

        return slots

    def get_upcoming(self, count: int = 10, include_snoozed: bool = False) -> List[Event]:
        """Get upcoming events."""
        now = datetime.now(ZoneInfo("UTC"))
        upcoming = []

        for event in self._events.values():
            if event.dismissed:
                continue
            if not include_snoozed and event.snoozed_until and event.snoozed_until > now:
                continue
            if event.end > now:
                upcoming.append(event)

        upcoming.sort(key=lambda e: e.start)
        return upcoming[:count]

    def get_by_priority(self, priority: EventPriority) -> List[Event]:
        """Get events by priority level."""
        return [e for e in self._events.values()
                if e.priority == priority and not e.dismissed]

    def get_by_tag(self, tag: str) -> List[Event]:
        """Get events with a specific tag."""
        return [e for e in self._events.values()
                if tag in e.tags and not e.dismissed]

    def clear_dismissed(self) -> int:
        """Remove all dismissed events."""
        dismissed_ids = [eid for eid, e in self._events.items() if e.dismissed]
        for eid in dismissed_ids:
            self.remove_event(eid)
        return len(dismissed_ids)

    def export_to_dict(self) -> Dict:
        """Export scheduler state to dictionary."""
        return {
            "default_timezone": self.default_timezone,
            "events": [
                {
                    "id": e.id,
                    "title": e.title,
                    "start": e.start.isoformat(),
                    "end": e.end.isoformat(),
                    "timezone": e.timezone,
                    "priority": e.priority.value,
                    "recurrence": e.recurrence.value,
                    "tags": list(e.tags),
                    "dismissed": e.dismissed,
                }
                for e in self._events.values()
            ]
        }
