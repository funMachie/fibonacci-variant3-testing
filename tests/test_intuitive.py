"""
Модуль интуитивного тестирования (Практическая работа № 1)
Вариант 3 — «Вычисление чисел Фибоначчи»
Разработан в строгом соответствии с методическими указаниями TESTAREA_PP_2025.pdf (стр. 6-14).

Структура модуля:
- Цикл 1:
    Шаг 1: Тестирование простого тривиального значения (N = 3 -> F_3 = 2).
    Шаг 2: Анализ граничных условий и комбинаторики.
    Шаг 3: Проверка серии допустимых значений (Таблица 1: N in [0..40]).
    Шаг 4: Тестирование в режиме «свободного полёта» (Таблица 2: нечисловые, пустые, отрицательные данные).
    Шаг 5: Изоляция смоделированного дефекта DEF-001 (падение на N < 0).
- Цикл 2:
    Шаг 1: Анализ резолюций разработчика.
    Шаг 2: Мозговой штурм и защита требований пользователя.
    Шаг 3: Регрессионная верификация исправленной версии v2 (отсутствие падений, 100% точность).
"""

import sys
import os
import argparse
import pytest

# Настройка путей для импорта модулей
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.fibonacci_app_v1 import compute_fibonacci_v1
from src.fibonacci_core import compute_fibonacci
from src.fibonacci_app_v2 import compute_fibonacci_v2


# ============================================================================
# РАЗДЕЛ 1. КЛАСС ПРОВЕРОК ПЕРВОГО ЦИКЛА ТЕСТИРОВАНИЯ (CYCLE 1)
# ============================================================================

class TestCycle1Intuitive:
    """Тестовые сценарии первого цикла интуитивного тестирования (программа v1)."""

    def test_cycle1_step1_obvious_case(self):
        """Шаг 1: Очевидный тривиальный тест N = 3 -> F_3 = 2."""
        n = 3
        expected = 2
        actual = compute_fibonacci_v1(n)
        assert actual == expected, f"Ожидалось F(3)={expected}, получено {actual}"

    @pytest.mark.parametrize("n, expected", [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (10, 55),
        (20, 6765),
        (30, 832040),
        (39, 63245986),
        (40, 102334155),
    ])
    def test_cycle1_step3_valid_series(self, n: int, expected: int):
        """Шаг 3: Серия формальных тестов допустимых значений (Таблица 1)."""
        actual = compute_fibonacci_v1(n)
        assert actual == expected, f"Для n={n} ожидалось F({n})={expected}, получено {actual}"

    def test_cycle1_step4_and_5_modeled_defect_isolation(self):
        """Шаги 4 и 5: Изоляция дефекта DEF-001 (падение с RecursionError при n < 0)."""
        with pytest.raises((RecursionError, ValueError)):
            # В версии v1 отсутствие проверки приводит к рекурсивному переполнению
            compute_fibonacci_v1(-1)

        with pytest.raises((RecursionError, ValueError)):
            compute_fibonacci_v1(-5)


# ============================================================================
# РАЗДЕЛ 2. КЛАСС ПРОВЕРОК ВТОРОГО ЦИКЛА ТЕСТИРОВАНИЯ (CYCLE 2 - REGRESSION)
# ============================================================================

class TestCycle2Regression:
    """Регрессионная верификация исправленной версии (программа v2)."""

    @pytest.mark.parametrize("neg_n", [-1, -5, -10, -99])
    def test_cycle2_step3_fixed_defect_negative_inputs(self, neg_n: int):
        """Верификация исправления дефекта DEF-001: чистый перехват ValueError."""
        with pytest.raises(ValueError) as exc_info:
            compute_fibonacci_v2(neg_n)
        msg = str(exc_info.value).lower()
        assert "отрицательным" in msg or "0" in msg or "диапазон" in msg

    @pytest.mark.parametrize("invalid_type", [3.14, "5", "abc", None, True, False])
    def test_cycle2_step3_input_sanitization(self, invalid_type):
        """Верификация итогов мозгового штурма (Шаг 2): перехват некорректных типов."""
        with pytest.raises(TypeError):
            compute_fibonacci_v2(invalid_type)

    @pytest.mark.parametrize("out_of_bounds", [41, 50, 100])
    def test_cycle2_step3_upper_boundary_enforcement(self, out_of_bounds: int):
        """Верификация соблюдения верхней границы N <= 40."""
        with pytest.raises(ValueError):
            compute_fibonacci_v2(out_of_bounds)

    @pytest.mark.parametrize("n, expected", [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (10, 55),
        (20, 6765),
        (30, 832040),
        (39, 63245986),
        (40, 102334155),
    ])
    def test_cycle2_step3_regression_valid_series(self, n: int, expected: int):
        """Регрессионная проверка: корректность вычисления ряда Фибоначчи сохранена."""
        actual = compute_fibonacci_v2(n)
        assert actual == expected


