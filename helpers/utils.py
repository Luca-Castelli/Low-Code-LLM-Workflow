# utils.py
import json
from typing import Any, List


def save_model_items(model_items: List[Any], file_path: str) -> None:
    try:
        with open(file_path, "w") as file:
            json.dump(
                [item.dict() for item in model_items], file, indent=4, default=str
            )
    except Exception as e:
        print(f"Error saving model items to {file_path}: {e}")
