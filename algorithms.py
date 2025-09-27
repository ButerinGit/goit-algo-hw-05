# -*- coding: utf-8 -*-
"""
Реалізації алгоритмів пошуку підрядка:
- Боєра–Мура (Boyer-Moore, варіант bad character + доброю суфіксною евристикою для простоти опускаємо, залишаємо bad character)
- Кнута–Морріса–Пратта (KMP)
- Рабіна–Карпа (Rabin–Karp, ролінг-хеш)
"""
from typing import List

def boyer_moore(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    # Підготовка таблиці останніх входжень символів (bad character rule)
    last = {}
    for i, c in enumerate(pattern):
        last[c] = i
    m, n = len(pattern), len(text)
    i = m - 1  # індекс у text
    j = m - 1  # індекс у pattern
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            i -= 1
            j -= 1
        else:
            lo = last.get(text[i], -1)
            i += m - min(j, lo + 1)
            j = m - 1
    return -1

def kmp(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    # Будуємо lps (longest proper prefix which is also suffix)
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def rabin_karp(text: str, pattern: str, base: int = 256, mod: int = 10**9 + 7) -> int:
    m, n = len(pattern), len(text)
    if m == 0:
        return 0
    if m > n:
        return -1
    # Попередньо обчислюємо base^(m-1) % mod
    h = pow(base, m - 1, mod)
    # Початкові хеші
    pat_hash = 0
    win_hash = 0
    for i in range(m):
        pat_hash = (pat_hash * base + ord(pattern[i])) % mod
        win_hash = (win_hash * base + ord(text[i])) % mod
    # Перевірка першого вікна
    if pat_hash == win_hash and text[:m] == pattern:
        return 0
    for i in range(m, n):
        # видаляємо лівий символ і додаємо новий правий
        win_hash = (win_hash - ord(text[i - m]) * h) % mod
        win_hash = (win_hash * base + ord(text[i])) % mod
        # звіряємо
        if win_hash == pat_hash:
            start = i - m + 1
            if text[start:start + m] == pattern:
                return start
    return -1

ALGORITHMS = {
    "Boyer-Moore": boyer_moore,
    "KMP": kmp,
    "Rabin-Karp": rabin_karp,
}