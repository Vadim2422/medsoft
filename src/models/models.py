from sqlalchemy import Column, TIMESTAMP, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship

from src.db import Base






class Reception(Base):
    __tablename__ = "reception"
    id = Column("id", Integer, primary_key=True)
    diagnosis = Column("diagnosis", String(250))
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="receptions")

    registered_at = Column(TIMESTAMP, server_default=func.now())

