from sqlalchemy import Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base


class Permission(Base):

    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="permissions")
