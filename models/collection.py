from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.database import Base

# Taula de relació entre Col·leccions i Equips
teams_in_collections = Table(
    "teams_in_collections",
    Base.metadata,
    Column("collection_id", Integer, ForeignKey("collections.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True)
)

# Taula de relació entre Equips i Jugadors
players_in_teams = Table(
    "players_in_teams",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
    Column("player_id", Integer, ForeignKey("players.id"), primary_key=True)
)

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    teams = relationship("Team", secondary=teams_in_collections, back_populates="collections")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String)

    collections = relationship("Collection", secondary=teams_in_collections, back_populates="teams")
    players = relationship("Player", secondary=players_in_teams, back_populates="teams")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    
    teams = relationship("Team", secondary=players_in_teams, back_populates="players")
