#!/usr/bin/env python3
"""
Generate word files for anagram testing.
Creates realistic word distributions with known anagram groups.
"""

import random
import string
from pathlib import Path

# Base words that form anagram groups
ANAGRAM_GROUPS = [
    ["listen", "silent", "enlist", "tinsel", "inlets"],
    ["evil", "vile", "live", "veil"],
    ["earth", "heart", "hater", "rathe"],
    ["night", "thing"],
    ["stream", "master", "tamers"],
    ["rescue", "secure", "recuse"],
    ["danger", "gander", "garden", "ranged"],
    ["plates", "staple", "pleats", "petals", "palest"],
    ["course", "source", "cerous"],
    ["sorted", "stored", "strode"],
    ["alerts", "alters", "artels", "estral", "laster", "ratels", "salter", "slater", "staler", "stelar", "talers"],
    ["carets", "caster", "caters", "crates", "reacts", "recast", "traces"],
    ["united", "untied", "dunite"],
    ["tones", "stone", "notes", "onset", "seton"],
    ["spare", "spear", "reaps", "pears", "parse"],
    ["café", "face"],  # Unicode test
    ["naïve", "avine"],  # Unicode test
    ["résumé", "resume"],  # Unicode test (different forms)
]

# Common word patterns for generating more words
PATTERNS = [
    "tion", "ing", "ness", "ment", "able", "ible", "ful", "less",
    "pre", "un", "re", "dis", "over", "under", "out", "mis"
]


def generate_random_word(min_len=3, max_len=10):
    """Generate a random word-like string."""
    length = random.randint(min_len, max_len)

    # Mix of common letter frequencies
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"

    word = []
    use_vowel = random.random() < 0.3

    for i in range(length):
        if use_vowel:
            word.append(random.choice(vowels))
        else:
            word.append(random.choice(consonants))
        use_vowel = not use_vowel if random.random() < 0.6 else use_vowel

    return ''.join(word)


def generate_word_list(count: int, include_anagrams: bool = True) -> list:
    """Generate a list of words with embedded anagram groups."""
    words = []

    if include_anagrams:
        # Include known anagram groups multiple times
        repeat_count = max(1, count // 1000)
        for group in ANAGRAM_GROUPS:
            for _ in range(repeat_count):
                words.extend(group)

    # Fill rest with random words
    remaining = count - len(words)
    for _ in range(remaining):
        words.append(generate_random_word())

    random.shuffle(words)
    return words


def main():
    base_path = Path(__file__).parent

    print("Generating word files for anagram testing...")

    # 10K words
    print("Generating words_10k.txt...")
    words_10k = generate_word_list(10000)
    with open(base_path / "words_10k.txt", "w") as f:
        f.write("\n".join(words_10k))
    print(f"  Created {len(words_10k)} words")

    # 100K words
    print("Generating words_100k.txt...")
    words_100k = generate_word_list(100000)
    with open(base_path / "words_100k.txt", "w") as f:
        f.write("\n".join(words_100k))
    print(f"  Created {len(words_100k)} words")

    # 1M words
    print("Generating words_1m.txt...")
    words_1m = generate_word_list(1000000)
    with open(base_path / "words_1m.txt", "w") as f:
        f.write("\n".join(words_1m))
    print(f"  Created {len(words_1m)} words")

    print("\nDone! Files created:")
    for f in ["words_10k.txt", "words_100k.txt", "words_1m.txt"]:
        size = (base_path / f).stat().st_size
        print(f"  {f}: {size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
