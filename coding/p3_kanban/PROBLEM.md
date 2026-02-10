# Problem 3: Full-Stack Kanban Board

## Difficulty: Hard
## Expected Time: 45-60 minutes
## Discrimination Target: DOM manipulation, state management, event handling

## Task

Create a single-file Kanban board application with advanced features.

## Requirements

### File Structure
- **Single HTML file** - all HTML, CSS, and JavaScript in one file
- **No external dependencies** - no libraries, no CDN links
- Must work offline when opened directly in browser

### Core Features (40 points)

1. **Three Columns** (5 pts)
   - Todo, In Progress, Done
   - Clear visual separation
   - Column headers

2. **Add Cards** (10 pts)
   - Input field + Add button in each column
   - Cards show title
   - Enter key should also add card

3. **Delete Cards** (5 pts)
   - Delete button on each card
   - Confirmation not required

4. **Drag and Drop** (20 pts)
   - Drag cards between columns
   - Visual feedback during drag (opacity, placeholder)
   - Drop zones highlight on dragover
   - **Pure JavaScript - no libraries**

### Advanced Features (40 points)

5. **Inline Editing** (10 pts)
   - Double-click card to edit title
   - Press Enter to save, Escape to cancel
   - Click outside to save

6. **Undo/Redo** (15 pts)
   - Ctrl+Z to undo (Cmd+Z on Mac)
   - Ctrl+Y or Ctrl+Shift+Z to redo
   - Supports: add, delete, move, edit operations
   - At least 20 operations in history

7. **LocalStorage Persistence** (10 pts)
   - Save state on every change
   - Restore on page load
   - Handle corrupted data gracefully

8. **Keyboard Navigation** (5 pts)
   - Tab through cards
   - Enter to edit focused card
   - Arrow keys to move focus between cards

### Polish (20 points)

9. **CSS Animations** (10 pts)
   - Smooth transitions for card moves
   - Fade in for new cards
   - Visual feedback for interactions

10. **Responsive Design** (5 pts)
    - Works on different screen sizes
    - Columns stack on mobile

11. **Accessibility** (5 pts)
    - Proper ARIA labels
    - Keyboard accessible
    - Focus indicators

## Test Cases

Open `kanban.html` in browser and verify:

### Manual Test Checklist
```
[ ] Page loads without errors in console
[ ] Can add cards to each column
[ ] Can drag cards between columns
[ ] Can delete cards
[ ] Double-click to edit works
[ ] Undo (Ctrl+Z) reverses last action
[ ] Redo (Ctrl+Y) works after undo
[ ] Refresh page - cards persist
[ ] Clear localStorage - page handles empty state
[ ] Tab navigates between cards
[ ] Works without internet connection
```

### Automated Tests
```bash
python evaluate_p3.py kanban.html
```

The evaluator uses Playwright/Selenium to test functionality.

## Evaluation Criteria

| Feature | Points |
|---------|--------|
| Three columns layout | 5 |
| Add cards functionality | 10 |
| Delete cards | 5 |
| Drag and drop (working) | 20 |
| Inline editing | 10 |
| Undo/Redo stack | 15 |
| LocalStorage persistence | 10 |
| Keyboard navigation | 5 |
| CSS animations | 10 |
| Responsive design | 5 |
| Accessibility | 5 |
| **Total** | **100** |

## Hints

- Use `draggable="true"` attribute
- Events: `dragstart`, `dragover`, `drop`, `dragend`
- Use `e.dataTransfer.setData()` to pass card ID
- For undo/redo, store action objects: `{type, data, inverse}`
- CSS: `transition: transform 0.2s ease`
