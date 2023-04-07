from ..database import MySession, Client, Journal
from .errors import ValidationError
from sqlalchemy import select, update, or_


def _is_str(string) -> bool:
    """if input is str, returns True, else False"""
    return isinstance(string, str)


def _is_email_valid(email) -> bool:
    """returns True if email is valid, else False"""
    if not ("@" in email and "." in email):
        return False
    return True


def add_new_client(client_name, address="", province="", phone="", email=""):
    """if the client is added to database, returns True, else False"""
    input_check = all(map(_is_str, (client_name, address, province, phone, email)))
    if not input_check:
        raise TypeError(f'client_name={client_name}, address={address}, \
province={province}, phone={phone}, email={email} arent all str, plz check.')
    if email:
        if not _is_email_valid(email):
            raise ValidationError(f"email={email} is not a valid email address.")

    with MySession as session:
        stmt = select(Client).where(Client.name == client_name)
        client = session.scalar(stmt)

        if client:
            print(f'client {client} already exists.')
            return False

        client = Client(name=client_name, address=address, province=province, phone=phone, email=email)
        session.add(client)
        session.commit()


def change_client_name(old_client_name, new_client_name) -> bool:
    with MySession as session:
        stmt = select(Client).where(Client.name == old_client_name)
        client = session.scalar(stmt)
        if not client:
            print(f"hasn't found client={old_client_name}.")
            return False
        stmt = select(Client).where(Client.name == new_client_name)
        occupied_name_client = session.scalar(stmt)

        if occupied_name_client:
            print(f"client name={new_client_name} is already occupied, try another.")
            return False
        client.name = new_client_name
        session.commit()
        return True


def modify_client_data(client_name, address="", province="", phone="", email=""):
    """if modifies are made, returns True, else False"""
    with MySession as session:
        stmt = update(Client).where(Client.name == client_name)
        if _is_email_valid(email):
            stmt = stmt.values(address=address)
        if province:
            stmt = stmt.values(province=province)
        if phone:
            stmt = stmt.values(phone=phone)
        if email:
            stmt = stmt.values(email=email)
        session.execute(stmt)
        session.commit()


def delete_client(client_name: str) -> bool:
    """if client is deleted, returns True, else False"""
    if not _is_str(client_name):
        raise TypeError(f'client_name={client_name} has to be str.')
    with MySession as session:
        stmt = select(Client).where(Client.name == client_name)
        client = session.scalar(stmt)
        if not client:
            print(f"hasn't found client={client_name}, plz retry.")
            return False
        client_id = client.id
        stmt = select(Journal).where(or_(Journal.giverId == client_id,
                                         Journal.giverId == client_id))
        results = session.scalars(stmt)
        results = tuple(results)
        if results:

            print(f"there are valid record\n{results[:5]}, can't delete client = {client}")
            return False

        else:
            session.delete(client)
            session.commit()
            print(f'you deleted client={client}')
            return True
