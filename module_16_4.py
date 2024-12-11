from typing import Annotated, List
from fastapi import FastAPI, Body, HTTPException, status
import uvicorn
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get('/users')
def get_all_users() -> list[User]:
    return users


@app.post('/user/{username}/{age}')
def create_user(user: User, username: str, age: int) -> str:
    user.id = len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return {'id': f'{user.id}', 'username': f'{user.username}', 'age': f'{user.age}'}


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int, username: str, age: int) -> str:
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return 'User update.'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}')
def delete_user(user_id: int):
    try:
        for user in users:
            if user.id == user_id:
                users.remove(user)
                return f'User with {user_id} was deleted.'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


if __name__ == '__main__':
    uvicorn.run(app='module_16_4:app', host="127.0.0.1", port=8000, reload=True)
