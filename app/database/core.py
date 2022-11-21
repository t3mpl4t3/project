from databases import Database
from sqlalchemy import MetaData

from settings import DATABASE_URL


database = Database( DATABASE_URL )
metadata = MetaData( )