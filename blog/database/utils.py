"""Database util functions"""

from sqlalchemy import Row
import json


def row_to_dict(row: Row) -> dict:
    """Convert row to dict, casting non-JSON-serializable objects as str

    Args:
        row (Row): Sqlalchemy row

    Returns:
        dict
    """
    dictionary = dict(row._mapping)
    for key, value in dictionary.items():
        try:
            json.dumps(value)
        except (TypeError, OverflowError):
            dictionary[key] = str(value)
    return dictionary

