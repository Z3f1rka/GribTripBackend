from datetime import datetime
from typing import List

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship  # noqa

from app.db.database import Base


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=True)
    files: Mapped[List[str]] = mapped_column(postgresql.ARRAY(String), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow())
    to_user: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    from_user: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
