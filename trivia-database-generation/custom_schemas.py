from datetime import date
from enum import Enum
from schema import Schema, And, Optional


class IntType(Enum):
    U_TINYINT = 0
    U_SMALLINT = 1
    INT = 2
    U_INT = 3


def is_int(type: IntType):
    range_min = 0
    range_max = 0

    match type:
        case IntType.U_TINYINT:
            range_max = 127
        case IntType.U_SMALLINT:
            range_max = 65535
        case IntType.U_INT:
            range_max = 4294967295
        case IntType.INT:
            range_min = -2147483648
            range_max = 2147483647
        case _:
            raise ValueError(f"Invalid int type '{type}'")

    return And(int, lambda x: range_min <= x <= range_max)


Season = Schema(
    [
        {
            Optional("idSeason"): is_int(IntType.U_INT),
            "season_number": is_int(IntType.U_SMALLINT),
        }
    ]
)

Episode = Schema(
    [
        {
            Optional("idEpisode"): is_int(IntType.U_INT),
            "air_date": date,
            "Season_idSeason": is_int(IntType.U_INT),
            Optional("episode_number"): is_int(IntType.U_SMALLINT),
        }
    ]
)

Category = Schema(
    [
        {
            Optional("idCategory"): is_int(IntType.U_INT),
            "name": And(str, lambda x: 3 <= len(x) <= 45),
            "Episode_idEpisode": is_int(IntType.U_INT),
            "round": is_int(IntType.U_TINYINT),
        }
    ]
)

Question = Schema(
    [
        {
            Optional("idQuestion"): is_int(IntType.U_INT),
            "clue_value": is_int(IntType.U_SMALLINT),
            Optional("comment"): And(str, lambda x: 0 <= len(x) <= 250),
            "question": And(str, lambda x: 0 <= len(x) <= 250),
            "answer": And(str, lambda x: 0 <= len(x) <= 500),
            "Category_idCategory": is_int(IntType.U_INT),
        }
    ]
)
