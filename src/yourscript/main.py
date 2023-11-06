import uvicorn

if __name__ == "__main__":
    uvicorn.run("main.web:app", host="0.0.0.0", reload=True, port=80)
