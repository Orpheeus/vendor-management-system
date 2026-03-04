from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_name = Column(String)
    services = Column(String)

    # Relacion con las evaluaciones
    reviews = relationship("Review", back_populates="contractor")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    contractor_id = Column(Integer, ForeignKey("contractors.id"))

    # Ratings (1-5)
    availability = Column(Integer)
    coordination = Column(Integer)
    cost_effectiveness = Column(Integer)
    skill_level = Column(Integer)
    reliability = Column(Integer)

    comments = Column(Text)

    contractor = relationship("Contractor", back_populates="reviews")