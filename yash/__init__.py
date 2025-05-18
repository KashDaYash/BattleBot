# Sample content for __init__.py
from yash.core.bot import Yaara
from yash.core.database import DynamicDB

user_db = DynamicDB("users.db")
app = Yaara()

