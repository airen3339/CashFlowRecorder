from rsc.utils.clients_functions import add_new_client, modify_client_data, delete_client, change_client_name
from rsc.database import MySession, Client
from sqlalchemy import select, or_
add_new_client("demishu")
modify_client_data("demishu", email='a@.aaa', province='VR')
change_client_name("demishu", "demishuuu")
add_new_client("demishu")
modify_client_data("demishu", email='a@.aaa', province='VR')
with MySession as session:
    stmt = select(Client).where(or_(Client.name=="demishu", Client.name=="demishuuu"))
    client_1, client_2 = tuple(session.scalars(stmt))
    print(client_1)
    print(client_2)

delete_client("demishu")
delete_client("demishuuu")