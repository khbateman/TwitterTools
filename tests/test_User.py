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

def test_url_no_base_1():
    user = User.User.from_url("/johnsmith/post/12345/something")
    assert user.handle == "johnsmith"

def test_url_no_base_2():
    user = User.User.from_url("/johnsmith/")
    assert user.handle == "johnsmith"

def test_url_no_base_3():
    user = User.User.from_url("/johnsmith")
    assert user.handle == "johnsmith"

def test_equality_01():
    u1 = User.User("abc")
    u2 = User.User("abc")
    assert u1 == u2

def test_equality_02():
    u1 = User.User("abc")
    assert u1 == u1

def test_equality_03():
    u1 = User.User("abc")
    u2 = User.User("abd")
    assert u1 != u2


def test_equality_04():
    u1 = User.User("abc", True, False, False)
    u2 = User.User("abc", True, False, False)
    assert u1 == u2

def test_equality_05():
    u1 = User.User("abc", True, False, False)
    u2 = User.User("abd", True, False, False)
    assert u1 != u2

def test_equality_06():
    u1 = User.User("abc", True, False, False)
    u2 = User.User("abc", False, False, False)
    assert u1 != u2

def test_equality_07():
    u1 = User.User("abc", True, False, False)
    u2 = User.User("abc", True, True, False)
    assert u1 != u2

def test_equality_08():
    u1 = User.User("abc", True, False, False)
    u2 = User.User("abc", True, False, True)
    assert u1 != u2

def test_equality_09():
    u1 = User.User("abc", True, False, False)
    u2 = User.User.from_url("https://twitter.com/abc/", True, False, False)
    assert u1 == u2

def test_equality_10():
    u1 = User.User("abc", False, True, False)
    u2 = User.User.from_url("https://twitter.com/abc", False, True, False)
    assert u1 == u2

def test_equality_11():
    u1 = User.User("abc", False, True, False)
    u2 = User.User.from_url("https://twitter.com/abc/something/123", False, True, False)
    assert u1 == u2

def test_equality_12():
    u1 = User.User("abc", False, True, False)
    u2 = User.User.from_url("https://twitter.com/abc", False, False, False)
    assert u1 != u2

def test_equality_13():
    u1 = User.User("kenan")
    u2 = User.User.from_url("https://twitter.com/kenan")
    assert u1 == u2