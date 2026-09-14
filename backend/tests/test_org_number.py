from __future__ import annotations
import pytest
from app.core.org_number import validate_org_number, format_org_number

@pytest.mark.parametrize("org_num", [
    "923609016", # Equinor ASA
    "985399077", # DNB Bank ASA
    "910244132", # Telenor ASA
    "914778271", # Norsk Hydro ASA
    "990886343", # Aker BP ASA
])
def test_valid_org_numbers(org_num):
    assert validate_org_number(org_num) is True

@pytest.mark.parametrize("org_num", [
    "123456789",
    "923609015",
    "000000000",
])
def test_invalid_org_numbers(org_num):
    assert validate_org_number(org_num) is False

@pytest.mark.parametrize("org_num", [
    "92360901",
    "9236090161",
    "",
])
def test_length_org_numbers(org_num):
    assert validate_org_number(org_num) is False

@pytest.mark.parametrize("org_num", [
    "92360901a",
    "abc",
    None,
])
def test_non_numeric_org_numbers(org_num):
    assert validate_org_number(org_num) is False

@pytest.mark.parametrize("input_num, expected", [
    ("923 609 016", "923609016"),
    ("923-609-016", "923609016"),
    ("  923609016  ", "923609016"),
])
def test_format_org_number(input_num, expected):
    assert format_org_number(input_num) == expected
