import datetime
import re
import json
from typing import Dict, NoReturn

from yandexgpt.exc import TaskExtractError


def extract_task_from_yagpt_response(response_text: str) -> Dict[str, str | datetime.datetime] | NoReturn:
    json_pattern = r'\{(?:[^{}]|\{[^{}]*\})*\}'
    json_match = re.search(json_pattern, response_text)
    if json_match:
        json_string = json_match.group(0)
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError:
            pass
    raise TaskExtractError(f'Reason: cant extract task from response, response: {response_text}')
