from .. import database
from sqlalchemy import select, update, or_


def _is_str(string) -> bool:
    """if input is str, returns True, else False"""
    return isinstance(string, str)


def _is_email_valid(email) -> bool:
    """returns True if email is valid, else False"""
    if not ("@" in email and "." in email):
        print('invalid email address')
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
            pass    # todo

    with database.MySession as session:
        stmt = select(database.Client).where(database.Client.name == client_name)
        client = session.scalar(stmt)

        if client:
            print(f'client {client} already exists.')
            return False

        client = database.Client(name=client_name, address=address, province=province, phone=phone, email=email)
        session.add(client)
        session.commit()


def change_client_name(old_client_name, new_client_name) -> bool:
    with database.MySession as session:
        stmt = select(database.Client).where(database.Client.name == old_client_name)
        client = session.scalar(stmt)
        if not client:
            print(f"hasn't found client={old_client_name}.")
            return False
        stmt = select(database.Client).where(database.Client.name == new_client_name)
        occupied_name_client = session.scalar(stmt)

        if occupied_name_client:
            print(f"client name={new_client_name} is already occupied, try another.")
            return False
        client.name = new_client_name
        session.commit()
        return True


def modify_client_data(client_name, address="", province="", phone="", email="") -> bool:
    """if modifies are made, returns True, else False"""
    with database.MySession as session:
        stmt = update(database.Client).where(database.Client.name == client_name)
        if address:
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
    with database.MySession as session:
        stmt = select(database.Client).where(database.Client.name == client_name)
        client = session.scalar(stmt)
        if not client:
            print(f"hasn't found client={client_name}, plz retry.")
            return False
        client_id = client.id
        stmt = select(database.Journal).where(or_(database.Journal.giverId == client_id,
                                                  database.Journal.giverId == client_id))
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
