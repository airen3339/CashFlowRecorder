import datetime
from generic_settings import app_root_path
from sqlalchemy import (create_engine, Integer, String, Float, Boolean)
from sqlalchemy.orm import (DeclarativeBase, declarative_base, Session, Mapped, mapped_column)

year = datetime.datetime.now().year

engine = create_engine('sqlite:///'+f'{app_root_path}\\database\\{year}.db'.replace("//", '/').replace('/', '\\'))


class Base(DeclarativeBase):
    pass


class Accounts(Base):
    __tablename__ = "conti"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)


class Clients(Base):
    __tablename__ = "clienti"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)


class Journal(Base):
    __tablename__ = "conto giornaliero"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    giverId: Mapped[int] = mapped_column(index=True)
    getterId: Mapped[int] = mapped_column(index=True)
    Amount: Mapped[float] = mapped_column(Float(10, 2))
    Note: Mapped[str] = mapped_column(String(100))


class Users(Base):
    __tablename__ = "utenti"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(15))


Base.metadata.create_all(bind=engine)
