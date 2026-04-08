from sqlalchemy import Column, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class VuzopediaProgram(Base):
    __tablename__ = "vuzopedia_program"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    cost = Column(Numeric(10, 2))
    study_type = Column(String(50))
    min_budget_score = Column(Integer)
    min_paid_score = Column(Integer)
    code = Column(String(50))
    sphere = Column(Text)
    career_prospects = Column(Text)
    budget_places = Column(Integer)
    paid_places = Column(Integer)
    url = Column(Text)

    cities = relationship("CityVuzopediaProgram", back_populates="program")


class HseProgram(Base):
    __tablename__ = "hse_program"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    code = Column(String(50))
    cost = Column(Numeric(10, 2))
    study_type = Column(String(50))
    budget_places = Column(Integer)
    paid_places = Column(Integer)
    foreigners_places = Column(Integer)
    url = Column(Text)

    courses = relationship("HseCourse", back_populates="program")


class HseCourse(Base):
    __tablename__ = "hse_course"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("hse_program.id"), nullable=False)
    title = Column(Text, nullable=False)
    year = Column(String(50))
    module = Column(String(50))
    status = Column(String(50))
    content = Column(Text)
    results = Column(Text)
    language = Column(String(50))
    credits = Column(Float)
    url = Column(Text)

    program = relationship("HseProgram", back_populates="courses")


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    programs = relationship("CityVuzopediaProgram", back_populates="city")


class CityVuzopediaProgram(Base):
    __tablename__ = "city_vuzopedia_program"

    city_id = Column(Integer, ForeignKey("city.id"), primary_key=True)
    vuzopedia_program_id = Column(Integer, ForeignKey("vuzopedia_program.id"), primary_key=True)

    city = relationship("City", back_populates="programs")
    program = relationship("VuzopediaProgram", back_populates="cities")
