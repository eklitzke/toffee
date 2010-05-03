import qa
import toffee.db
from toffee.tests.fixtures import *

@qa.testcase()
def basic_create_user(ctx):
    email = random_email() 
    user = toffee.db.Users.new(email, 'foo')
    toffee.db.Users.get_by_email_password(email, 'foo')

@qa.testcase()
def fetch_user_wrong_email(ctx):
    email = random_email() 
    user = toffee.db.Users.new(email, 'foo')
    with qa.expect_raises(toffee.db.NoSuchEmail):
        toffee.db.Users.get_by_email_password(email + 'xxx', 'foo')

@qa.testcase()
def fetch_user_wrong_password(ctx):
    email = random_email() 
    user = toffee.db.Users.new(email, 'foo')
    with qa.expect_raises(toffee.db.BadPassword):
        toffee.db.Users.get_by_email_password(email, 'bar')
