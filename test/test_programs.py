import pytest
from mini.runner import run_from_path

def test_sort():
    assert(run_from_path('test_programs/bubble_sort.mini') == [1, 2, 3, 5, 6, 7])

def test_fib():
    assert(run_from_path('test_programs/fib.mini') == 89)

def test_fact():
    assert(run_from_path('test_programs/fact.mini') == 3628800)
