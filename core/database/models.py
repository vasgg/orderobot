from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey, String, func

review = Annotated[str | None, mapped_column(String(2083))]
user_id_fk = Annotated[
    int, mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
]
order_id_fk = Annotated[
    int, mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
]


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )


class User(Base):
    __tablename__ = "users"
    telegram_id = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str | None] = mapped_column(String(32))
    fullname: Mapped[str]
    balance: Mapped[int] = mapped_column(default=0)
    freelance_rating: Mapped[float | None]
    customer_rating: Mapped[float | None]


class Order(Base):
    __tablename__ = "orders"
    customer_id: Mapped[user_id_fk]
    name: Mapped[str] = mapped_column(default='Безымянный заказ')
    status: Mapped[str] = mapped_column(default='draft')
    budget: Mapped[str] = mapped_column(default='0')
    description: Mapped[str] = mapped_column(String(2083), default='—')
    link: Mapped[str | None] = mapped_column(String(2083), default='—')
    worker_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


class Dialog(Base):
    __tablename__ = "dialogs"
    applcation_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False
    )


class Message(Base):
    __tablename__ = "messages"
    dialog_id: Mapped[int] = mapped_column(
        ForeignKey("dialogs.id", ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(2083))


class Ticket(Base):
    __tablename__ = "tickets"
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    worker_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(2083))


class Review(Base):
    __tablename__ = "reviews"
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    customer_review: Mapped[review]
    worker_review: Mapped[review]
    customer_rating: Mapped[float | None]
    worker_rating: Mapped[float | None]


class Application(Base):
    __tablename__ = "applications"
    order_id: Mapped[order_id_fk]
    freelancer_id: Mapped[user_id_fk]
