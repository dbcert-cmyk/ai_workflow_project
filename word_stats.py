import re


def get_word_stats(text):
    # Remove special characters/punctuation and split into words
    words = re.findall(r"\b\w+\b", text.lower())

    if not words:
        return {"word_count": 0, "longest_word": "", "vowel_start_count": 0}

    word_count = len(words)
    longest_word = max(words, key=len)
    vowel_start_count = sum(1 for word in words if word[0] in "aeiou")

    return {
        "word_count": word_count,
        "longest_word": longest_word,
        "vowel_start_count": vowel_start_count,
    }


if __name__ == "__main__":
    test_text = "Apple, banana! Orange, and a very long elephant."
    result = get_word_stats(test_text)
    print(result)
