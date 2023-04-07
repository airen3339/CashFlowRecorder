from rsc.utils.accounts_functions import add_new_client, modify_client_data, delete_client, change_client_name
add_new_client("demishu")
modify_client_data("demishu", email='aaaa', province='VR')
change_client_name("demishu", "demishuuu")

delete_client('demishuuu')