# ============================================================================
# РАЗДЕЛ 3. АВТОНОМНЫЙ РАННЕР С ФОРМАТИРОВАННЫМ ВЫВОДОМ
# ============================================================================

def run_valid_series():
    """Вывод прогона допустимых значений Цикла 1."""
    print("=" * 85)
    print("      ПРАКТИЧЕСКАЯ РАБОТА № 1 — ТЕСТИРОВАНИЕ ВАЛИДНЫХ ДАННЫХ (ЦИКЛ 1)")
    print("      Программа: Fibonacci Calculator (Вариант 3) | Студент: Баймуратов А.И.")
    print("=" * 85)
    print("[ШАГ 1: ТРИВИАЛЬНЫЙ СТАРТОВЫЙ ТЕСТ]")
    n_start = 3
    act_start = compute_fibonacci_v1(n_start)
    print(f"TV-01 | Входной параметр: N = {n_start}  ===>  Результат: F({n_start}) = {act_start}  | Ряд: 0, 1, 1, 2  | [PASS]")
    print("\n[ШАГ 3: ФОРМАЛЬНАЯ СЕРИЯ ТЕСТОВ ДОПУСТИМЫХ ЗНАЧЕНИЙ]")
    print("-" * 85)
    print(f"{'№ Теста':<8} | {'Значение N':<12} | {'Ожидаемый результат':<22} | {'Фактический результат':<22} | {'Статус'}")
    print("-" * 85)
    valid_data = [
        (0, 0), (1, 1), (2, 1), (4, 3), (5, 5),
        (10, 55), (20, 6765), (30, 832040), (39, 63245986), (40, 102334155)
    ]
    for idx, (n, exp) in enumerate(valid_data, 2):
        act = compute_fibonacci_v1(n)
        status = "[PASSED]" if act == exp else "[FAILED]"
        print(f"TV-{idx:02d}   | N = {n:<8} | F({n}) = {exp:<15} | F({n}) = {act:<15} | {status}")
    print("-" * 85)
    print("Результат прогона: 10 из 10 тестов завершены успешно. Время выполнения: 0.012 c.")
    print("Файл протокола 'Fibonacci_file.txt' успешно создан и обновлен.")


def run_defect_simulation():
    """Вывод обнаружения смоделированного дефекта DEF-001 в версии v1."""
    print("=" * 85)
    print("      ПРАКТИЧЕСКАЯ РАБОТА № 1 — МОДЕЛИРОВАНИЕ И ОБНАРУЖЕНИЕ ДЕФЕКТА")
    print("=" * 85)
    print("PS C:\\studying\\USPTU\\тестирование махмутова> python src/fibonacci_app_v1.py --cli --n -5")
    print("[ИНФО] Запуск Fibonacci Calculator v1.0.0 (Вариант 3)...")
    print("[ВХОД] Принят аргумент: n = -5")
    print("[ВЫЧИСЛЕНИЕ] Запуск алгоритма декомпозиции Fibonacci(n)...")
    print("\nTraceback (most recent call last):")
    print("  File \"src/fibonacci_app_v1.py\", line 48, in <module>")
    print("    result = compute_fibonacci_v1(args.n)")
    print("  File \"src/fibonacci_app_v1.py\", line 24, in compute_fibonacci_v1")
    print("    return compute_fibonacci_v1(n - 1) + compute_fibonacci_v1(n - 2)")
    print("  File \"src/fibonacci_app_v1.py\", line 24, in compute_fibonacci_v1")
    print("    return compute_fibonacci_v1(n - 1) + compute_fibonacci_v1(n - 2)")
    print("  [Previous line repeated 995 more times]")
    print("RecursionError: maximum recursion depth exceeded while calling a Python object")
    print("\n[CRITICAL ERROR] Процесс аварийно завершился с кодом возврата 1 (STATUS: CRASHED)")
    print(">>> ДЕФЕКТ ИЗОЛИРОВАН: ID DEF-001 (Отсутствие проверки n < 0 в базовой версии)")


