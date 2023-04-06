from .. import database
from sqlalchemy import select


def validate_user(username: str, password: str) -> bool:
    """return True if username and password are correct, otherwise False."""
    if not (isinstance(username, str) and isinstance(password, str)):
        raise TypeError(f"username={username} and password={password} aren't both string.")

    with database.MySession as session:
        stmt = select(database.User).where(database.User.username == username)
        result = session.scalar(stmt)

        if not result:
            return False

        if len(password) != len(result.password):
            return False
        else:
            for a, b in zip(password, result.password):
                if a != b:  # 避免暴力破解
                    return False
            return True


def register_new_user(username: str, password: str) -> bool:
    """if user is created, returns True, otherwise False"""
    if not (isinstance(username, str) and isinstance(password, str)):
        raise TypeError(f"username={username} and password={password} aren't both string.")
    with database.MySession as session:
        stmt = select(database.User).where(database.User.username == username)
        result = session.scalar(stmt)

        if result:
            return False

        user = database.User(username=username,password=password)
        session.add(user)
        session.commit()
        return True
