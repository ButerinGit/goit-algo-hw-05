# -*- coding: utf-8 -*-
"""
Запуск бенчмарків для порівняння алгоритмів пошуку підрядка.
Приклади:
python benchmark.py --files data/article1.txt data/article2.txt --repeat 7 --number 1000
python benchmark.py --files data/article1.txt data/article2.txt --exist "алгоритмів" --miss "фантастичне_слово_якого_нема"
"""
import argparse
import timeit
from typing import Dict, List, Tuple
from algorithms import ALGORITHMS
import json
import os
import random

def pick_patterns(text: str, exist_len: int = 12) -> Tuple[str, str]:
    # Беремо існуючий підрядок: випадкове вікно довжини exist_len із середини тексту
    if len(text) < exist_len:
        exist = text
    else:
        start = max(0, len(text) // 3)
        end = max(start + exist_len, min(len(text) - exist_len, 2 * len(text) // 3))
        pos = random.randint(start, end)
        exist = text[pos:pos + exist_len]
    # Вигаданий: міняємо один символ або додаємо символ, щоб гарантувати відсутність
    if exist:
        miss = exist[:-1] + chr((ord(exist[-1]) + 13) % 0x10FFFF)
    else:
        miss = "___not_in_text___"
    # Додаткова гарантія відсутності
    if exist and exist in text:
        while miss in text:
            miss += "#"
    return exist, miss

def bench_file(text: str, exist: str, miss: str, repeat: int, number: int) -> Dict:
    results = {}
    for name, fn in ALGORITHMS.items():
        # прогрів
        fn(text, exist); fn(text, miss)
        # вимірювання
        exist_timer = timeit.Timer(lambda: fn(text, exist))
        miss_timer = timeit.Timer(lambda: fn(text, miss))
        exist_times = exist_timer.repeat(repeat=repeat, number=number)
        miss_times = miss_timer.repeat(repeat=repeat, number=number)
        results[name] = {
            "exist_idx": fn(text, exist),
            "miss_idx": fn(text, miss),
            "exist_times": exist_times,
            "miss_times": miss_times,
            "exist_avg": sum(exist_times) / len(exist_times),
            "miss_avg": sum(miss_times) / len(miss_times),
        }
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True, help="Шляхи до текстових файлів")
    parser.add_argument("--exist", type=str, default=None, help="Підрядок, що існує в тексті")
    parser.add_argument("--miss", type=str, default=None, help="Підрядок, що відсутній у тексті")
    parser.add_argument("--repeat", type=int, default=7, help="Кількість повторів (timeit.repeat)")
    parser.add_argument("--number", type=int, default=100, help="Скільки запусків на один повтор")
    parser.add_argument("--out", type=str, default="results.json", help="Файл для збереження результатів")
    args = parser.parse_args()

    data = {"files": [], "meta": {"repeat": args.repeat, "number": args.number}}
    for path in args.files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        exist = args.exist
        miss = args.miss
        if exist is None or miss is None:
            exist, miss = pick_patterns(text)
        file_result = bench_file(text, exist, miss, args.repeat, args.number)
        fastest_exist = min(file_result.items(), key=lambda kv: kv[1]["exist_avg"])[0]
        fastest_miss = min(file_result.items(), key=lambda kv: kv[1]["miss_avg"])[0]
        data["files"].append({
            "path": path,
            "exist": exist,
            "miss": miss,
            "results": file_result,
            "fastest_exist": fastest_exist,
            "fastest_miss": fastest_miss,
        })
    # Глобальні висновки
    def best_overall(kind: str) -> str:
        # підрахунок перемог за файлами
        wins = {}
        for file in data["files"]:
            w = file[f"fastest_{kind}"]
            wins[w] = wins.get(w, 0) + 1
        return max(wins.items(), key=lambda kv: kv[1])[0]

    data["summary"] = {
        "best_exist_overall": best_overall("exist"),
        "best_miss_overall": best_overall("miss"),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Збережено результати в {args.out}")

if __name__ == "__main__":
    main()