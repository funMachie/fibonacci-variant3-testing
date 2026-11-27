"""
tests/test_units.py
===================
Комплекс модульных тестов (Unit Tests) для Практической работы № 4 (Часть 2).
Разработан на базе фреймворка Pytest в соответствии с МУ TESTAREA_PP_2025.pdf (стр. 57–66).
Вариант 3: «Вычисление чисел Фибоначчи» (0 <= N <= 40).

Студент: Баймуратов А.И. (гр. БПИ-23-01)
Преподаватель: к.х.н., доцент Махмутова Р.И.
УГНТУ, 2026

Архитектура тестового набора:
- 6 специализированных тестовых классов (TestFibonacciBasic, TestFibonacciParametrized,
  TestFibonacciBoundaries, TestFibonacciExceptions, TestFibonacciTracer, TestFibonacciAuxiliary).
- 4 декларативные тестовые фикстуры (tracer, sample_fibonacci_data, boundary_cases, invalid_type_matrix).
- 7 параметризованных матриц (@pytest.mark.parametrize).
- Контрактная валидация исключительных ситуаций через pytest.raises с анализом сообщений.
- Группировка по маркерам (@pytest.mark.smoke, @pytest.mark.regression, @pytest.mark.whitebox).
"""

import sys
import os
import pytest
from typing import Any, Dict, List, Tuple

# Обеспечение доступности корневых пакетов проекта
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.fibonacci_core import (
    compute_fibonacci,
    get_fibonacci_sequence,
    get_dual_index_info,
    format_sequence_str,
    FIBONACCI_MIN_N,
    FIBONACCI_MAX_N
)
from src.tracer import CFGTracer


# ============================================================================
# РАЗДЕЛ 1. ТЕСТОВЫЕ ФИКСТУРЫ (@pytest.fixture)
# ============================================================================

@pytest.fixture
def tracer() -> CFGTracer:
    """
    Фикстура для изолированной трассировки маршрутов графа CFG.
    Создает чистый экземпляр CFGTracer и очищает его после завершения теста.
    """
    t = CFGTracer()
    yield t
    t.reset()


@pytest.fixture(scope="module")
def sample_fibonacci_data() -> Dict[int, int]:
    """Справочная таблица эталонных значений ряда Фибоначчи (OEIS A000045)."""
    return {
        0: 0,
        1: 1,
        2: 1,
        3: 2,
        4: 3,
        5: 5,
        6: 8,
        7: 13,
        8: 21,
        9: 34,
        10: 55,
        15: 610,
        20: 6765,
        25: 75025,
        30: 832040,
        35: 9227465,
        39: 63245986,
        40: 102334155
    }


@pytest.fixture(scope="module")
def boundary_cases() -> Dict[str, int]:
    """Граничные значения диапазона допустимых индексов."""
    return {
        "min_valid": FIBONACCI_MIN_N,
        "next_valid": FIBONACCI_MIN_N + 1,
        "pre_max_valid": FIBONACCI_MAX_N - 1,
        "max_valid": FIBONACCI_MAX_N,
        "below_min": FIBONACCI_MIN_N - 1,
        "above_max": FIBONACCI_MAX_N + 1
    }


@pytest.fixture(scope="module")
def invalid_type_matrix() -> List[Any]:
    """Коллекция недопустимых типов данных для проверки строгой типизации."""
    return [
        True, False,           # Логические типы
        0.0, 1.5, 3.14, -0.1,  # Вещественные числа
        "0", "10", "abc", "",  # Строковые значения
        None,                  # Отсутствие значения
        [0], (1,), {"n": 5}    # Коллекции и структуры
    ]


# ============================================================================
# РАЗДЕЛ 2. КЛАСС БАЗОВЫХ ТЕСТОВ (TestFibonacciBasic)
# ============================================================================

