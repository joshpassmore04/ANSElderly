from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.user.permission import Permission


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()

    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(default="default")

    permissions: Mapped[list["Permission"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_load": "selectin",
        "polymorphic_identity": "user"
    }

    def add_permission(self, permission: Permission):
        self.permissions.append(permission)

    def remove_permission(self, permission: Permission):
        self.permissions.remove(permission)
