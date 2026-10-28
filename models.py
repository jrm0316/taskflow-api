from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    tasks: Mapped[list[Task]] = relationship(back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "priority >= 0 AND priority <= 2",
            name="ck_tasks_priority_range"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(back_populates="tasks")
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    completed: Mapped[bool] = mapped_column()
    priority: Mapped[int] = mapped_column()

