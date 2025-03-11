from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    collection_id = Column(Integer, ForeignKey('collections.id'))

    # Relació amb la taula Collection
    collection = relationship("Collection", back_populates="teams")
