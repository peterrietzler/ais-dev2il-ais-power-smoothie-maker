import time
from pathlib import Path

import pyjokes
from rich.console import Console

from main import get_ingredients
from main import make_smoothie


def test_get_ingredients(tmp_path: Path):
  """get_ingredients returns ingredients from the file"""
  content = "Apple\nBanana\nOrange"
  recipe_file = tmp_path / "my_smoothie.txt"
  recipe_file.write_text(content)

  expected = ["Apple", "Banana", "Orange"]
  assert get_ingredients(recipe_file) == expected


def test_get_ingredients_file_does_not_exists(tmp_path: Path):
  """get_ingredients returns an empty list of ingredients if the file does not exist"""
  non_existent_file = tmp_path / "non_existent.txt"
  assert get_ingredients(non_existent_file) == []


def test_get_ingredients_file_empty(tmp_path: Path):
  """get_ingredients returns an empty list if the file exists but is empty"""
  empty_file = tmp_path / "smoothie_without_ingredients.txt"
  empty_file.write_text("")
  assert get_ingredients(empty_file) == []


def test_make_smoothie_prints_added_ingredients_version_1(tmp_path, capsys):
  """make_smoothie prints all ingredients that were added to the smoothie to the console"""
  recipe_file = tmp_path / "my_smoothie.txt"
  recipe_file.write_text("Apple\nBanana")
  make_smoothie(recipe_file)
  captured = capsys.readouterr()
  assert "Added Apple" in captured.out
  assert "Added Banana" in captured.out


def test_make_smoothie_prints_added_ingredients_version_2(tmp_path):
  """make_smoothie prints all ingredients that were added to the smoothie to the console"""
  recipe_file = tmp_path / "my_smoothie.txt"
  recipe_file.write_text("Apple\nBanana\n")
  from rich.console import Console
  console = Console(record=True)
  make_smoothie(recipe_file, console)
  text_output = console.export_text()
  assert "Added Apple" in text_output
  assert "Added Banana" in text_output


def test_make_smoothie_prints_a_joke(tmp_path, monkeypatch):
  """make_smoothie prints a joke"""

  # Setup
  recipe_file = tmp_path / "my_smoothie.txt"
  recipe_file.write_text("Mango\n")
  # Mocking: Replace pyjokes.get_joke with a lambda that returns a fixed string
  monkeypatch.setattr(pyjokes, "get_joke",
                      lambda: "A mock walks into a bar. The bartender asks, 'What can I get you?' The mock returns None.")
  # Mocking: Make the test fast
  monkeypatch.setattr(time, "sleep",
                      lambda x: None)

  # When
  console = Console(record=True)
  make_smoothie(recipe_file, console)

  # Then
  output = console.export_text()
  assert "The mock returns None" in output
