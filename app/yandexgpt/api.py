import aiohttp
from typing import Dict, Any
from typing import NoReturn

import aiohttp.http_exceptions
import aiohttp.web_exceptions

from schemas.tasks import TaskShemaAdd
from yandexgpt._request_params import DEFAULT_HEADERS, DEFAULT_URL, format_task_request_data
from yandexgpt.utils import extract_task_from_yagpt_response
from yandexgpt.exc import TaskExtractError


async def get_task_from_msg(user_msg: str) -> TaskShemaAdd | NoReturn:
    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as session:
        response = await session.post(url=DEFAULT_URL, json=format_task_request_data(user_msg),
                                      ssl=False)
        if response.ok:
            response_json = await response.json()
            msg = __get_msg_from_response_json(response_json)
            task = TaskShemaAdd(**extract_task_from_yagpt_response(msg))
            return task
        raise TaskExtractError(f'Reason: yagpt bad request. Response: {await response.text()}')
    

def __get_msg_from_response_json(response_json: Dict[str, Any]) -> str:
    try:
        return response_json['result']['alternatives'][-1]['message'].get('text', '')
    except KeyError as e:
        print(e)
        return ''
