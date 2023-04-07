import hashlib
from .. import database
from sqlalchemy import select


class ValidationError(Exception):
    pass


def _is_username_valid(username: str) -> bool:
    """if username doesn't contain illegal character, returns True, else False."""
    if not isinstance(username, str):
        return False
    if not 5 < len(username) < 19:
        return False
    if username[0].isdigit():
        return False
    illegals = ("'", '"', ";", "--", ",", "!", "~", "@", "$", "%", "^", "/", " ", "_", ">", "<")
    for char in illegals:
        if char in username:
            return False
    return True


def _is_password_valid(password) -> bool:
    """if password contains upper, lower, number, and special char, returns True, else False"""
    if not isinstance(password, str):
        return False
    if not 8 <= len(password) <= 18:
        return False

    has_upper = False
    has_lower = False
    has_number = False
    has_special = False
    for char in password:
        if not has_upper:
            if char.isupper():
                has_upper = True
        if not has_lower:
            if char.islower():
                has_lower = True
        if not has_number:
            if char.isdigit():
                has_number = True
        if not has_special:
            if char in r'''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''':
                has_special = True

        if has_upper and has_lower and has_number and has_special:
            return True


def _hash_password(password) -> str | None:
    """return hashed password"""
    if not isinstance(password, str):
        return
    return hashlib.sha1(password.encode("utf-8")).hexdigest()


def validate_user(username: str, password: str) -> bool:
    """return True if username and password are correct, otherwise False."""
    if not (isinstance(username, str) and isinstance(password, str)):
        raise TypeError(f"username={username} and password={password} aren't both string.")

    with database.MySession as session:
        stmt = select(database.User).where(database.User.username == username)
        result = session.scalar(stmt)

        if not result:
            print(f'username={username} is not registered.')
            return False

        password = _hash_password(password)
        if password != result.password:
            print("password not correct, plz retry.")
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

        if not (_is_username_valid(username) and _is_password_valid(password)):
            raise ValidationError(f"Username={username} and/or password={password} not valid")

        password = _hash_password(password)
        user = database.User(username=username, password=password)
        session.add(user)
        session.commit()
        return True


def delete_user(username: str, password: str):
    if validate_user(username, password):
        with database.MySession as session:
            stmt = select(database.User).where(username == username)
            user = session.scalar(stmt)
            session.delete(user)
            session.commit()
            print(f"user={username} is deleted.")

