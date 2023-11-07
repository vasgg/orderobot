from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str | None] = mapped_column(String(32))
    fullname: Mapped[str]
    balance: Mapped[int] = mapped_column(default=0)
    freelance_rating: Mapped[float | None]
    customer_rating: Mapped[float | None]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)


class Order(Base):
    __tablename__ = "orders"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(default='Безымянный заказ')
    status: Mapped[str] = mapped_column(default='draft')
    budget: Mapped[str] = mapped_column(default='0')
    description: Mapped[str] = mapped_column(String(2083), default='—')
    link: Mapped[str | None] = mapped_column(String(2083), default='—')
    worker_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    customer: Mapped["User"] = relationship(
        "User", foreign_keys=customer_id, backref="orders_as_customer", lazy=False
    )
    worker: Mapped["User"] = relationship(
        "User", foreign_keys=worker_id, backref="orders_as_worker", lazy=False
    )


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint('order_id', 'freelancer_id'),
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    freelancer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    fee: Mapped[int | None] = mapped_column()
    completion_days: Mapped[int | None] = mapped_column()
    message: Mapped[str | None] = mapped_column(String(2083))

    order: Mapped["Order"] = relationship(
        "Order", foreign_keys=[order_id], backref="applications", lazy=False
    )
    freelancer: Mapped["User"] = relationship(
        'User', foreign_keys=[freelancer_id], backref="applications", lazy=False
    )
