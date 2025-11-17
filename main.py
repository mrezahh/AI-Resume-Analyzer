from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"} 
    
# check the git