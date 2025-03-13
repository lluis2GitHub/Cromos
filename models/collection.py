from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    # Relació amb la taula Team
    teams = relationship("Team", back_populates="collection", cascade="all, delete-orphan")
    players = relationship("Player", back_populates="collection")  # 🔥 Relació amb Player

