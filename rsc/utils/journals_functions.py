import datetime

from ..database import MySession, Journal, Account, Client, User
from .users_functions import validate_user
from .errors import ValidationError
from sqlalchemy import select, and_, or_
"""1. 记录收入和支出流水账目；
2. 分类管理账目，如餐饮、交通、服饰、旅游等；
3. 支持多种货币单位，如人民币、美元、欧元等；
4. 支持多种账户类型，如现金、银行卡、支付宝、微信等；
5. 统计分析账目，如每月、每季度、每年的收支情况；
6. 支持自定义账目标签，方便查询和筛选；
7. 导出账目数据，支持Excel、CSV等格式；
8. 支持数据备份和恢复，防止数据丢失。"""


def _is_date(date:datetime.datetime|datetime.date|str, format="%Y/%m/%d"):
    if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
        return True
    if isinstance(date, str):
        try:
            datetime.datetime.strptime(date, format)
            return True
        except ValueError:
            return False


def _are_id_valid(id_1, id_2):
    """ if both 2 id are valid, returns True, else False"""
    with MySession as session:
        check_dict = {id_num: Account if id_num<100 else Client for id_num in (id_1,id_2)}
        obj_list = []
        for id_num, Obj in check_dict.items():
            stmt = ""
            if Obj is Account:
                stmt = select(Obj).where(Obj.id == id_num)

            elif Obj is Client:
                stmt = select(Obj).where(Obj.clientId == id_num)
            else:
                raise ValidationError(f"id = {id_num} is not valid.")
            obj_list.append(session.scalar(stmt))
        return all(obj_list)


def add_new_record(date: datetime.datetime, giverId, getterId, amount, user, note=""):
    if _is_date(date) and _are_id_valid(giverId,getterId) and amount:
        if not isinstance(date, datetime.datetime) or not isinstance(date, datetime.date):
            if isinstance(date, str):
                try:
                    date = datetime.datetime.strptime(date, "%Y/%m/%d")
                except ValueError:
                    raise ValueError(f"date = {date} can't be transformed into datetime obj.")

        journal_account = Journal(date=date, giverId=giverId, getterId=getterId, user=user, note=note)
        with MySession as session:
            session.add(journal_account)
            session.commit()
        return True
    else:
        print(f'date={date}, giverId={giverId}, getterId={getterId}, amount={amount}, user={user}, note={note}\
are not valid.')
        return False

# def modify_data