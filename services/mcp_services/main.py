from fastapi import FastAPI


app = FastAPI(title="MCP Services")

@app.get("/")
async def root():
    return {"message": "Welcome to MCP Services!"}