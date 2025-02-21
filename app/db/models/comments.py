from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship  # noqa

from app.db.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[str] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    answer: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="comments")
    route_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("routes.id"))
    routes = relationship("Route", back_populates="comments")