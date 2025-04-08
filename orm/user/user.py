from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from orm import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
