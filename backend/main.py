from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware 
from starlette.middleware.sessions import SessionMiddleware 
from starlette.requests import Request
import uvicorn 
from routers.auth import router as authrouter
from routers.course import router as courserouter
from dotenv import load_dotenv 
from db import Base, engine, db_dependency
from sqlalchemy.orm import Session
from typing import Annotated
import os
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()


GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID");
FRONTEND_URL = os.getenv("FRONTEND_URL");
SECRET_KEY = os.getenv("SECRET_KEY")

if not GOOGLE_CLIENT_SECRET:
    logging.warning("GOOGLE_CLIENT_SECRET is not set.")
if not GOOGLE_CLIENT_ID:
    logging.warning("GOOGLE_CLIENT_ID is not set.")
if not FRONTEND_URL:
    logging.warning("FRONTEND_URL is not set.")
if not SECRET_KEY:
    logging.warning("SECRET_KEY is not set.")


app = FastAPI() 
origins = [ 
	FRONTEND_URL
] 
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY) 
app.add_middleware( 
	CORSMiddleware, 
	allow_origins=origins, 
	allow_credentials=True, 
	allow_methods=["*"], 
	allow_headers=["*"], 
) 



# Auth route
app.include_router(router=authrouter, prefix="/auth")
# Course route
app.include_router(router=courserouter, prefix="/course")


# NO LONGER NEEDED
@app.post("/setup_db")
def setup_database(db: Session = db_dependency):
    try:
        # Create all tables in the database
        Base.metadata.create_all(bind=engine)
        return {"message": "Database setup completed."}
    except Exception as e:
        logging.error(f"Error setting up database: {e}")
        raise HTTPException(status_code=500, detail="Database setup failed.")
    

if __name__ == "__main__": 
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
