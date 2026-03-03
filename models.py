from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_name = Column(String)
    services = Column(String)

    # Promedio segun reviews
    @property
    def average_score(self):
        if not self.reviews:
            return 0.0
        return sum([r.total_rating for r in self.reviews]) / len(self.reviews)
    
    reviews = relationship("Review", back_populates="contractor")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    contractor_id = Column(Integer, ForeignKey("contractors.id"))

    # Ratings
    availability = Column(Integer)
    easy_to_coordinate = Column(Integer)
    lucrative = Column(Integer)
    skilled = Column(Integer)
    no_problems_back_end = Column(Integer)

    comments = Column(Text)

    contractor = relationship("Contractor", back_populates="reviews")