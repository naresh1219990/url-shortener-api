# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import shortuuid
from starlette.responses import RedirectResponse

# Database configuration
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# URL model
class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)

# Pydantic model for request
class URLInput(BaseModel):
    url: str

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorten")
def shorten_url(url_input: URLInput, db: Session = Depends(get_db)):
    # Generate a short code
    short_code = shortuuid.uuid()[:8]
    
    # Create a new URL object
    db_url = URL(original_url=url_input.url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    # Construct the shortened URL
    shortened_url = f"http://localhost:8000/{short_code}"
    
    return {"shortened_url": shortened_url}

@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    # Query the database for the original URL
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url=db_url.original_url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
