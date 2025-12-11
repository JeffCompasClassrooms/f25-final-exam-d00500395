# Final Exam System Test, written by Ayden Wayman - A7W13

import pytest
from christmas_list import ChristmasList
import os
import tempfile

TEMPLATE_LIST = "empty_christmas_list.pkl"
WORKING_LIST = "christmas_list.pkl"

@pytest.fixture
def temp_file():
    temp_dir = tempfile.mkdtemp()
    filepath = os.path.join(temp_dir, "test_christmas_list.pkl")
    
    yield filepath
    
    if os.path.exists(filepath):
        os.remove(filepath)
    os.rmdir(temp_dir)

@pytest.fixture
def christmas_list(temp_file):
    """Fixture that provides a ChristmasList instance with a temporary file."""
    return ChristmasList(temp_file)

def describe_christmas_list():
    def it_starts_empty(christmas_list):
        items = christmas_list.loadItems()
        assert items == []

    def it_adds_items(christmas_list):
        christmas_list.add("Racecar")
        christmas_list.add("Baseball")
        items = christmas_list.loadItems()
        assert {"name": "Racecar", "purchased": False} in items
        assert {"name": "Baseball", "purchased": False} in items

    def it_checks_off_items(christmas_list):
        christmas_list.add("Puzzle")
        christmas_list.check_off("Puzzle")
        items = christmas_list.loadItems()
        for item in items:
            if item["name"] == "Puzzle":
                assert item["purchased"] is True

    def it_removes_items(christmas_list):
        christmas_list.add("Board Game")
        christmas_list.remove("Board Game")
        items = christmas_list.loadItems()
        assert all(item["name"] != "Board Game" for item in items)

    def it_prints_list(capsys, christmas_list):
        christmas_list.add("Lego Set")
        christmas_list.add("Action Figure")
        christmas_list.check_off("Lego Set")
        items = christmas_list.loadItems()
        christmas_list.print_list()
        captured = capsys.readouterr()
        for item in items:
            if item["purchased"]:
                assert f"[x] {item['name']}" in captured.out
            else:
                assert f"[_] {item['name']}" in captured.out

    def it_handles_nonexistent_item_check_off(christmas_list):
        christmas_list.add("Racecar")
        christmas_list.check_off("Nonexistent Item")
        items = christmas_list.loadItems()
        for item in items:
            if item["name"] == "Racecar":
                assert item["purchased"] is False

    def it_handles_nonexistent_item_removal(christmas_list):
        christmas_list.add("Train Set")
        christmas_list.remove("Nonexistent Item")
        items = christmas_list.loadItems()
        assert any(item["name"] == "Train Set" for item in items)

    def it_saves_data_between_sessions(temp_file):
        cl1 = ChristmasList(temp_file)
        cl1.add("Video Game")
        cl1.check_off("Video Game")
        
        cl2 = ChristmasList(temp_file)
        items = cl2.loadItems()
        assert {"name": "Video Game", "purchased": True} in items

    def it_initializes_file_if_missing(temp_file):
        if os.path.exists(temp_file):
            os.remove(temp_file)
        cl = ChristmasList(temp_file)
        items = cl.loadItems()
        assert items == []

    def it_allows_multiple_items_with_same_name(christmas_list):
        christmas_list.add("Book")
        christmas_list.add("Book")
        items = christmas_list.loadItems()
        assert len([item for item in items if item["name"] == "Book"]) == 2
        christmas_list.check_off("Book")
        items = christmas_list.loadItems()
        assert all(item["purchased"] is True for item in items if item["name"] == "Book")

    def it_removes_all_items_if_duplicates_exist(christmas_list):
        christmas_list.add("Puzzle")
        christmas_list.add("Puzzle")
        christmas_list.remove("Puzzle")
        items = christmas_list.loadItems()
        assert len([item for item in items if item["name"] == "Puzzle"]) == 0

    def it_prints_empty_list(capsys, christmas_list):
        christmas_list.print_list()
        captured = capsys.readouterr()
        assert captured.out == ""

    def it_checks_off_all_items_with_same_name(christmas_list):
        christmas_list.add("Game")
        christmas_list.add("Game")
        christmas_list.check_off("Game")
        items = christmas_list.loadItems()
        assert all(item["purchased"] is True for item in items if item["name"] == "Game")

    def it_removes_only_specified_items(christmas_list):
        christmas_list.add("Baseball")
        christmas_list.add("Racecar")
        christmas_list.remove("Baseball")
        items = christmas_list.loadItems()
        assert all(item["name"] != "Baseball" for item in items)
        assert any(item["name"] == "Racecar" for item in items)