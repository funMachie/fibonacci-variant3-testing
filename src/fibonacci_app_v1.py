"""
Fibonacci Application v1.0 — Практическая работа № 1 (src/fibonacci_app_v1.py)
=============================================================================
Дисциплина: Тестирование программного обеспечения
Вариант 3: «Вычисление чисел Фибоначчи»
Студент: Баймуратов А.И., гр. БПИ-23-01
Преподаватель: к.х.н., доцент Махмутова Р.И.
УГНТУ, 2026

ВЕРСИЯ 1.0 (Содержит смоделированные дефекты для интуитивного тестирования):
1. Дефект кодирования: Отсутствует проверка на отрицательные числа (n < 0),
   что приводит к аварийному завершению с RecursionError при вводе n = -1 или n = -5.
2. Дефект интерфейса: Поле ввода не очищается после ошибки (нарушение Требования 14).
3. Поддерживает работу в двух режимах: Tkinter GUI и пакетный CLI.
"""

import argparse
import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

DEFAULT_DATA_FILE = "Fibonacci_file.txt"


# ----------------------------------------------------------------------
# Вычислительное ядро версии 1.0 (с умышленным дефектом DEF-001)
# ----------------------------------------------------------------------
def compute_fibonacci_v1(n: int) -> int:
    """
    Вычисление числа Фибоначчи в версии 1.0.

    ВНИМАНИЕ (Смоделированный дефект кодирования DEF-001):
    Отсутствует валидация n < 0! При отрицательном значении n рекурсия уходит
    в бесконечность, порождая исключение RecursionError.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    # Отсутствует условие if n < 0!
    # Для ускорения положительных значений n >= 2 используется цикл:
    if n >= 2:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    # Сюда попадают n < 0, вызывая рекурсивный коллапс:
    return compute_fibonacci_v1(n - 1) + compute_fibonacci_v1(n - 2)


def get_sequence_v1(n: int) -> List[int]:
    """Возвращает последовательность чисел до n."""
    if n < 0:
        # Падает с RecursionError аналогично ядру
        return [compute_fibonacci_v1(n)]
    seq = [0]
    if n == 0:
        return seq
    seq.append(1)
    if n == 1:
        return seq
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
        seq.append(b)
    return seq


def save_to_file_v1(n: int, val: int, seq: List[int], filepath: str = DEFAULT_DATA_FILE) -> str:
    """
    Сохраняет результаты расчета в файл протокола (Требования 2-5, 11-13 Приложения В).
    """
    seq_str = ", ".join(str(x) for x in seq)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = (
        f"Входной параметр n: {n}\n"
        f"Число Фибоначчи F(n): {val}\n"
        f"Последовательность: {seq_str}\n"
        f"Дата и время расчета: {timestamp}\n"
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(filepath)


# ----------------------------------------------------------------------
# Графический интерфейс Tkinter (GUI v1.0)
# ----------------------------------------------------------------------
class FibonacciAppV1GUI:
    """
    Оконный интерфейс на базе Tkinter для версии 1.0.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        # Дефект заголовка: неполное название
        self.root.title("Fibonacci Calculator (v1.0 - Unfixed)")
        self.root.geometry("540x440")
        self.root.minsize(480, 380)

        self.last_n: int = 0
        self.last_val: int = 0
        self.last_seq: List[int] = []

        self._build_widgets()

    def _build_widgets(self) -> None:
        # Верхний фрейм ввода
        frame_input = ttk.LabelFrame(self.root, text=" Ввод исходных данных ", padding=10)
        frame_input.pack(fill="x", padx=15, pady=10)

        lbl_prompt = ttk.Label(frame_input, text="Введите номер числа Фибоначчи (n):")
        lbl_prompt.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.entry_n = ttk.Entry(frame_input, width=15, font=("Arial", 11))
        self.entry_n.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.entry_n.focus_set()

        self.btn_calc = ttk.Button(frame_input, text="Вычислить", command=self.on_calculate)
        self.btn_calc.grid(row=0, column=2, padx=8, pady=5)

        # Фрейм отображения результатов
        frame_res = ttk.LabelFrame(self.root, text=" Результаты вычислений ", padding=10)
        frame_res.pack(fill="both", expand=True, padx=15, pady=5)

        self.lbl_f0 = ttk.Label(
            frame_res,
            text="0-индексация F(n): —",
            font=("Arial", 11, "bold"),
            foreground="#1b4f72"
        )
        self.lbl_f0.pack(anchor="w", padx=5, pady=4)

        self.lbl_f1 = ttk.Label(
            frame_res,
            text="1-индексация F'(n): —",
            font=("Arial", 10),
            foreground="#4a235a"
        )
        self.lbl_f1.pack(anchor="w", padx=5, pady=4)

        ttk.Label(frame_res, text="Сформированная последовательность (F_0 .. F_n):").pack(
            anchor="w", padx=5, pady=(8, 2)
        )

        self.txt_seq = tk.Text(frame_res, height=6, wrap="word", font=("Consolas", 10))
        self.txt_seq.pack(fill="both", expand=True, padx=5, pady=4)

        # Фрейм кнопок управления
        frame_actions = ttk.Frame(self.root, padding=5)
        frame_actions.pack(fill="x", padx=15, pady=5)

        self.btn_save = ttk.Button(
            frame_actions,
            text="Сохранить в Fibonacci_file.txt",
            command=self.on_save_file,
            state="disabled"
        )
        self.btn_save.pack(side="left", padx=5)

        self.btn_clear = ttk.Button(frame_actions, text="Очистить", command=self.on_clear)
        self.btn_clear.pack(side="right", padx=5)

        # Статус-бар внизу
        self.status_var = tk.StringVar(value="Готово к работе")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=(8, 3)
        )
        self.status_bar.pack(side="bottom", fill="x")

    def on_calculate(self) -> None:
        """
        Обработчик нажатия кнопки «Вычислить».
        Содержит смоделированный дефект: перехватывает ValueError,
        но НЕ перехватывает RecursionError и НЕ очищает поле при ошибке.
        """
        raw_text = self.entry_n.get().strip()

        # Проверка на пустой ввод
        if not raw_text:
            messagebox.showwarning("Предупреждение", "Поле ввода не должно быть пустым!")
            # Дефект: поле ввода не очищается и не сбрасывается
            self.status_var.set("Ошибка: пустой ввод")
            return

        try:
            val_n = int(raw_text)
        except ValueError:
            messagebox.showerror(
                "Ошибка ввода",
                f"Введено некорректное значение: {raw_text!r}. Допускаются только целые числа!"
            )
            # Дефект (нарушение Требования 14): поле ввода НЕ очищается после ошибки
            self.status_var.set("Ошибка: введено не целое число")
            return

        # Внимание: отсутствует валидация n < 0!
        # Вызов compute_fibonacci_v1(-1) приведет к необработанному RecursionError!
        try:
            if val_n > 40:
                messagebox.showwarning(
                    "Ограничение",
                    "Значение n > 40 превышает допустимый предел по спецификации!"
                )
                self.status_var.set("Предупреждение: n > 40")
                return

            res = compute_fibonacci_v1(val_n)
            seq = get_sequence_v1(val_n)

            self.last_n = val_n
            self.last_val = res
            self.last_seq = seq

            # Обновление UI
            self.lbl_f0.config(text=f"0-индексация F({val_n}) = {res}")
            if val_n == 0:
                self.lbl_f1.config(text="1-индексация: F'(0) — не определено (нулевой член)")
            else:
                self.lbl_f1.config(text=f"1-индексация F'({val_n}) = {res}")

            self.txt_seq.delete("1.0", tk.END)
            self.txt_seq.insert("1.0", ", ".join(str(x) for x in seq))

            # Автосохранение в файл по Требованию 4 Приложения В
            save_to_file_v1(val_n, res, seq)
            self.btn_save.config(state="normal")
            self.status_var.set(f"Успешно вычислено F({val_n}) = {res}. Данные сохранены в файл.")

        except RecursionError as err:
            # В версии 1.0 этот блок сознательно демонстрирует Traceback в терминале
            print(f"[CRITICAL UNHANDLED DEFECT] RecursionError: {err}", file=sys.stderr)
            raise  # Пробрасываем исключение наружу для фиксации аварии

    def on_save_file(self) -> None:
        """Ручное сохранение данных."""
        if not self.last_seq:
            messagebox.showwarning("Предупреждение", "Сначала выполните вычисление!")
            return
        abs_path = save_to_file_v1(self.last_n, self.last_val, self.last_seq)
        messagebox.showinfo("Сохранение", f"Результаты успешно сохранены в файл:\n{abs_path}")
        self.status_var.set("Файл обновлен вручную.")

    def on_clear(self) -> None:
        """Очистка полей."""
        self.entry_n.delete(0, tk.END)
        self.lbl_f0.config(text="0-индексация F(n): —")
        self.lbl_f1.config(text="1-индексация F'(n): —")
        self.txt_seq.delete("1.0", tk.END)
        self.btn_save.config(state="disabled")
        self.status_var.set("Поля очищены.")
        self.entry_n.focus_set()


