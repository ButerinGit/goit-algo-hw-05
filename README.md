# goit-algo-hw-05

## Структура проєкту

```
goit-algo-hw-05/
├─ algorithms.py       # Реалізація алгоритмів
├─ benchmark.py        # Запуск бенчмарків
├─ data/
│  ├─ art.txt          # Вхідний текст 1
│  └─ art2.txt         # Вхідний текст 2
├─ report_template.md  # Шаблон звіту
└─ README.md           # Документація
```

## Встановлення

Склонуйте репозиторій:

```bash
git clone https://github.com/username/goit-algo-hw-05.git
cd goit-algo-hw-05
```

## Використання

Запустити порівняння алгоритмів на своїх файлах можна так:

```bash
python benchmark.py --files data/art.txt data/art2.txt --repeat 7 --number 1000
```

Параметри:

* `--files` – список текстових файлів для аналізу
* `--exist` – підрядок, який гарантовано є в тексті (необов’язковий)
* `--miss` – підрядок, якого точно немає в тексті (необов’язковий)
* `--repeat` – кількість повторів для вимірювання (`timeit.repeat`)
* `--number` – кількість запусків за один повтор
* `--out` – шлях до JSON-файлу з результатами (за замовчуванням `results.json`)

## Приклад запуску

```bash
python benchmark.py --files data/art.txt data/art2.txt --repeat 5 --number 500
```

Результати збережуться у файлі:

```
results.json
```

## Формат результатів

У `results.json` зберігається середній час виконання для кожного алгоритму, індекс знайденого підрядка та підсумкові висновки.
Приклад:

```json
{
  "files": [
    {
      "path": "data/art.txt",
      "exist": "алгоритмів",
      "miss": "фантастичне_слово_якого_нема",
      "fastest_exist": "KMP",
      "fastest_miss": "Boyer-Moore"
    }
  ],
  "summary": {
    "best_exist_overall": "KMP",
    "best_miss_overall": "Boyer-Moore"
  }
}
```
