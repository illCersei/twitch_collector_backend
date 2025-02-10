from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    game_id = Column(Integer, primary_key=True, autoincrement=True)
    game_name = Column(String, nullable=False)

    viewers = relationship("Viewer", back_populates="game")


class Viewer(Base):
    __tablename__ = "viewer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)
    date_time = Column(DateTime, nullable=False)
    viewers = Column(Integer, nullable=False)

    game = relationship("Game", back_populates="viewers")
