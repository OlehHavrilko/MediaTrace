from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./mediatrace.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class VideoAnalysis(Base):
    __tablename__ = "video_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    video_url = Column(String, index=True)
    video_id = Column(String)
    title = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Storage for results
    metadata_json = Column(JSON)
    vision_results = Column(JSON)
    audio_results = Column(JSON)
    editing_results = Column(JSON)
    potential_sources = Column(JSON)

def init_db():
    Base.metadata.create_all(bind=engine)
