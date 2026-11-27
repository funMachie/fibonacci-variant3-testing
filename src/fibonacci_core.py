"""
Fibonacci Core Engine (src/fibonacci_core.py)
=============================================
Дисциплина: Тестирование программного обеспечения
Вариант 3: «Вычисление чисел Фибоначчи»
Студент: Баймуратов А.И., гр. БПИ-23-01
Преподаватель: к.х.н., доцент Махмутова Р.И.
УГНТУ, 2026

Эталонное вычислительное ядро алгоритма Фибоначчи:
- Диапазон: 0 <= n <= 40
- Строгая проверка типов (защита от bool, float, str, None)
- Интегрированная трассировка базовых путей CFG
- Поддержка двойной индексации и генерации последовательностей
"""

from typing import Any, Dict, List, Optional, Tuple

try:
    from src.tracer import CFGTracer
except ImportError:
    from tracer import CFGTracer  # type: ignore


# Константы диапазона
FIBONACCI_MIN_N = 0
FIBONACCI_MAX_N = 40


def compute_fibonacci(
    n: Any,
    track_path: bool = False,
    tracer: Optional[CFGTracer] = None
) -> Tuple[int, List[str]]:
    """
    Вычисляет n-е число Фибоначчи для 0 <= n <= 40 по формуле:
      F(0) = 0
      F(1) = 1
      F(n) = F(n-1) + F(n-2)  при n >= 2

    Параметры:
      n: целое неотрицательное число в диапазоне [0, 40].
         Строго запрещены типы bool, float, str, None, list и др.
      track_path: если True, возвращает маршрут пройденных вершин графа CFG.
      tracer: опциональный внешний экземпляр CFGTracer для сбора трассы.

    Возвращает:
      (result, path): кортеж из целочисленного результата и списка пройденных узлов.

    Исключения:
      TypeError: если тип аргумента n не int или является bool.
      ValueError: если n < 0 или n > 40.
    """
    # Инициализация трассировщика при необходимости
    active_tracer = tracer
    if active_tracer is None and track_path:
        active_tracer = CFGTracer()

    # --- Узел 1: Валидация типа входного аргумента ---
    if active_tracer is not None:
        active_tracer.step("1")
    if type(n) is bool or not isinstance(n, int):
        if active_tracer is not None:
            active_tracer.step("11")
        err = TypeError(
            f"Порядковый номер n должен быть целым числом (int), получено: "
            f"{type(n).__name__} (значение: {n!r})"
        )
        if active_tracer is not None:
            setattr(err, "route", active_tracer.get_path())
        raise err

    # --- Узел 2: Валидация нижней границы диапазона (n >= 0) ---
    if active_tracer is not None:
        active_tracer.step("2")
    if n < FIBONACCI_MIN_N:
        if active_tracer is not None:
            active_tracer.step("11")
        err = ValueError(
            f"Порядковый номер n не может быть отрицательным (n >= {FIBONACCI_MIN_N}), "
            f"получено: {n}"
        )
        if active_tracer is not None:
            setattr(err, "route", active_tracer.get_path())
        raise err

    # --- Узел 3: Валидация верхней границы диапазона (n <= 40) ---
    if active_tracer is not None:
        active_tracer.step("3")
    if n > FIBONACCI_MAX_N:
        if active_tracer is not None:
            active_tracer.step("11")
        err = ValueError(
            f"Порядковый номер n превышает максимально допустимое значение "
            f"{FIBONACCI_MAX_N} (n <= {FIBONACCI_MAX_N}), получено: {n}"
        )
        if active_tracer is not None:
            setattr(err, "route", active_tracer.get_path())
        raise err

    # --- Узел 4: Проверка базового случая n == 0 ---
    if active_tracer is not None:
        active_tracer.step("4")
    if n == 0:
        if active_tracer is not None:
            active_tracer.step("5")
            active_tracer.step("11")
        route = active_tracer.get_path() if active_tracer is not None else []
        return 0, route

    # --- Узел 6: Проверка базового случая n == 1 ---
    if active_tracer is not None:
        active_tracer.step("6")
    if n == 1:
        if active_tracer is not None:
            active_tracer.step("7")
            active_tracer.step("11")
        route = active_tracer.get_path() if active_tracer is not None else []
        return 1, route

    # --- Узел 8: Инициализация переменных цикла ---
    if active_tracer is not None:
        active_tracer.step("8")
    f_prev = 0
    f_curr = 1
    i = 2

    # --- Узел 9: Цикл с предусловием (while i <= n) ---
    while True:
        if active_tracer is not None:
            active_tracer.step("9")
        if i <= n:
            # --- Узел 10: Тело цикла (вычисление суммы и сдвиг) ---
            if active_tracer is not None:
                active_tracer.step("10")
            f_next = f_prev + f_curr
            f_prev = f_curr
            f_curr = f_next
            i += 1
        else:
            break

    # --- Узел 11: Возврат результата ---
    if active_tracer is not None:
        active_tracer.step("11")
    route = active_tracer.get_path() if active_tracer is not None else []
    return f_curr, route


def get_fibonacci_sequence(n: int) -> List[int]:
    """
    Возвращает полный список чисел Фибоначчи от F(0) до F(n) включительно.

    Параметры:
      n: целое неотрицательное число в диапазоне [0, 40].

    Возвращает:
      List[int]: последовательность значений [F(0), F(1), ..., F(n)].
    """
    if type(n) is bool or not isinstance(n, int):
        raise TypeError(f"n должно быть целым числом, получено: {type(n).__name__}")
    if n < FIBONACCI_MIN_N or n > FIBONACCI_MAX_N:
        raise ValueError(
            f"n должно быть в диапазоне [{FIBONACCI_MIN_N}, {FIBONACCI_MAX_N}], получено: {n}"
        )

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


def format_sequence_str(seq: List[int], max_items: int = 15) -> str:
    """
    Форматирует последовательность чисел Фибоначчи в компактную строку для UI.
    """
    if len(seq) <= max_items:
        return ", ".join(str(x) for x in seq)
    head = ", ".join(str(x) for x in seq[:8])
    tail = ", ".join(str(x) for x in seq[-4:])
    return f"{head}, ..., {tail} (всего {len(seq)} элементов)"


def get_dual_index_info(n: int) -> Dict[str, Any]:
    """
    Формирует структуру сопоставления математической 0-индексации (OEIS A000045)
    и классической 1-индексации для числа с номером n.

    Возвращает словарь с форматированными строками для GUI и отчетов.
    """
    val, _ = compute_fibonacci(n, track_path=False)

    if n == 0:
        f_one_label = "F'(0) — не определено (нулевой элемент вне натурального счета)"
        desc = (
            f"0-индексация: F(0) = {val} | "
            f"1-индексация: ряд начинается с F'(1) = 1 | "
            f"Позиция: 1-й элемент полного ряда"
        )
    else:
        f_one_label = f"F'({n}) = {val}"
        desc = (
            f"0-индексация: F({n}) = {val} | "
            f"1-индексация (без 0): F'({n}) = {val} | "
            f"Позиция: {n + 1}-й элемент ряда (включая F_0)"
        )

    return {
        "n": n,
        "value": val,
        "f_zero_label": f"F({n}) = {val}",
        "f_one_label": f_one_label,
        "sequence_rank": n + 1,
        "description": desc,
    }
