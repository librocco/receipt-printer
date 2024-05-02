from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import json


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "An http endpoint to print ESC/POS receipts"


@app.get("/printreceipt")
async def print_label():
    return {"message": f"Use POST instead"}


@app.post("/printreceipt")
async def print_label(request: Request):
    # Get the  book data from bookData POST var
    try:
        recept_data = await request.json()
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=405, detail="Invalid JSON data: %s" % e)

    print("TODO: actual printing to be implemented")

    return {"status": "OK", "message": f"Receipt printed"}


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
