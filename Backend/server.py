from fastapi import FastAPI
from ImageChecker import ImageChecker
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

image_checker = ImageChecker()
app = FastAPI()

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Image(BaseModel):
    img: str

@app.get("/")
async def root():
    print(f'Got request for root')
    return {"message": "Hello World"}

@app.post("/predict")
async def predict(image: Image):
    data = image_checker.deserialise_image(image.img)
    equation = image_checker.check_image(data)
    try:
        result = str(eval(equation))
    except:
        result = 'NaN'
    return {"equation": equation, "result": result}

# Run with 
# uvicorn server:app --reload