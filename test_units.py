import dbe_test
import pytest

def test_euclaidean_distance():
    assert dbe_test.euclaidean_distance((2,5),(4,8)) == 3.605551275463989


def test_focal_length():
    assert dbe_test.focal_length(6,5) == 30
    assert dbe_test.focal_length(23,5)==115


def test_distance_measure():
    assert dbe_test.distance_measure(8,2) == 4
    assert dbe_test.distance_measure(9, 2) == 4.5