@pytest.mark.smoke
class TestFibonacciBasic:
    """Базовые приемочные проверки корректности вычислительного ядра."""

    def test_base_case_zero(self):
        """Проверка нулевого базового элемента F(0) = 0."""
        val, _ = compute_fibonacci(0)
        assert val == 0
        assert isinstance(val, int)

    def test_base_case_one(self):
        """Проверка первого базового элемента F(1) = 1."""
        val, _ = compute_fibonacci(1)
        assert val == 1
        assert isinstance(val, int)

    def test_first_computed_element(self):
        """Проверка первого вычисляемого через цикл элемента F(2) = 1."""
        val, _ = compute_fibonacci(2)
        assert val == 1
        assert isinstance(val, int)

    def test_determinism(self):
        """Проверка детерминированности функции при повторных вызовах."""
        res1, _ = compute_fibonacci(10)
        res2, _ = compute_fibonacci(10)
        assert res1 == res2 == 55


# ============================================================================
# РАЗДЕЛ 3. ПАРАМЕТРИЗОВАННЫЕ ВЫЧИСЛЕНИЯ (TestFibonacciParametrized)
# ============================================================================

@pytest.mark.smoke
@pytest.mark.regression
class TestFibonacciParametrized:
    """Параметризованное тестирование допустимого диапазона [0, 40]."""

    # Матрица 1: Табличные пары OEIS A000045
    @pytest.mark.parametrize("n, expected", [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
        (12, 144),
        (15, 610),
        (18, 2584),
        (20, 6765),
        (25, 75025),
        (30, 832040),
        (35, 9227465),
        (39, 63245986),
        (40, 102334155),
    ])
    def test_fibonacci_values(self, n: int, expected: int):
        """Сверка вычисленного числа Фибоначчи с эталоном OEIS A000045."""
        actual, _ = compute_fibonacci(n)
        assert actual == expected, f"F({n}) ожидалось {expected}, получено {actual}"

    def test_fixture_values_consistency(self, sample_fibonacci_data: Dict[int, int]):
        """Проверка согласованности вычислений по фикстуре эталонных данных."""
        for n, exp in sample_fibonacci_data.items():
            act, _ = compute_fibonacci(n)
            assert act == exp

    # Матрица 2: Рекуррентное соотношение F(n) = F(n-1) + F(n-2)
    @pytest.mark.parametrize("n", [5, 10, 15, 20, 30, 40])
    def test_recurrence_relation(self, n: int):
        """Проверка фундаментального рекуррентного соотношения F(n) = F(n-1) + F(n-2)."""
        fn, _ = compute_fibonacci(n)
        fn_minus_1, _ = compute_fibonacci(n - 1)
        fn_minus_2, _ = compute_fibonacci(n - 2)
        assert fn == fn_minus_1 + fn_minus_2


# ============================================================================
# РАЗДЕЛ 4. ГРАНИЧНЫЕ УСЛОВИЯ И BVA (TestFibonacciBoundaries)
# ============================================================================

@pytest.mark.regression
class TestFibonacciBoundaries:
    """Тестирование дискретных граничных условий диапазона."""

    def test_lower_boundary_valid(self, boundary_cases: Dict[str, int]):
        """Нижняя граница допустимого диапазона: n = 0."""
        val, _ = compute_fibonacci(boundary_cases["min_valid"])
        assert val == 0

    def test_lower_boundary_plus_one(self, boundary_cases: Dict[str, int]):
        """Прилегающая внутренняя точка нижней границы: n = 1."""
        val, _ = compute_fibonacci(boundary_cases["next_valid"])
        assert val == 1

    def test_upper_boundary_valid(self, boundary_cases: Dict[str, int]):
        """Верхняя граница допустимого диапазона: n = 40."""
        val, _ = compute_fibonacci(boundary_cases["max_valid"])
        assert val == 102334155

    def test_upper_boundary_minus_one(self, boundary_cases: Dict[str, int]):
        """Прилегающая внутренняя точка верхней границы: n = 39."""
        val, _ = compute_fibonacci(boundary_cases["pre_max_valid"])
        assert val == 63245986

    def test_lower_boundary_invalid(self, boundary_cases: Dict[str, int]):
        """Нарушение нижней границы диапазона: n = -1."""
        with pytest.raises(ValueError, match=r"Порядковый номер n не может быть отрицательным"):
            compute_fibonacci(boundary_cases["below_min"])

    def test_upper_boundary_invalid(self, boundary_cases: Dict[str, int]):
        """Нарушение верхней границы диапазона: n = 41."""
        with pytest.raises(ValueError, match=r"Порядковый номер n превышает максимально допустимое значение"):
            compute_fibonacci(boundary_cases["above_max"])


