from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey, Table, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()


character_power_association = Table(
    'character_power_association',
    Base.metadata,
    Column('character_id', String, ForeignKey('characters.character_id'), primary_key=True),
    Column('power_id', String, ForeignKey('powers.power_id'), primary_key=True)
)

character_comic_association = Table(
    'character_comic_association',
    Base.metadata,
    Column('character_id', String, ForeignKey('characters.character_id'), primary_key=True),
    Column('comic_id', String, ForeignKey('comics.comic_id'), primary_key=True)
)

class Character(Base):
    __tablename__ = 'characters'
    character_id = Column(String, primary_key=True)
    character_name = Column(String, nullable=False)
    power = relationship('Power', secondary=character_power_association, backref='power_hero')
    comic = relationship('Comic', secondary=character_comic_association, backref='comic_hero')
    ingested = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, onupdate=datetime.now)

    def __repr__(self):
        return '<Character: {}>'.format(self.character_id)

class Power(Base):
    __tablename__ = 'powers'
    power_id = Column(String, primary_key=True)
    power_name = Column(String, nullable=False)
    character = relationship('Character', secondary=character_power_association, backref='powers')

class Comic(Base):
    __tablename__ = 'comics'
    comic_id = Column(String, primary_key=True)
    title = Column(String, nullable=True)
    issue_number = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    character = relationship('Character', secondary=character_comic_association, backref='comics')

class CharacterWiki(Base):
    __tablename__ = 'characters_wiki'
    character_wiki_id = Column(String, primary_key=True)
    name = Column(String)
    eye_color = Column(String)
    race = Column(String)
    hair_color = Column(String)
    publisher = Column(String)
    skin_color = Column(String)
    height = Column(Float)
    weight = Column(Float)
    identity = Column(String)
    status = Column(String)
    appearances = Column(Integer)
    first_appearance = Column(String)
    year = Column(Integer)
    universe = Column(String)
    character_id = Column(String, ForeignKey('characters.character_id'))
    character = relationship("Character", backref="hero_wiki", foreign_keys=[character_id])


class CharacterStat(Base):
    __tablename__ = 'character_stats'
    character_stat_id = Column(String, primary_key=True)
    name = Column(String)
    alignment = Column(String)
    intelligence = Column(Integer)
    strength = Column(Integer)
    speed = Column(Integer)
    durability = Column(Integer)
    power = Column(Integer)
    combat = Column(Integer)
    total = Column(Integer)
    character_id = Column(String, ForeignKey('characters.character_id'))
    character = relationship("Character", backref="hero_stats", foreign_keys=[character_id])

