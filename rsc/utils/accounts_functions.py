from ..database import Account, MySession
from .users_functions import validate_user
from sqlalchemy import select


def add_new_account(account_name) -> bool:
    with MySession as session:
        stmt = select(Account).where(Account.name == account_name)
        occupied_name_account = session.scalar(stmt)
        if occupied_name_account:
            print(f'account name={account_name} is already used. Try another')
            return False
        else:
            new_account = Account(name=account_name, balance=0)
            session.add(new_account)
            session.commit()
            return True


def change_account_name(old_name, new_name):
    with MySession as session:
        stmt = select(Account).where(Account.name == old_name)
        account = session.scalar(stmt)
        if not account:
            print(f"hasn't found account={old_name}.")
            return False
        stmt = select(Account).where(Account.name == new_name)
        occupied_name_account = session.scalar(stmt)
        if occupied_name_account:
            print(f"account name={new_name} is already occupied, try another.")
            return False
        account.name = new_name
        session.commit()
        return True


def delete_account(account_name, username, password):
    with MySession as session:
        stmt = select(Account).where(Account.name == account_name)
        account = session.scalar(stmt)
        if not account:
            print(f"hasn't found account={account_name}. Plz retry.")
            return False
        if validate_user(username, password):
            session.delete(account)
            session.commit()
