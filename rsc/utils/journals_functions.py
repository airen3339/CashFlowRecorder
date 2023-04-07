from ..database import MySession, Journal, Client, User
from .errors import ValidationError
"""1. 记录收入和支出流水账目；
2. 分类管理账目，如餐饮、交通、服饰、旅游等；
3. 支持多种货币单位，如人民币、美元、欧元等；
4. 支持多种账户类型，如现金、银行卡、支付宝、微信等；
5. 统计分析账目，如每月、每季度、每年的收支情况；
6. 支持自定义账目标签，方便查询和筛选；
7. 导出账目数据，支持Excel、CSV等格式；
8. 支持数据备份和恢复，防止数据丢失。"""

