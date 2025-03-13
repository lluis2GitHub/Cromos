from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    position = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=False)  # 🔹 Nou camp

    # Relació amb Team
    team = relationship("Team", back_populates="players")

    # Relació amb Collection (si cal)
    collection = relationship("Collection", back_populates="players")