# ----------------------------------------------------------------------
# Консольный режим CLI (поддержка флагов --cli, --n, --file)
# ----------------------------------------------------------------------
def run_cli_v1(args: argparse.Namespace) -> int:
    """Запуск приложения в пакетном консольном режиме."""
    val_n = args.n
    if not args.quiet:
        print("=" * 60)
        print("  Fibonacci Calculator v1.0 — CLI Mode (LR 1)")
        print("=" * 60)
        print(f"Входной параметр n: {val_n}")

    try:
        res = compute_fibonacci_v1(val_n)
        seq = get_sequence_v1(val_n)

        if not args.quiet:
            print(f"Результат F({val_n}) [0-индексация]: {res}")
            if val_n >= 1:
                print(f"Результат F'({val_n}) [1-индексация]: {res}")
            else:
                print("Результат F'(0) [1-индексация]: не определено (нулевой член)")
            print(f"Последовательность: {', '.join(str(x) for x in seq)}")

        filepath = args.file or DEFAULT_DATA_FILE
        saved_path = save_to_file_v1(val_n, res, seq, filepath)
        if not args.quiet:
            print(f"Результаты сохранены в: {saved_path}")
            print("Статус выполнения: УСПЕШНО (EXIT CODE 0)")
        return 0

    except RecursionError as r_err:
        print(f"\n[КРИТИЧЕСКИЙ СБОЙ] RecursionError при вычислении n = {val_n}:", file=sys.stderr)
        print(f"Описание ошибки: {r_err}", file=sys.stderr)
        print("Причина: Отсутствует проверка n < 0 в модуле compute_fibonacci_v1", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"\n[ОШИБКА] Необработанное исключение: {exc}", file=sys.stderr)
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Вычисление чисел Фибоначчи (Вариант 3) — Версия 1.0"
    )
    parser.add_argument("--cli", action="store_true", help="Запуск в консольном режиме без GUI")
    parser.add_argument("--n", type=int, help="Порядковый номер n числа Фибоначчи")
    parser.add_argument("--file", type=str, default=DEFAULT_DATA_FILE, help="Путь для сохранения файла")
    parser.add_argument("--quiet", action="store_true", help="Подавлять подробный консольный вывод")

    args = parser.parse_args()

    # Если передан флаг --cli или явно задан параметр --n, работаем в CLI
    if args.cli or args.n is not None:
        if args.n is None:
            print("Ошибка: В режиме --cli параметр --n <целое число> обязателен!", file=sys.stderr)
            sys.exit(1)
        sys.exit(run_cli_v1(args))
    else:
        root = tk.Tk()
        app = FibonacciAppV1GUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()
