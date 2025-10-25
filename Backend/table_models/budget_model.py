from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

# BudgetTable class that tells sqlalchemy what type of table to create
class BudgetTable(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    limit = Column(Float, nullable=False)
    spent = Column(Float, default=0.0)



    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # match the `User` model class name and back_populates value
    user = relationship("User", back_populates="budgets")