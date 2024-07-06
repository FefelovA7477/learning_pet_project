import fastapi
from pydantic import BaseModel
from typing import Annotated, List, Dict
    
app = fastapi.FastAPI()

class TestModel(BaseModel):
    name: str
    id: int


@app.post('/item', response_model=List[TestModel | str])
async def post_item(query: Annotated[str, fastapi.Query(max_length=20)],
             test_obj: TestModel):
    result = [test_obj, query]
    return result

@app.get('/')
async def pong():
    return 'Hello world!'

    
