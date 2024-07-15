from typing import Dict, Any

from core.config import settings


DEFAULT_HEADERS = {
    'Authorization': f'Api-Key {settings.YANDEX_GPT_API_TOKEN}',
    'Content-Type': 'application/json',
    'x-folder-id': f'{settings.YANDEX_GPT_FOLDER_ID}'
}
DEFAULT_URL = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'


def format_task_request_data(text: str) -> Dict[str, Any]:
    msg = 'Верни ответ в формате JSON\n' + text
    request_data = {
        "modelUri": f"gpt://{settings.YANDEX_GPT_CATALOG_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Выдели из этого текста название задачи, краткое описание задачи и сроки выполнения "
                        "в формате YYYY-MM-DDTHH:mm:ss и выведи полученные данные в формате JSON с ключами "
                        "title, description и deadline. В качестве ответа выдай только представление данных в JSON"
            },
            {
                "role": "user",
                "text": text
            }
        ]
    }
    return request_data