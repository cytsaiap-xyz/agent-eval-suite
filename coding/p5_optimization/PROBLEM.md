# Problem 5: Performance Optimization Challenge

## Difficulty: Hard
## Expected Time: 30-45 minutes
## Discrimination Target: Algorithm optimization, data structures, memory efficiency

## Task

Optimize the anagram grouping algorithm to handle 1 million words in under 1 second.

## The Slow Code

See `slow_anagrams.py` - an O(n²) algorithm that times out on large inputs.

## Requirements

1. **Correctness**: Produce same results as original
2. **Performance**: 1M words in < 1 second
3. **Memory**: Handle 10M words without crashing (streaming/batching)
4. **Unicode**: Handle accented characters (café, naïve)
5. **Case-insensitive**: "Listen" and "Silent" are anagrams

## Input Format

`words.txt` - one word per line

## Output Format

`anagram_groups.json`:
```json
{
  "groups": [
    ["listen", "silent", "enlist"],
    ["evil", "vile", "live"],
    ...
  ],
  "statistics": {
    "total_words": 1000000,
    "unique_groups": 45000,
    "largest_group_size": 12,
    "top_10_groups": [...]
  }
}
```

## Provided Files

- `slow_anagrams.py` - the O(n²) reference implementation
- `words_10k.txt` - 10,000 words for development
- `words_100k.txt` - 100,000 words for testing
- `words_1m.txt` - 1,000,000 words for final benchmark

## Evaluation

```bash
python evaluate_p5.py solution.py
```

## Scoring Breakdown

| Test | Points |
|------|--------|
| Correctness on 10K words | 15 |
| Correctness on 100K words | 15 |
| 1M words in < 5 seconds | 15 |
| 1M words in < 1 second | 15 |
| Handles Unicode correctly | 10 |
| Case-insensitive | 10 |
| Top 10 groups correct | 10 |
| Memory efficient (10M words) | 10 |
| **Total** | **100** |

## Hints

- Think about what uniquely identifies an anagram group
- Consider using a hash map with a clever key
- `sorted()` on a string gives a canonical form
- For memory efficiency, consider generators
- `collections.defaultdict` is useful
- Unicode normalization: `unicodedata.normalize('NFD', s)`

## Expected Algorithm Complexity

- Time: O(n * k log k) where k is average word length
- Space: O(n) for storing groups
