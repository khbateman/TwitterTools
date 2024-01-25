from TwitterTools import crawler, User
from selenium.webdriver.common.by import By
import os



# Note that `get_driver` is a setup function declared in conftest.py that 
# sets up the driver only once to be re-used throughout all these tests
def test_user_crawler_01(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_01_verified_follows-me_following-them_not-protected.html")
    # with open(os.path.join(current_dir, "Testing_Resources/user_01_verified_follows-me_following-them_not-protected.html")) as f:
    #     html = f.readlines()[0]

    # driver = crawler.create_driver()
    # get_driver.get("data:text/html;charset=utf-8," + html)
    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "MarkASchrader",
                            following_me = True,
                            following_them = True,
                            protected_account = False,
                            verified=True)
    
    assert user == expected


def test_user_crawler_02(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_02_verified_follows-me_not-following-them_not-protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "jshaulpanic",
                            following_me = True,
                            following_them = False,
                            protected_account = False,
                            verified=True)
    
    assert user == expected


def test_user_crawler_03(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_03_verified_doesnt-follow-me_following-them_not-protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "OldPantherFan",
                            following_me = False,
                            following_them = True,
                            protected_account = False,
                            verified=True)
    
    assert user == expected


def test_user_crawler_04(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_04_verified_doesnt-follow-me_not-following-them_protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "RyanChauner",
                            following_me = False,
                            following_them = False,
                            protected_account = True,
                            verified=True)
    
    assert user == expected


def test_user_crawler_05(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_05_verified-doesnt-follow-me-not-following-them_not-protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "THerroTrades",
                            following_me = False,
                            following_them = False,
                            protected_account = False,
                            verified=True)
    
    assert user == expected


def test_user_crawler_06(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_06_not-verified_follows-me_following-them_protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "kenansandbox",
                            following_me = True,
                            following_them = True,
                            protected_account = True,
                            verified=False)
    
    assert user == expected

def test_user_crawler_07(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_07_not-verified_follows-me_following-them_not-protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "kevinspellman",
                            following_me = True,
                            following_them = True,
                            protected_account = False,
                            verified=False)
    
    assert user == expected


def test_user_crawler_08(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_08_not-verified_follows-me_not-following-them_protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "iafrahilly",
                            following_me = True,
                            following_them = False,
                            protected_account = True,
                            verified=False)
    
    assert user == expected


def test_user_crawler_09(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_09_not-verified_follows-me_not-following-them_not-protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "vo_superhero",
                            following_me = True,
                            following_them = False,
                            protected_account = False,
                            verified=False)
    
    assert user == expected

def test_user_crawler_10(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_10_not-verified_doesnt-follow-me_following-them_protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "perry772",
                            following_me = False,
                            following_them = True,
                            protected_account = True,
                            verified=False)
    
    assert user == expected

def test_user_crawler_11(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_11_not-verified_doesnt-follow-me_following-them_not-protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "MikeSaurbaugh",
                            following_me = False,
                            following_them = True,
                            protected_account = False,
                            verified=False)
    
    assert user == expected


def test_user_crawler_12(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_12_not-verified_doesnt-follow-me_not-following-them_protected.html")    

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "PattyPartyMode",
                            following_me = False,
                            following_them = False,
                            protected_account = True,
                            verified=False)
    
    assert user == expected
    
def test_user_crawler_13(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_13_not-verified_doesnt-follow-me_not-following-them_not-protected.html")

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "arckp6",
                            following_me = False,
                            following_them = False,
                            protected_account = False,
                            verified=False)
    
    assert user == expected

def test_user_crawler_14(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_14_org_verified.html")

    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "CLTgov",
                            following_me = False,
                            following_them = False,
                            protected_account = False,
                            verified=True)
    
    assert user == expected


def test_user_crawler_15(get_driver):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "Testing_Resources/user_15_user_with_emoji_in_name.html")    
    
    get_driver.get("file://" + file_path)
    div = get_driver.find_element(By.XPATH, "*")
    
    user = crawler.create_user_from_div(div)
    expected = User.User(handle = "comuflauta",
                            following_me = False,
                            following_them = False,
                            protected_account = True,
                            verified=True)
    
    assert user == expected