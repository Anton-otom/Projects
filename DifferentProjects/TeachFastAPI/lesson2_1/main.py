from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="public"), name="static")


@app.post("/calculate")
async def calculate(num1: float = Form(...),
                    num2: float = Form(...)):
    result = num1 + num2
    return {"result": result}


@app.get("/")
async def read_root():
    return FileResponse("public/index.html")