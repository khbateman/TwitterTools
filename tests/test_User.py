from TwitterTools import User
import pytest

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

def test_url_init_1():
    user = User.User.from_url("https://twitter.com/johnsmith",
                                following_me = False,
                                following_them = True,
                                protected_account = False)
    assert user.handle == "johnsmith"
    assert user.following_me == False
    assert user.following_them == True
    assert user.protected_account == False


def test_url_init_2():
    user = User.User.from_url("https://twitter.com/johnsmith/",
                                following_me = True,
                                following_them = False,
                                protected_account = True)
    assert user.handle == "johnsmith"
    assert user.following_me == True
    assert user.following_them == False
    assert user.protected_account == True


def test_url_init_3():
    user = User.User.from_url("https://twitter.com/johnsmith/post/12345/something")
    assert user.handle == "johnsmith"

def test_url_init_4():
    # www version
    user = User.User.from_url("https://www.twitter.com/johnsmith/post/12345/something")
    assert user.handle == "johnsmith"

def test_url_init_wrong_url_1():
    with pytest.raises(IndexError):
        user = User.User.from_url("https://google.com/johnsmith")

