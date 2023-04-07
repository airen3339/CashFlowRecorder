import datetime
from typing_extensions import Annotated
from .generic_settings import app_root_path
from sqlalchemy import (create_engine, String, Float, ForeignKey, func)
from sqlalchemy.orm import (DeclarativeBase, Session, Mapped, mapped_column)

year = datetime.datetime.now().year

engine = create_engine('sqlite:///'+f'{app_root_path}\\database\\{year}.db',
                       connect_args={"check_same_thread": False}, echo=True)


timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "bank accounts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    balance: Mapped[float] = mapped_column(Float(10, 2))

    def __repr__(self):
        return f"{self.__tablename__}(id={self.id}, name={self.name}, balance={self.balance})"


class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    address: Mapped[str] = mapped_column(String(50))
    province: Mapped[str] = mapped_column(String(10), index=True)
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(20))

    def __repr__(self):
        return f"{self.__tablename__}(id={self.id}, name={self.name}, province={self.province})"


class Journal(Base):
    __tablename__ = "journal account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[timestamp] = mapped_column(server_default=func.UTC_TIMESTAMP(), index=True)
    giverId: Mapped[int] = mapped_column(index=True)
    getterId: Mapped[int] = mapped_column(index=True)
    amount: Mapped[float] = mapped_column(Float(10, 2))
    note: Mapped[str] = mapped_column(String(100))
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)

    def __repr__(self):
        return f"{self.__tablename__}(id={self.id}, date={self.date}, giverId={self.giverId}, \
getterId={self.getterId}, amount={self.amount}, note={self.note}, userId={self.userId})"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(40))

    def __repr__(self):
        return f"{self.__tablename__}(id={self.id}, username={self.username}, password={self.password})"


Base.metadata.create_all(bind=engine)

MySession = Session(engine)
