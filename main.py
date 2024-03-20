import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from public.users import user_router
from public.companies import company_router
from datetime import datetime
from public.db import create_tables, index_builder

create_tables()
index_builder()

app = FastAPI()

app.include_router(user_router)
app.include_router(company_router)

@app.on_event("startup")
def startup():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
    
@app.on_event("shutdown")
def shutdown():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: End\n')

@app.get('/', response_class = HTMLResponse)
def index():
    return "<b> hello </b>" 

if __name__ == '__main__':
    uvicorn.run(app, host = "127.0.0.1", port = 8000)