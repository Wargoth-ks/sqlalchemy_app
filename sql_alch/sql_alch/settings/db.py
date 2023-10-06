import sys
import os

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from secret import config

db_user = config.db_user.get_secret_value()
db_password = config.db_password.get_secret_value()
db_name = config.db_name.get_secret_value()

url = f"postgresql+psycopg2://{db_user}:{db_password}@localhost/{db_name}"
engine = create_engine(url, echo=True)

# engine = create_engine(
#     f"postgresql+psycopg2://{db_user}:{db_password}@localhost/{db_name}", echo=True
# )

# engine = create_engine(
#     f"postgresql+psycopg2://wargoth:123@localhost/post_db", echo=True
# )

DBSession = sessionmaker(bind=engine)
session = DBSession()
