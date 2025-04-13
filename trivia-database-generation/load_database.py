from dataclasses import dataclass
from io import TextIOWrapper
import os
from database import Database
from datetime import date
import csv
import logging
from typing import Any

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

DATA_PATH = os.path.join("trivia_dataset", "seasons")

db: Database = Database()


def load_seasons() -> None:
    season_number = 1
    while True:
        file_name: str = f"season{season_number}.tsv"
        file_path: str = os.path.join(DATA_PATH, file_name)
        if not os.path.isfile(file_path):
            break
        load_season(season_number, file_path)
        season_number += 1
        break  # Only load 1 season


def load_season(season_number: int, file_path: str) -> None:
    db.insert_season({"season_number": season_number})
    with open(file_path, "r", encoding="utf-8") as file:
        rows = parse_file(file)
        episodes = extract_episodes(rows)
        db.insert_episodes(season_number, episodes)
        categories = extract_categories(rows)
        insert_categories(categories)
        questions = extract_questions(rows)
        insert_questions(questions)


def parse_file(file: TextIOWrapper) -> list[dict[str, Any]]:
    reader = csv.DictReader(file, delimiter="\t")
    return [
        {
            "round": int(row["round"]),
            "clue_value": int(row["clue_value"]),
            "category": row["category"],
            "comments": row["comments"],
            "answer": row["answer"],
            "question": row["question"],
            "air_date": date.fromisoformat(row["air_date"]),
        }
        for row in reader
    ]


def extract_episodes(lines: list[dict[str, Any]]):
    logging.debug("Extracting episodes...")
    air_dates: list[date] = []
    for line in lines:
        air_date = line["air_date"]
        if air_date in air_dates:
            continue
        air_dates.append(air_date)
    return [{"air_date": air_date} for air_date in air_dates]


@dataclass
class CategoryList:
    date: date
    items: list[dict[str, Any]]

    def append(self, item):
        self.items.append(item)

    def __eq__(self, other):
        if isinstance(other, CategoryList):
            return self.date == other.date
        elif isinstance(other, date):
            return self.date == other
        else:
            return NotImplemented


def extract_categories(lines: list[dict[str, Any]]) -> list[CategoryList]:
    logging.debug("Extracting categories...")
    categories: list[CategoryList] = []
    for line in lines:
        date = line["air_date"]
        if date in categories:
            logger.debug(line["category"])
            logger.debug(categories[categories.index(date)].items)
            if line_to_category(line) in categories[categories.index(date)].items:
                logger.debug("Continuing...")
                continue
            categories[categories.index(date)].append(line_to_category(line))
        else:
            categories.append(CategoryList(date, [line_to_category(line)]))
    return categories


def insert_categories(meta_category_list: list[CategoryList]):
    for categories_list in meta_category_list:
        air_date = categories_list.date
        items = categories_list.items
        db.insert_categories(air_date, items)


def line_to_category(line: dict[str, Any]):
    return {"name": line["category"], "round": line["round"]}


@dataclass
class QuestionList:
    air_date: date
    round: int
    category_name: str
    items: list[dict[str, Any]]

    def __eq__(self, other: tuple[date, int, str]):
        if other[0] == self.air_date and other[1] == self.round and other[2] == self.category_name:
            return True
        return False

    def append(self, item):
        self.items.append(item)


def line_to_question(line: dict[str, Any]):
    return {
        "clue_value": line["clue_value"],
        "comment": line.get("comment", ""),
        "question": line["question"],
        "answer": line["answer"],
    }


def extract_questions(lines: list[dict[str, Any]]):
    logging.debug("Extracting questions...")
    questions: list[QuestionList] = []
    for line in lines:
        date: date = line["air_date"]
        round: int = line["round"]
        category_name: str = line["category"]
        category = (date, round, category_name)
        if (date, round, category) in questions:
            logger.debug(line["answer"])
            logger.debug(questions[questions.index(category)].items)
            if line_to_question(line) in questions[questions.index(category)].items:
                logger.debug("Continuing...")
                continue
            questions[questions.index(category)].append(line_to_question(line))
        else:
            questions.append(QuestionList(date, round, category_name, [line_to_question(line)]))
    return questions


def insert_questions(meta_question_list: list[QuestionList]):
    for question_list in meta_question_list:
        date = question_list.air_date
        round = question_list.round
        category_name = question_list.category_name
        questions = question_list.items
        db.insert_questions(date, round, category_name, questions)


if __name__ == "__main__":
    db.purge()
    load_seasons()
