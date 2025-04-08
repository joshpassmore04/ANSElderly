from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.airport.gate import Gate


class Flight(Base):

    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(primary_key=True)

    gate_id: Mapped[int] = mapped_column(ForeignKey("gate.id"), nullable=False)
    gate: Mapped["Gate"] = relationship("Gate")