from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from orm.user.luggage import Luggage
from orm.user.user import User


# https://iifx.dev/en/articles/230056541
class Traveller(User):
    __tablename__ = "traveller"
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user: Mapped["User"] = relationship("User")
    passport_verified: Mapped[bool] = mapped_column()
    luggage_items: Mapped[list["Luggage"]] = relationship(
        "Luggage", back_populates="owner", cascade="all, delete-orphan"
    )