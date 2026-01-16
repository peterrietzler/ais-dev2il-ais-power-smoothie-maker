from pathlib import Path
from main import get_ingredients
from main import make_smoothie
from unittest.mock import patch


def test_get_ingredients_file_not_exists(tmp_path: Path):
  """get_ingredients returns an empty list of ingredients if the file does not exist"""
  non_existent_file = tmp_path / "non_existent.txt"
  assert get_ingredients(non_existent_file) == []


def test_get_ingredients_empty_file(tmp_path: Path):
  """get_ingredients returns an empty list if the file exists but is empty"""
  empty_file = tmp_path / "empty.txt"
  empty_file.write_text("")
  assert get_ingredients(empty_file) == []


def test_get_ingredients_valid_content(tmp_path: Path):
  """get_ingredients successfully returns ingredients from the file"""
  content = "Apple\n  \nBanana \n  Orange  \n"
  recipe_file = tmp_path / "recipe.txt"
  recipe_file.write_text(content)

  expected = ["Apple", "Banana", "Orange"]
  assert get_ingredients(recipe_file) == expected

def test_make_smoothie(tmp_path: Path):
    """make_smoothie returns the ingredients of the smoothie"""
    recipe_file = tmp_path / "mocked.txt"
    mocked_ingredients = ["Apple", "Banana"]
    with patch("main.get_ingredients", return_value=mocked_ingredients):
        assert make_smoothie(recipe_file) == mocked_ingredients
