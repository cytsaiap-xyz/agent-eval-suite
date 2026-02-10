# Task: Optimize Anagram Grouping Algorithm

You are given `slow_anagrams.py` - an O(n²) algorithm that groups anagrams. Optimize it to handle 1 million words in under 1 second.

## Your Task

Create `solution.py` with an optimized `find_anagram_groups()` function.

## The Problem

The current implementation compares every pair of words, resulting in O(n²) complexity. It works fine for small inputs but times out on large datasets.

## Requirements

### Performance Targets
- 10,000 words: < 1 second
- 100,000 words: < 2 seconds
- 1,000,000 words: < 1 second (yes, faster due to better algorithm)

### Correctness
- Case-insensitive: "Listen" and "SILENT" are anagrams
- Handle Unicode: "café" should work
- Preserve original case in output
- Same results as the slow version

### Function Signature

```python
def find_anagram_groups(words: list[str]) -> list[list[str]]:
    """
    Group words that are anagrams of each other.

    Args:
        words: List of words to group

    Returns:
        List of groups, where each group is a list of anagrams
    """
    ...
```

### Optional: Statistics Function

```python
def get_statistics(groups: list[list[str]]) -> dict:
    """
    Return statistics about the anagram groups.

    Returns:
        {
            "total_words": int,
            "unique_groups": int,
            "largest_group_size": int,
            "top_10_groups": list[list[str]]
        }
    """
    ...
```

## Test Files

- `words_10k.txt` - 10,000 words for development
- `words_100k.txt` - 100,000 words for testing
- `words_1m.txt` - 1,000,000 words for benchmarking

## Usage

```bash
python solution.py words_1m.txt
```

## Algorithm Hint

Think about what uniquely identifies an anagram group. If two words are anagrams, what property do they share?

Consider:
- What's the time complexity of sorting a string?
- How can you use a hash map to group things efficiently?
- `collections.defaultdict` might be useful

## Expected Complexity

- Time: O(n × k log k) where k is average word length
- Space: O(n) for storing groups

## Example

```python
words = ["listen", "silent", "enlist", "hello", "world"]
groups = find_anagram_groups(words)
# Result: [["listen", "silent", "enlist"], ["hello"], ["world"]]
```
