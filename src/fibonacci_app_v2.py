"""
Fibonacci Application v2.0 — Исправленная версия (src/fibonacci_app_v2.py)
========================================================================
Дисциплина: Тестирование программного обеспечения
Вариант 3: «Вычисление чисел Фибоначчи»
Студент: Баймуратов А.И., гр. БПИ-23-01
Преподаватель: к.х.н., доцент Махмутова Р.И.
УГНТУ, 2026

ВЕРСИЯ 2.0 (Дефекты устранены, Резолюция Fixed):
1. Валидация входных данных [0..40] на уровне ядра и UI.
2. Автоматическая очистка поля ввода при ошибке (Требование 14).
3. Полный академический заголовок окна.
4. Поддержка флага трассировки --trace для структурного тестирования.
"""

import argparse
import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, List

try:
    from src.fibonacci_core import (
        compute_fibonacci,
        format_sequence_str,
        get_dual_index_info,
        get_fibonacci_sequence,
    )
    from src.tracer import CFGTracer
except ImportError:
    from fibonacci_core import (  # type: ignore
        compute_fibonacci,
        format_sequence_str,
        get_dual_index_info,
        get_fibonacci_sequence,
    )
    from tracer import CFGTracer  # type: ignore

DEFAULT_DATA_FILE = "Fibonacci_file.txt"


def compute_fibonacci_v2(n: Any) -> int:
    """
    Вспомогательная функция вычисления Фибоначчи для версии 2.0.
    Использует эталонное ядро compute_fibonacci со строгой валидацией.
    """
    val, _ = compute_fibonacci(n, track_path=False)
    return val


