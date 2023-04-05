import distanceAndBlinkDetectionModel
import pytest

def test_euclaidean_distance():
    assert distanceAndBlinkDetectionModel.euclaidean_distance((2,5),(4,8)) == 3.605551275463989