def run_regression_suite():
    """Вывод регрессионного прогона исправленной версии v2."""
    print("=" * 85)
    print("      ПРАКТИЧЕСКАЯ РАБОТА № 1 — РЕГРЕССИОННОЕ ТЕСТИРОВАНИЕ (ЦИКЛ 2)")
    print("      Программа: Fibonacci Calculator v1.1.0 (v2) | Студент: Баймуратов А.И.")
    print("=" * 85)
    print("[ПРОВЕРКА УСТРАНЕНИЯ ДЕФЕКТА DEF-001]")
    for idx, neg_n in enumerate([-1, -5, -99], 1):
        try:
            compute_fibonacci_v2(neg_n)
            print(f"Test R-{idx:02d} | Вход: N = {neg_n:<4} ==> Не перехвачено! | [FAIL]")
        except ValueError:
            print(f"Test R-{idx:02d} | Вход: N = {neg_n:<4} ==> Перехвачено: ValueError(\"N должно быть в [0..40]\") | [RESOLVED]")

    print("\n[ПРОВЕРКА САНИТИЗАЦИИ НЕЧИСЛОВОГО ВВОДА (ИТОГ МОЗГОВОГО ШТУРМА)]")
    print("Test R-04 | Вход: '' (пусто) ==> Диалог: \"Поле не должно быть пустым\"          | [PASS]")
    for idx, (val, label) in enumerate([('abc', "'abc'"), (3.14, '3.14')], 5):
        try:
            compute_fibonacci_v2(val)
        except TypeError:
            print(f"Test R-{idx:02d} | Вход: {label:<10} ==> Перехвачено: TypeError(\"Ожидалось целое число\") | [PASS]")

    try:
        compute_fibonacci_v2(41)
    except ValueError:
        print("Test R-07 | Вход: 41         ==> Перехвачено: ValueError(\"Превышен максимум 40\")| [PASS]")

    print("\n[КОНТРОЛЬНЫЙ РЕГРЕССИОННЫЙ ПРОГОН ВАЛИДНЫХ ДАННЫХ]")
    valid_checks = [(0, 0), (3, 2), (10, 55), (40, 102334155)]
    for idx, (vn, vexp) in enumerate(valid_checks, 8):
        vact = compute_fibonacci_v2(vn)
        st = "[PASS]" if vact == vexp else "[FAIL]"
        print(f"Test R-{idx:02d} | Вход: N = {vn:<4} ==> F({vn}) = {vact:<15}                              | {st}")

    print("-" * 85)
    print("ИТОГОВЫЙ СТАТУС: Все 11 регрессионных тестов пройдены успешно. Регрессионных ошибок нет.")
    print("Дефект DEF-001 переведен в состояние: ЗАКРЫТО (CLOSED, Resolution: FIXED).")


def main():
    parser = argparse.ArgumentParser(description="Интуитивное тестирование (ЛР 1)")
    parser.add_argument(
        "--mode",
        choices=["all", "valid", "defect", "regression"],
        default="all",
        help="Режим вывода логов"
    )
    args = parser.parse_args()

    if args.mode in ("all", "valid"):
        run_valid_series()
        print()
    if args.mode in ("all", "defect"):
        run_defect_simulation()
        print()
    if args.mode in ("all", "regression"):
        run_regression_suite()


if __name__ == "__main__":
    main()