def save_to_file_v2(n: int, val: int, seq: List[int], filepath: str = DEFAULT_DATA_FILE) -> str:
    """Сохранение отчета в файл (Требования 2-5, 11-13 Приложения В)."""
    seq_str = ", ".join(str(x) for x in seq)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = (
        f"Входной параметр n: {n}\n"
        f"Число Фибоначчи F(n): {val}\n"
        f"Последовательность: {seq_str}\n"
        f"Дата и время расчета: {timestamp}\n"
        f"Статус проверки: Валидировано (v2.0)\n"
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(filepath)


class FibonacciAppV2GUI:
    """Графический оконный интерфейс исправленной версии 2.0."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Вычисление чисел Фибоначчи — Вариант 3 (v2.0)")
        self.root.geometry("560x460")
        self.root.minsize(500, 400)

        self.last_n: int = 0
        self.last_val: int = 0
        self.last_seq: List[int] = []

        self._build_widgets()

    def _build_widgets(self) -> None:
        frame_input = ttk.LabelFrame(self.root, text=" Ввод исходных данных ", padding=10)
        frame_input.pack(fill="x", padx=15, pady=10)

        lbl_prompt = ttk.Label(
            frame_input,
            text="Введите порядковый номер n (целое число от 0 до 40):"
        )
        lbl_prompt.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.entry_n = ttk.Entry(frame_input, width=12, font=("Arial", 11))
        self.entry_n.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.entry_n.bind("<Return>", lambda event: self.on_calculate())
        self.entry_n.focus_set()

        self.btn_calc = ttk.Button(frame_input, text="Вычислить", command=self.on_calculate)
        self.btn_calc.grid(row=0, column=2, padx=8, pady=5)

        frame_res = ttk.LabelFrame(self.root, text=" Результаты расчёта ", padding=10)
        frame_res.pack(fill="both", expand=True, padx=15, pady=5)

        self.lbl_f0 = ttk.Label(
            frame_res,
            text="0-индексация F(n): —",
            font=("Arial", 11, "bold"),
            foreground="#0b5345"
        )
        self.lbl_f0.pack(anchor="w", padx=5, pady=3)

        self.lbl_f1 = ttk.Label(
            frame_res,
            text="1-индексация F'(n): —",
            font=("Arial", 10),
            foreground="#4a235a"
        )
        self.lbl_f1.pack(anchor="w", padx=5, pady=3)

        self.lbl_note = ttk.Label(frame_res, text="Позиция в ряду: —", font=("Arial", 9, "italic"))
        self.lbl_note.pack(anchor="w", padx=5, pady=2)

        ttk.Label(frame_res, text="Последовательность членов ряда (F_0 .. F_n):").pack(
            anchor="w", padx=5, pady=(6, 2)
        )

        self.txt_seq = tk.Text(frame_res, height=5, wrap="word", font=("Consolas", 10))
        self.txt_seq.pack(fill="both", expand=True, padx=5, pady=4)

        frame_actions = ttk.Frame(self.root, padding=5)
        frame_actions.pack(fill="x", padx=15, pady=5)

        self.btn_save = ttk.Button(
            frame_actions,
            text="Сохранить в файл",
            command=self.on_save_file,
            state="disabled"
        )
        self.btn_save.pack(side="left", padx=5)

        self.btn_clear = ttk.Button(frame_actions, text="Очистить", command=self.on_clear)
        self.btn_clear.pack(side="right", padx=5)

        self.status_var = tk.StringVar(value="Готово к расчёту (диапазон n: 0..40)")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=(8, 3)
        )
        self.status_bar.pack(side="bottom", fill="x")

    def on_calculate(self) -> None:
        """Расчёт с полной валидацией и соблюдением Требования 14."""
        raw_text = self.entry_n.get().strip()

        if not raw_text:
            messagebox.showwarning("Предупреждение", "Поле ввода не должно быть пустым!")
            self.entry_n.delete(0, tk.END)
            self.entry_n.focus_set()
            self.status_var.set("Предупреждение: пустой ввод")
            return

        try:
            val_n = int(raw_text)
        except ValueError:
            messagebox.showerror(
                "Ошибка ввода",
                f"Значение {raw_text!r} не является целым числом!\n"
                f"Пожалуйста, введите целое число от 0 до 40."
            )
            # Требование 14: очистка поля ввода после ошибки
            self.entry_n.delete(0, tk.END)
            self.entry_n.focus_set()
            self.status_var.set("Ошибка: неверный формат ввода")
            return

        try:
            # Вызов эталонного ядра с полной проверкой диапазона
            res, _ = compute_fibonacci(val_n, track_path=False)
            seq = get_fibonacci_sequence(val_n)
            dual_info = get_dual_index_info(val_n)

            self.last_n = val_n
            self.last_val = res
            self.last_seq = seq

            # Обновление UI
            self.lbl_f0.config(text=f"0-индексация (OEIS A000045): {dual_info['f_zero_label']}")
            self.lbl_f1.config(text=f"1-индексация: {dual_info['f_one_label']}")
            self.lbl_note.config(text=dual_info['description'])

            self.txt_seq.delete("1.0", tk.END)
            self.txt_seq.insert("1.0", format_sequence_str(seq, max_items=25))

            save_to_file_v2(val_n, res, seq)
            self.btn_save.config(state="normal")
            self.status_var.set(f"Успешно: F({val_n}) = {res}. Данные сохранены в файл.")

        except ValueError as v_err:
            messagebox.showerror("Ошибка диапазона", str(v_err))
            # Требование 14: автоматическая очистка поля ввода
            self.entry_n.delete(0, tk.END)
            self.entry_n.focus_set()
            self.status_var.set(f"Ошибка диапазона: {v_err}")

    def on_save_file(self) -> None:
        if not self.last_seq:
            return
        p = save_to_file_v2(self.last_n, self.last_val, self.last_seq)
        messagebox.showinfo("Сохранение", f"Файл успешно сохранен:\n{p}")

    def on_clear(self) -> None:
        self.entry_n.delete(0, tk.END)
        self.lbl_f0.config(text="0-индексация F(n): —")
        self.lbl_f1.config(text="1-индексация F'(n): —")
        self.lbl_note.config(text="Позиция в ряду: —")
        self.txt_seq.delete("1.0", tk.END)
        self.btn_save.config(state="disabled")
        self.status_var.set("Поля очищены.")
        self.entry_n.focus_set()


def run_cli_v2(args: argparse.Namespace) -> int:
    """Пакетный запуск v2.0 с поддержкой трассировки CFG."""
    val_n = args.n
    tracer = CFGTracer() if args.trace else None

    if not args.quiet:
        print("=" * 65)
        print("  Fibonacci Calculator v2.0 — CLI Interface (Defect Fixed)")
        print("=" * 65)
        print(f"Входной параметр n: {val_n}")

    try:
        res, path = compute_fibonacci(val_n, track_path=args.trace, tracer=tracer)
        seq = get_fibonacci_sequence(val_n)
        dual = get_dual_index_info(val_n)

        if not args.quiet:
            print(f"Результат {dual['f_zero_label']} (0-индексация)")
            print(f"Результат {dual['f_one_label']} (1-индексация)")
            print(f"Последовательность: {format_sequence_str(seq, max_items=20)}")
            if args.trace:
                print(f"Маршрут CFG: {' -> '.join(path)}")

        filepath = args.file or DEFAULT_DATA_FILE
        saved_path = save_to_file_v2(val_n, res, seq, filepath)
        if not args.quiet:
            print(f"Файл сохранен: {saved_path}")
            print("Статус: PASS (Код возврата 0)")
        return 0

    except (ValueError, TypeError) as err:
        print(f"\n[ОШИБКА ВАЛИДАЦИИ] Перехвачено исключение: {err}", file=sys.stderr)
        if args.trace and tracer:
            print(f"Маршрут до сбоя: {tracer.format_route()}", file=sys.stderr)
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Вычисление чисел Фибоначчи — Версия 2.0")
    parser.add_argument("--cli", action="store_true", help="Запуск в консольном режиме")
    parser.add_argument("--n", type=int, help="Порядковый номер n")
    parser.add_argument("--file", type=str, default=DEFAULT_DATA_FILE, help="Путь к файлу")
    parser.add_argument("--trace", action="store_true", help="Включить трассировку вершин CFG")
    parser.add_argument("--quiet", action="store_true", help="Краткий вывод")

    args = parser.parse_args()

    if args.cli or args.n is not None:
        if args.n is None:
            print("Ошибка: В режиме --cli укажите --n <число>!", file=sys.stderr)
            sys.exit(1)
        sys.exit(run_cli_v2(args))
    else:
        root = tk.Tk()
        app = FibonacciAppV2GUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()