# ============================================================================
# РАЗДЕЛ 5. ОБРАБОТКА ИСКЛЮЧЕНИЙ И ТИПИЗАЦИЯ (TestFibonacciExceptions)
# ============================================================================

@pytest.mark.regression
class TestFibonacciExceptions:
    """Верификация строгой контрактной типизации и обработки исключительных ситуаций."""

    # Матрица 3: Отрицательные числа (ValueError)
    @pytest.mark.parametrize("neg_n", [-1, -2, -5, -10, -50, -100, -999])
    def test_negative_values_raise_value_error(self, neg_n: int):
        """Любые отрицательные значения должны вызывать ValueError."""
        with pytest.raises(ValueError) as exc_info:
            compute_fibonacci(neg_n)
        assert "не может быть отрицательным" in str(exc_info.value)
        assert f"получено: {neg_n}" in str(exc_info.value)

    # Матрица 4: Выход за верхнюю границу (ValueError)
    @pytest.mark.parametrize("overflow_n", [41, 42, 50, 100, 500, 1000])
    def test_overflow_values_raise_value_error(self, overflow_n: int):
        """Значения свыше 40 должны вызывать ValueError с указанием лимита."""
        with pytest.raises(ValueError) as exc_info:
            compute_fibonacci(overflow_n)
        assert "превышает максимально допустимое значение 40" in str(exc_info.value)
        assert f"получено: {overflow_n}" in str(exc_info.value)

    # Матрица 5: Логические типы bool (TypeError)
    @pytest.mark.parametrize("bool_val", [True, False])
    def test_boolean_values_raise_type_error(self, bool_val: bool):
        """Логические значения True/False должны строго блокироваться как TypeError."""
        with pytest.raises(TypeError) as exc_info:
            compute_fibonacci(bool_val)
        assert "должен быть целым числом (int)" in str(exc_info.value)
        assert "bool" in str(exc_info.value)

    # Матрица 6: Недопустимые типы данных (TypeError)
    @pytest.mark.parametrize("invalid_type_val", [
        0.0, 1.5, 3.14, -0.1,  # Вещественные числа
        "0", "10", "abc", "",  # Строковые представления и мусор
        None,                  # Отсутствие значения
        [5], (5,), {"n": 5}    # Коллекции
    ])
    def test_non_integer_types_raise_type_error(self, invalid_type_val: Any):
        """Нецелочисленные типы данных должны вызывать TypeError."""
        with pytest.raises(TypeError) as exc_info:
            compute_fibonacci(invalid_type_val)
        assert "должен быть целым числом (int)" in str(exc_info.value)


# ============================================================================
# РАЗДЕЛ 6. ТРАССИРОВКА И БЕЛЫЙ ЯЩИК (TestFibonacciTracer)
# ============================================================================

