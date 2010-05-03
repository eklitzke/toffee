from toffee.tests.user_tests import *

import sqlalchemy
import toffee.db

engine = sqlalchemy.create_engine('sqlite:///:memory:')
toffee.db.bind_engine(engine)
