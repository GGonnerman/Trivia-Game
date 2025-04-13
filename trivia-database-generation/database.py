from dotenv import load_dotenv
from datetime import date
from typing import Any
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
import os
from custom_schemas import Category, Question, Season, Episode
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)


class Database:
    connection: MySQLConnection
    cursor: MySQLCursor

    def __init__(self, recreate_database: bool = True) -> None:
        load_dotenv()

        MYSQL_USERNAME: str = os.environ.get("MYSQL_USERNAME")
        MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD")
        MYSQL_IP: str = os.environ.get("MYSQL_IP")
        MYSQL_PORT: str = os.environ.get("MYSQL_PORT")

        logger.debug("Setting up sql connection...")

        self.connection = mysql.connector.connect(
            host=MYSQL_IP,
            port=MYSQL_PORT,
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            database="trivia",
            charset="utf8mb4",
        )

        logger.debug("Checking if connected...")

        if not self.connection.is_connected():
            raise ConnectionError("Failed to connect to MySQL database on {MYSQL_USERNAME} @ {MYSQL_IP}:{MYSQL_PORT}")

        logger.debug("Creating cursor...")

        self.cursor = self.connection.cursor()

        logger.debug("Finished setup")

    def purge(self):
        tables = [
            "CustomGame_has_Category",
            "CustomGame",
            "User",
            "Category",
            "Episode",
            "Question",
            "Season",
        ]
        purge_stms = (
            "SET FOREIGN_KEY_CHECKS = 0;",
            *[f"TRUNCATE {table};" for table in tables],
            "SET FOREIGN_KEY_CHECKS = 1;",
        )
        for stm in purge_stms:
            self.cursor.execute(stm, {})
        self.connection.commit()

    def insert_season(self, season: dict[Any, Any]):
        season = Season.validate([season])[0]
        insert_stm = "INSERT INTO Season (season_number) VALUES (%(season_number)s)"

        self.cursor.execute(insert_stm, season)
        self.connection.commit()

    def get_season_id(self, season_number):
        search_stm = "SELECT idSeason FROM Season WHERE season_number = %(season_number)s"
        self.cursor.execute(search_stm, {"season_number": season_number})
        logger.debug(f"Getting the season id number for {season_number}...")
        return self.cursor.fetchone()[0]

    def insert_episodes(self, season_number: int, episodes: list[dict[Any, Any]]):
        season_id = self.get_season_id(season_number)
        episodes = [{**episode, "Season_idSeason": season_id, "episode_number": index + 1} for index, episode in enumerate(episodes)]

        episodes = Episode.validate(episodes)
        logger.debug("Inserting episodes...")
        insert_stm = "INSERT INTO Episode (air_date, Season_idSeason, episode_number) VALUES (%(air_date)s, %(Season_idSeason)s, %(episode_number)s)"

        self.cursor.executemany(insert_stm, episodes)
        self.connection.commit()

    def insert_categories(self, air_date, categories: list[dict[Any, Any]]):
        episode_id = self.get_episode_from_air_date(air_date)
        categories = [{**category, "Episode_idEpisode": episode_id} for category in categories]

        categories = Category.validate(categories)

        logger.debug("Inserting categories...")

        insert_stm = "INSERT INTO Category (name, Episode_idEpisode, round) VALUES (%(name)s, %(Episode_idEpisode)s, %(round)s)"

        self.cursor.executemany(insert_stm, categories)
        self.connection.commit()

    def get_episode_from_air_date(self, air_date: date):
        query_stm = "SELECT idEpisode FROM Episode WHERE air_date = %(air_date)s"
        self.cursor.execute(query_stm, {"air_date": air_date})
        logger.debug(f"Getting the episode id for date {air_date}...")
        return self.cursor.fetchone()[0]

    def insert_questions(self, air_date, round, category_name, questions):
        category_id = self.get_category(air_date, round, category_name)

        insert_stm = "INSERT INTO Question (clue_value, comment, question, answer, Category_idCategory) VALUES (%(clue_value)s, %(comment)s, %(question)s, %(answer)s, %(Category_idCategory)s)"

        questions = [{"comment": "", **question, "Category_idCategory": category_id} for question in questions]
        questions = Question.validate(questions)

        logger.debug("Inserting questions...")

        self.cursor.executemany(insert_stm, questions)
        self.connection.commit()

    def get_category(self, air_date: date, round: int, name: str):
        episode_id = self.get_episode_from_air_date(air_date)
        query_stm = "SELECT idCategory FROM Category WHERE Episode_idEpisode = %(episode_id)s AND round = %(round)s AND name = %(name)s"
        params = {
            "episode_id": episode_id,
            "round": round,
            "name": name,
        }
        self.cursor.execute(query_stm, params)
        return self.cursor.fetchone()[0]

    def close(self) -> None:
        self.connection.close()


if __name__ == "__main__":
    db = Database()
    db.purge()
    for i in range(10, 14):
        db.insert_season(
            {
                "season_number": i,
            }
        )
    db.insert_episodes(
        12,
        [
            {"air_date": date(1984, 9, 10)},
            {"air_date": date(1984, 9, 11)},
            {"air_date": date(1984, 9, 12)},
        ],
    )

    categories = [
        (
            date(1984, 9, 10),
            [
                {"name": "LAKES & RIVERS", "round": 1},
                {"name": "INVENTIONS", "round": 2},
            ],
        ),
        (
            date(1984, 9, 11),
            [
                {"name": "ANIMALS", "round": 1},
            ],
        ),
    ]

    for category in categories:
        db.insert_categories(*category)

    db.insert_questions(
        date(1984, 9, 10),
        1,
        category_name="LAKES & RIVERS",
        questions=[
            {"clue_value": 100, "question": "River mentioned most often in the Bible", "answer": "the Jordan"},
            {"clue_value": 200, "question": "Scottish word for lake", "answer": "loch"},
            {"clue_value": 400, "question": "American river only 33 miles shorter than the Mississippi", "answer": "the Missouri"},
        ],
    )

    db.close()
