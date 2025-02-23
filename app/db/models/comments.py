from datetime import datetime, timezone

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship  # noqa

from app.db.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[str] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow())
    answer: Mapped[bool] = mapped_column(Boolean, default=False)
    type: Mapped[str] = mapped_column(String, default='public')
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="comments")
    route_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("routes.id", ondelete="CASCADE"))
    route = relationship("Route", back_populates="comments")
