from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./chat_history.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    agent = Column(String, nullable=False)
    response = Column(Text, nullable=True)   # ✅ allow NULL
    steps = Column(Text, nullable=True)
    visual = Column(String, nullable=True)
    follow_up = Column(Text, nullable=True)  # ✅ new column
# Create tables
Base.metadata.create_all(bind=engine)
