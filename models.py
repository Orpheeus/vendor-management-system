from sqlalchemy import Column, Integer, String, ForeignKey, Text, Select, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from database import Base

class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_name = Column(String)
    services = Column(String)

    # Relacion con las evaluaciones
    reviews = relationship("Review", back_populates="contractor", lazy="selectin", cascade="all, delete-orphan")

    # LOGICA DEL PROMEDIO GENERAL
    @hybrid_property
    def average_rating(self):
        # Verificacion de reseñas
        if not self.reviews:
            return 0.0
        
        # Suma de los promedios de cada review y divide entre el total de reviews
        total_sum = 0
        for rev in self.reviews: #TODO:Funcion escalable y optimizable, una vez creada la aplicacion implementaremos una casilla/boton para agregar un criterio nuevo para que el usuario lo pueda crear sin necesidad de cambiar/agregar valores manualmente
            criteria = [
                rev.availability,
                rev.coordination,
                rev.cost_effectiveness,
                rev.skill_level,
                rev.reliability
            ]

            total_sum += sum(criteria) / len(criteria)

        return total_sum / len(self.reviews)

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

    # PROMEDIO DE ESTA RESEñA INDIVIDUAL
    def total_rating(self):
        scores = [self.availability,
                  self.coordination,
                  self.cost_effectiveness,
                  self.skill_level,
                  self.reliability]
        valid_scores = [s for s in scores  if s is not None]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0.0

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False) 