@pytest.mark.whitebox
@pytest.mark.regression
class TestFibonacciTracer:
    """Верификация динамической трассировки и покрытия базовых путей CFG."""

    # Матрица 7: Проверка маршрутов графа CFG
    @pytest.mark.parametrize("n, exp_val, exp_route", [
        (0, 0, "1 -> 2 -> 3 -> 4 -> 5 -> 11"),
        (1, 1, "1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 11"),
        (2, 1, "1 -> 2 -> 3 -> 4 -> 6 -> 8 -> 9 -> 10 -> 9 -> 11"),
        (3, 2, "1 -> 2 -> 3 -> 4 -> 6 -> 8 -> 9 -> 10 -> 9 -> 10 -> 9 -> 11"),
    ])
    def test_cfg_route_matching(self, n: int, exp_val: int, exp_route: str, tracer: CFGTracer):
        """Проверка точного соответствия фактического маршрута CFG теоретическому."""
        val, _ = compute_fibonacci(n, tracer=tracer)
        assert val == exp_val
        assert tracer.format_route() == exp_route

    def test_tracer_attached_to_type_error(self, tracer: CFGTracer):
        """Проверка фиксации маршрута '1 -> 11' при возникновении ошибки типа."""
        with pytest.raises(TypeError) as exc_info:
            compute_fibonacci("invalid", tracer=tracer)
        assert hasattr(exc_info.value, "route")
        assert exc_info.value.route == ["1", "11"]

    def test_tracer_attached_to_value_error_negative(self, tracer: CFGTracer):
        """Проверка фиксации маршрута '1 -> 2 -> 11' при отрицательном числе."""
        with pytest.raises(ValueError) as exc_info:
            compute_fibonacci(-5, tracer=tracer)
        assert hasattr(exc_info.value, "route")
        assert exc_info.value.route == ["1", "2", "11"]

    def test_tracer_attached_to_value_error_overflow(self, tracer: CFGTracer):
        """Проверка фиксации маршрута '1 -> 2 -> 3 -> 11' при переполнении."""
        with pytest.raises(ValueError) as exc_info:
            compute_fibonacci(45, tracer=tracer)
        assert hasattr(exc_info.value, "route")
        assert exc_info.value.route == ["1", "2", "3", "11"]


# ============================================================================
# РАЗДЕЛ 7. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ЯДРА (TestFibonacciAuxiliary)
# ============================================================================

@pytest.mark.regression
class TestFibonacciAuxiliary:
    """Тестирование вспомогательных утилит генерации последовательностей и метаданных."""

    @pytest.mark.parametrize("n, exp_len, exp_last", [
        (0, 1, 0),
        (1, 2, 1),
        (2, 3, 1),
        (5, 6, 5),
        (10, 11, 55),
        (40, 41, 102334155),
    ])
    def test_sequence_generator(self, n: int, exp_len: int, exp_last: int):
        """Проверка функции get_fibonacci_sequence()."""
        seq = get_fibonacci_sequence(n)
        assert len(seq) == exp_len
        assert seq[-1] == exp_last
        assert seq[0] == 0

    def test_sequence_generator_errors(self):
        """Проверка исключений в get_fibonacci_sequence()."""
        with pytest.raises(TypeError):
            get_fibonacci_sequence(3.14)  # type: ignore
        with pytest.raises(ValueError):
            get_fibonacci_sequence(-1)

    @pytest.mark.parametrize("n, exp_val, exp_rank", [
        (0, 0, 1),
        (1, 1, 2),
        (10, 55, 11),
        (40, 102334155, 41),
    ])
    def test_dual_index_info(self, n: int, exp_val: int, exp_rank: int):
        """Проверка метаданных двойной индексации get_dual_index_info()."""
        info = get_dual_index_info(n)
        assert info["n"] == n
        assert info["value"] == exp_val
        assert info["sequence_rank"] == exp_rank
        assert "description" in info

    def test_format_sequence_str(self):
        """Проверка компактного форматирования длинных последовательностей."""
        seq_short = [0, 1, 1, 2, 3]
        assert format_sequence_str(seq_short) == "0, 1, 1, 2, 3"

        seq_long = list(range(20))
        formatted = format_sequence_str(seq_long, max_items=10)
        assert "..." in formatted
        assert "всего 20 элементов" in formatted
