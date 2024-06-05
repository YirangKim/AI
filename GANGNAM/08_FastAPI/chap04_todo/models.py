from sqlalchemy import Column, Integer, Boolean, Text
from database import Base

class Todo(Base):
    # 테이블 이름 설정
    __tablename__ = 'todos'
    # 컴럼 설정
    id = Column(Integer, primary_key=True)
    task = Column(Text)
    completed = Column(Boolean, default=False)
    
    
