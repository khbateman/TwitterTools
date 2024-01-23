import test_crawler
from TwitterTools import User

def create_User_1():
    return User.User(handle = "kenanbateman", 
                following_me = True,
                following_them = True,
                protected_account = True)

def test_handle():
    user = create_User_1()
    assert user.handle == "kenanbateman"


def test_url():
    user = create_User_1()
    assert user.url == "https://twitter.com/kenanbateman"

def test_following_me():
    user = create_User_1()
    assert user.following_me == True

def test_following_them():
    user = create_User_1()
    assert user.following_them == True

def test_protected():
    user = create_User_1()
    assert user.protected_account == True