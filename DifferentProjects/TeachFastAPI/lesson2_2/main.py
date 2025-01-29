from fastapi import FastAPI
from models.models import User


app = FastAPI()


@app.post("/user")
async def post_user(user: User):
    adult = check_age(user.age)
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": adult
    }


def check_age(age: int) -> bool:
    return age >= 18


if __name__ == "__main__":
    pass
