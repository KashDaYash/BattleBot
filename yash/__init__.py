from yash.core.bot import Yaara
from yash.core import database

# Set MongoDB collection to 'users'
database.init_db("users")

# Start the bot instance
app = Yaara()
