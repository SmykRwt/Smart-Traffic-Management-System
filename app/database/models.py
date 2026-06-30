from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class Analytics(Base):

    __tablename__ = "analytics"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    current_vehicle_count: Mapped[int] = mapped_column(
        Integer
    )

    unique_vehicle_count: Mapped[int] = mapped_column(
        Integer
    )

    traffic_density: Mapped[str] = mapped_column(
        String(30)
    )

    congestion_level: Mapped[str] = mapped_column(
        String(30)
    )