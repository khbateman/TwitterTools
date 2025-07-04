from TwitterTools import crawler, User
from selenium.webdriver.common.by import By
import os
from datetime import datetime, timedelta
from math import floor



def create_time_html_string(days_before_now):
    '''
    Helper method for `create_test_tweets_page_html_with_relative_times`
    
    Creates string in the following format for html page
    ----
    `2024-01-26T21:13:24.000Z">55s`
    '''

    shift = timedelta(days = days_before_now)
    shifted_time = datetime.now() - shift

    if days_before_now < 1:
        if shift.seconds < 60:
            display_text = str(shift.seconds) + "s"
        elif shift.seconds < 3600:
            display_text = str(shift.seconds // 60) + "m"
        else:
            display_text = str(shift.seconds // 3600) + "h"
    elif shifted_time.year == datetime.now().year:
        display_text = datetime.strftime(shifted_time, "%b %-d")
    else:
        display_text = datetime.strftime(shifted_time, "%b %-d, %Y")

    return datetime.strftime(shifted_time, "%Y-%m-%dT%H:%M:%S.000Z") + '">' + display_text


def create_test_tweets_page_html_with_relative_times(tweet1_days_since, tweet2_days_since, tweet3_days_since, tweet4_days_since, tweet5_days_since, tweet6_days_since, file_name = "test_tweets_page_tmp.html"):
    '''
    Creates a duplicate of page test/Testing_Resources/test_tweets_page.html
    with dynamic times to aid in specific test cases below
    '''
    # tweet_1_date_string = '''2024-01-26T21:13:24.000Z">55s'''
    # tweet_2_date_string = '''2024-01-26T18:45:45.000Z">2h'''
    # tweet_3_date_string = '''2024-01-26T18:46:11.000Z">2h'''
    # tweet_4_date_string = '''2024-01-26T17:23:40.000Z">3h'''
    # tweet_5_date_string = '''2024-01-26T14:26:30.000Z">6h'''
    # tweet_6_date_string = '''2024-01-26T14:15:00.000Z">7h'''

    tweet_1_date_string = create_time_html_string(tweet1_days_since)
    tweet_2_date_string = create_time_html_string(tweet2_days_since)
    tweet_3_date_string = create_time_html_string(tweet3_days_since)
    tweet_4_date_string = create_time_html_string(tweet4_days_since)
    tweet_5_date_string = create_time_html_string(tweet5_days_since)
    tweet_6_date_string = create_time_html_string(tweet6_days_since)

    full_html = ""
    current_dir = os.path.dirname(__file__)
    full_html += "".join(open(os.path.join(current_dir, "Testing_Resources/test_tweets_page_p1.txt")).readlines())
    full_html += tweet_1_date_string

    full_html += "".join(open(os.path.join(current_dir, "Testing_Resources/test_tweets_page_p2.txt")).readlines())
    full_html += tweet_2_date_string

    full_html += "".join(open(os.path.join(current_dir, "Testing_Resources/test_tweets_page_p3.txt")).readlines())
    full_html += tweet_3_date_string

    full_html += "".join(open(os.path.join(current_dir, "Testing_Resources/test_tweets_page_p4.txt")).readlines())
    full_html += tweet_4_date_string

    full_html += "".join(open(os.path.join(current_dir, "Testing_Resources/test_tweets_page_p5.txt")).readlines())
    full_html += tweet_5_date_string

    full_html += "".join(open(os.path.join(current_dir, "Testing_Resources/test_tweets_page_p6.txt")).readlines())
    full_html += tweet_6_date_string

    full_html += "".join(open(os.path.join(current_dir, "Testing_Resources/test_tweets_page_p7.txt")).readlines())

    with open(os.path.join(current_dir, "Testing_Resources/", file_name), "w") as f:
        f.write(full_html)



# Grouping these in classes since the driver slows down over repeated tests
# and grouping it by classes allows the driver's scope to be set to the class
# level, and have it recreated for each group
class TestCrawlerSingleUsers():
    # Note that `get_driver` is a setup function declared in conftest.py that 
    # sets up the driver only once to be re-used throughout all these tests
    def test_user_crawler_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_01_verified_follows-me_following-them_not-protected.html")
        # with open(os.path.join(current_dir, "Testing_Resources/user_01_verified_follows-me_following-them_not-protected.html")) as f:
        #     html = f.readlines()[0]

        # driver = crawler.create_driver()
        # get_driver.get("data:text/html;charset=utf-8," + html)
        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        # div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "MarkASchrader",
                                following_me = True,
                                following_them = True,
                                protected_account = False,
                                verified=True)
        
        assert user == expected


    def test_user_crawler_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_02_verified_follows-me_not-following-them_not-protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "jshaulpanic",
                                following_me = True,
                                following_them = False,
                                protected_account = False,
                                verified=True)
        
        assert user == expected


    def test_user_crawler_03(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_03_verified_doesnt-follow-me_following-them_not-protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "OldPantherFan",
                                following_me = False,
                                following_them = True,
                                protected_account = False,
                                verified=True)
        
        assert user == expected


    def test_user_crawler_04(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_04_verified_doesnt-follow-me_not-following-them_protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "RyanChauner",
                                following_me = False,
                                following_them = False,
                                protected_account = True,
                                verified=True)
        
        assert user == expected


    def test_user_crawler_05(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_05_verified-doesnt-follow-me-not-following-them_not-protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "THerroTrades",
                                following_me = False,
                                following_them = False,
                                protected_account = False,
                                verified=True)
        
        assert user == expected


    def test_user_crawler_06(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_06_not-verified_follows-me_following-them_protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "kenansandbox",
                                following_me = True,
                                following_them = True,
                                protected_account = True,
                                verified=False)
        
        assert user == expected

    def test_user_crawler_07(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_07_not-verified_follows-me_following-them_not-protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "kevinspellman",
                                following_me = True,
                                following_them = True,
                                protected_account = False,
                                verified=False)
        
        assert user == expected


    def test_user_crawler_08(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_08_not-verified_follows-me_not-following-them_protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "iafrahilly",
                                following_me = True,
                                following_them = False,
                                protected_account = True,
                                verified=False)
        
        assert user == expected


    def test_user_crawler_09(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_09_not-verified_follows-me_not-following-them_not-protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "vo_superhero",
                                following_me = True,
                                following_them = False,
                                protected_account = False,
                                verified=False)
        
        assert user == expected

    def test_user_crawler_10(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_10_not-verified_doesnt-follow-me_following-them_protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "perry772",
                                following_me = False,
                                following_them = True,
                                protected_account = True,
                                verified=False)
        
        assert user == expected

    def test_user_crawler_11(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_11_not-verified_doesnt-follow-me_following-them_not-protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "MikeSaurbaugh",
                                following_me = False,
                                following_them = True,
                                protected_account = False,
                                verified=False)
        
        assert user == expected


    def test_user_crawler_12(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_12_not-verified_doesnt-follow-me_not-following-them_protected.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "PattyPartyMode",
                                following_me = False,
                                following_them = False,
                                protected_account = True,
                                verified=False)
        
        assert user == expected
        
    def test_user_crawler_13(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_13_not-verified_doesnt-follow-me_not-following-them_not-protected.html")

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "arckp6",
                                following_me = False,
                                following_them = False,
                                protected_account = False,
                                verified=False)
        
        assert user == expected

    def test_user_crawler_14(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_14_org_verified.html")

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "CLTgov",
                                following_me = False,
                                following_them = False,
                                protected_account = False,
                                verified=True)
        
        assert user == expected


    def test_user_crawler_15(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_15_user_with_emoji_in_name.html")    
        
        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "comuflauta",
                                following_me = False,
                                following_them = False,
                                protected_account = True,
                                verified=True)
        
        assert user == expected
    

    def test_user_crawler_16(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_from_search_01.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "Charlottegshore",
                                following_me = False,
                                following_them = False,
                                protected_account = False,
                                verified=True)
        
        assert user == expected
    
    def test_user_crawler_17(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_from_search_02.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "theobserver",
                                following_me = False,
                                following_them = True,
                                protected_account = False,
                                verified=False)
        
        assert user == expected
    
    def test_user_crawler_18(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_from_search_03.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div)
        expected = User.User(handle = "kevinspellman",
                                following_me = True,
                                following_them = True,
                                protected_account = False,
                                verified=False)
        
        assert user == expected
    

    def test_user_crawler_19(self, get_driver):
        # See if alternate XPATHs work for quote posts
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_from_post_quote_01.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div, quote_post = True)
        expected = User.User(handle = "MatiasDonovan",
                                following_me = False,
                                following_them = False,
                                protected_account = False,
                                verified=False)
        
        assert user == expected

    def test_user_crawler_20(self, get_driver):
        # See if alternate XPATHs work for quote posts (verified account)
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_from_post_quote_02_verified.html")    

        get_driver.get("file://" + file_path)
        div = get_driver.find_element(By.XPATH, "/html/body/div")
        
        user = crawler.create_user_from_div(div, quote_post = True)
        expected = User.User(handle = "Sentdex",
                                following_me = False,
                                following_them = False,
                                protected_account = False,
                                verified=True)
        
        assert user == expected


class TestCrawlerUserPage():
    def test_get_all_user_divs_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/following_scroll_1.html")

        get_driver.get("file://" + file_path)

        all_user_divs = crawler.get_all_user_divs(get_driver)

        assert len(all_user_divs) == 19


    def test_get_all_user_divs_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/following_scroll_2.html")

        get_driver.get("file://" + file_path)

        all_user_divs = crawler.get_all_user_divs(get_driver)

        assert len(all_user_divs) == 32


    def test_get_all_user_divs_03(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_01_verified_follows-me_following-them_not-protected.html")

        get_driver.get("file://" + file_path)

        all_user_divs = crawler.get_all_user_divs(get_driver)

        # Should fail
        assert len(all_user_divs) == 0



    def test_scrape_single_follow_page_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/following_scroll_1.html")

        users, urls = crawler.scrape_single_follow_page(get_driver, "file://" + file_path, sleep_after_loading = 0, sleep_after_scrolling = 0)

        assert len(users) == 19
        assert len(urls) == 19

        # Since it scrapes back to front, to get the ones from the top, using negative indexing
        test_user_1 = users[-1]
        test_url_1 = urls[-1]
        assert test_user_1.handle == "Sentdex"
        assert test_user_1.url == test_url_1
        assert test_user_1.following_me == False
        assert test_user_1.following_them == True
        assert test_user_1.protected_account == False
        assert test_user_1.verified == True

        test_user_2 = users[-2]
        test_url_2 = urls[-2]
        assert test_user_2.handle == "kenansandbox"
        assert test_user_2.url == test_url_2
        assert test_user_2.following_me == True
        assert test_user_2.following_them == True
        assert test_user_2.protected_account == True
        assert test_user_2.verified == False

        test_user_3 = users[-11]
        test_url_3 = urls[-11]
        assert test_user_3.handle == "cybertruck"
        assert test_user_3.url == test_url_3
        assert test_user_3.following_me == False
        assert test_user_3.following_them == True
        assert test_user_3.protected_account == False
        assert test_user_3.verified == True




    def test_scrape_single_follow_page_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/following_scroll_2.html")

        users, urls = crawler.scrape_single_follow_page(get_driver, "file://" + file_path, sleep_after_loading = 0, sleep_after_scrolling = 0)

        assert len(users) == 32
        assert len(urls) == 32
    

    def test_get_all_user_divs_search_page_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/search_results_01.html")

        get_driver.get("file://" + file_path)

        all_user_divs = crawler.get_all_user_divs_from_search(get_driver)

        assert len(all_user_divs) == 17


    def test_get_all_user_divs_search_page_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/search_results_01_scrolled.html")

        get_driver.get("file://" + file_path)

        all_user_divs = crawler.get_all_user_divs_from_search(get_driver)

        assert len(all_user_divs) == 28


    def test_get_all_user_divs_search_page_03(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/search_results_02_empty.html")

        get_driver.get("file://" + file_path)

        all_user_divs = crawler.get_all_user_divs_from_search(get_driver)

        assert len(all_user_divs) == 0


    def test_get_all_user_divs_search_page_04(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_search_failure.html")

        get_driver.get("file://" + file_path)

        all_user_divs = crawler.get_all_user_divs_from_search(get_driver)

        assert len(all_user_divs) == 0


class TestTimeSinceRecentActivitySinglePage():
    def test_get_time_lapsed_since_most_recent_activity_single_page_01(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 0.0005, 
                                                    tweet2_days_since = 0.005, 
                                                    tweet3_days_since = 0.5, 
                                                    tweet4_days_since = 20, 
                                                    tweet5_days_since = 365, 
                                                    tweet6_days_since = 400)
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path,
                                                sleep_after_loading = 0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 0.0005)) < timedelta(seconds=10)


    def test_get_time_lapsed_since_most_recent_activity_single_page_02(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 0.004, 
                                                    tweet2_days_since = 0.005, 
                                                    tweet3_days_since = 0.5, 
                                                    tweet4_days_since = 20, 
                                                    tweet5_days_since = 365, 
                                                    tweet6_days_since = 400)
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path,
                                                sleep_after_loading = 0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 0.004)) < timedelta(seconds=10)


    def test_get_time_lapsed_since_most_recent_activity_single_page_03(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 0.3, 
                                                    tweet2_days_since = 0.4, 
                                                    tweet3_days_since = 0.5, 
                                                    tweet4_days_since = 20, 
                                                    tweet5_days_since = 365, 
                                                    tweet6_days_since = 400)
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path,
                                                sleep_after_loading = 0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 0.3)) < timedelta(seconds=10)


    def test_get_time_lapsed_since_most_recent_activity_single_page_04(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 0.039, 
                                                    tweet2_days_since = 0.04, 
                                                    tweet3_days_since = 0.5, 
                                                    tweet4_days_since = 20, 
                                                    tweet5_days_since = 365, 
                                                    tweet6_days_since = 400)
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path,
                                                sleep_after_loading = 0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 0.039)) < timedelta(seconds=10)

    def test_get_time_lapsed_since_most_recent_activity_single_page_05(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 0.900, 
                                                    tweet2_days_since = 901, 
                                                    tweet3_days_since = 902, 
                                                    tweet4_days_since = 903, 
                                                    tweet5_days_since = 904, 
                                                    tweet6_days_since = 905)
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path,
                                                sleep_after_loading = 0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 900)) < timedelta(seconds=10)


    def test_get_time_lapsed_since_most_recent_activity_single_page_06(self, get_driver):
        # Simulating pinned tweets where early tweets aren't necessarily newest
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 500, 
                                                    tweet2_days_since = 650, 
                                                    tweet3_days_since = 3, 
                                                    tweet4_days_since = 10, 
                                                    tweet5_days_since = 15, 
                                                    tweet6_days_since = 18)
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path,
                                                sleep_after_loading = 0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 3)) < timedelta(seconds=10)

    def test_get_time_lapsed_since_most_recent_activity_single_page_07(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 0.900, 
                                                    tweet2_days_since = 901, 
                                                    tweet3_days_since = 902, 
                                                    tweet4_days_since = 903, 
                                                    tweet5_days_since = 904, 
                                                    tweet6_days_since = 905)
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path,
                                                sleep_after_loading = 0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 900)) < timedelta(seconds=10)




    def test_get_time_lapsed_since_most_recent_activity_single_page_08(self, get_driver):
        # Simulating where the lowest answer won't be returned if early tweet
        # meets threshold for efficiency
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 6, 
                                                    tweet2_days_since = 7, 
                                                    tweet3_days_since = 8, 
                                                    tweet4_days_since = 9, 
                                                    tweet5_days_since = 10, 
                                                    tweet6_days_since = 1, # this shouldn't be found
                                                    file_name = "test_tweets_page_tmp.html")
        
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path,
                                                stop_checking_after_days_threshold_met=7,
                                                sleep_after_loading = 0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 6)) < timedelta(seconds=10)



    def test_get_time_lapsed_since_most_recent_activity_single_page_09(self, get_driver):
        # Simulating efficient timing where finding early tweet that meets threshold exits
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 6, # should exit here
                                                    tweet2_days_since = 650, 
                                                    tweet3_days_since = 3, 
                                                    tweet4_days_since = 10, 
                                                    tweet5_days_since = 15, 
                                                    tweet6_days_since = 1,
                                                    file_name = "test_tweets_page_tmp.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 500, 
                                                    tweet2_days_since = 650, 
                                                    tweet3_days_since = 501, 
                                                    tweet4_days_since = 10, 
                                                    tweet5_days_since = 15, 
                                                    tweet6_days_since = 5, # should exit here
                                                    file_name = "test_tweets_page_tmp_2.html")


        
        current_dir = os.path.dirname(__file__)
        file_path_1 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")
        file_path_2 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_2.html")

        start = datetime.now()
        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path_1,
                                                stop_checking_after_days_threshold_met=7,
                                                sleep_after_loading = 0)
        file_1_time = datetime.now() - start
        
        start = datetime.now()
        time_since = crawler.get_time_lapsed_since_most_recent_activity_single_page(
                                                get_driver,
                                                url="file://" + file_path_2,
                                                stop_checking_after_days_threshold_met=7,
                                                sleep_after_loading = 0)
        file_2_time = datetime.now() - start


        # Check that file 1 runs quicker than file 2 with efficiency exit
        assert file_1_time < file_2_time
        




class TestTimeSinceRecentActivityMultiPage():
    def test_get_time_lapsed_since_most_recent_activity_multi_page_01(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 500, 
                                                    tweet2_days_since = 650, 
                                                    tweet3_days_since = 4, 
                                                    tweet4_days_since = 10, 
                                                    tweet5_days_since = 15, 
                                                    tweet6_days_since = 18,
                                                    file_name="test_tweets_page_tmp.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 123, 
                                                    tweet2_days_since = 456, 
                                                    tweet3_days_since = 789, 
                                                    tweet4_days_since = 12, 
                                                    tweet5_days_since = 19, 
                                                    tweet6_days_since = 20,
                                                    file_name="test_tweets_page_tmp_2.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 15, 
                                                    tweet2_days_since = 16, 
                                                    tweet3_days_since = 17, 
                                                    tweet4_days_since = 110, 
                                                    tweet5_days_since = 115, 
                                                    tweet6_days_since = 1118,
                                                    file_name="test_tweets_page_tmp_3.html")
        
        current_dir = os.path.dirname(__file__)
        file_path_1 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")
        file_path_2 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_2.html")
        file_path_3 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_3.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_multi_page(
                                                get_driver,
                                                urls=["file://" + file_path_1,
                                                    "file://" + file_path_2,
                                                    "file://" + file_path_3],
                                                sleep_after_loading=0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 4)) < timedelta(seconds=10)


    def test_get_time_lapsed_since_most_recent_activity_multi_page_02(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 500, 
                                                    tweet2_days_since = 650, 
                                                    tweet3_days_since = 40, 
                                                    tweet4_days_since = 100, 
                                                    tweet5_days_since = 15, 
                                                    tweet6_days_since = 18,
                                                    file_name="test_tweets_page_tmp.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 123, 
                                                    tweet2_days_since = 456, 
                                                    tweet3_days_since = 789, 
                                                    tweet4_days_since = 12, 
                                                    tweet5_days_since = 19, 
                                                    tweet6_days_since = 20,
                                                    file_name="test_tweets_page_tmp_2.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 15, 
                                                    tweet2_days_since = 16, 
                                                    tweet3_days_since = 17, 
                                                    tweet4_days_since = 110, 
                                                    tweet5_days_since = 115, 
                                                    tweet6_days_since = 1118,
                                                    file_name="test_tweets_page_tmp_3.html")
        

        current_dir = os.path.dirname(__file__)
        file_path_1 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")
        file_path_2 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_2.html")
        file_path_3 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_3.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_multi_page(
                                                get_driver,
                                                urls=["file://" + file_path_1,
                                                    "file://" + file_path_2,
                                                    "file://" + file_path_3],
                                                sleep_after_loading=0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 12)) < timedelta(seconds=10)


    def test_get_time_lapsed_since_most_recent_activity_multi_page_03(self, get_driver):
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 500, 
                                                     tweet2_days_since = 650, 
                                                     tweet3_days_since = 40, 
                                                     tweet4_days_since = 100, 
                                                     tweet5_days_since = 15, 
                                                     tweet6_days_since = 18,
                                                     file_name="test_tweets_page_tmp.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 123, 
                                                     tweet2_days_since = 456, 
                                                     tweet3_days_since = 789, 
                                                     tweet4_days_since = 112, 
                                                     tweet5_days_since = 119, 
                                                     tweet6_days_since = 210,
                                                     file_name="test_tweets_page_tmp_2.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 15, 
                                                     tweet2_days_since = 16, 
                                                     tweet3_days_since = 17, 
                                                     tweet4_days_since = 110, 
                                                     tweet5_days_since = 115, 
                                                     tweet6_days_since = 2,
                                                     file_name="test_tweets_page_tmp_3.html")
        
        current_dir = os.path.dirname(__file__)
        file_path_1 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")
        file_path_2 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_2.html")
        file_path_3 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_3.html")

        time_since = crawler.get_time_lapsed_since_most_recent_activity_multi_page(
                                                get_driver,
                                                urls=["file://" + file_path_1,
                                                      "file://" + file_path_2,
                                                      "file://" + file_path_3],
                                                sleep_after_loading=0)
        
        # Check these are within 10 seconds of each other (since processing time varies)
        assert (time_since - timedelta(days = 2)) < timedelta(seconds=10)






    def test_get_time_lapsed_since_most_recent_activity_multi_page_04(self, get_driver):
        # Checking efficient timing where threshold time is found on first page
        # and therefore later pages are skipped
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 6, 
                                                     tweet2_days_since = 650, 
                                                     tweet3_days_since = 40, 
                                                     tweet4_days_since = 100, 
                                                     tweet5_days_since = 15, 
                                                     tweet6_days_since = 18,
                                                     file_name="test_tweets_page_tmp.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 123, 
                                                     tweet2_days_since = 456, 
                                                     tweet3_days_since = 789, 
                                                     tweet4_days_since = 112, 
                                                     tweet5_days_since = 119, 
                                                     tweet6_days_since = 210,
                                                     file_name="test_tweets_page_tmp_2.html")
        
        create_test_tweets_page_html_with_relative_times(tweet1_days_since = 15, 
                                                     tweet2_days_since = 16, 
                                                     tweet3_days_since = 17, 
                                                     tweet4_days_since = 110, 
                                                     tweet5_days_since = 115, 
                                                     tweet6_days_since = 8,
                                                     file_name="test_tweets_page_tmp_3.html")
        
        current_dir = os.path.dirname(__file__)
        file_path_1 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp.html")
        file_path_2 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_2.html")
        file_path_3 = os.path.join(current_dir, "Testing_Resources/test_tweets_page_tmp_3.html")

        start = datetime.now()
        time_since = crawler.get_time_lapsed_since_most_recent_activity_multi_page(
                                                get_driver,
                                                urls=["file://" + file_path_1,
                                                      "file://" + file_path_2,
                                                      "file://" + file_path_3],
                                                sleep_after_loading=0)
        simulation_time_1 = datetime.now() - start


        start = datetime.now()
        time_since = crawler.get_time_lapsed_since_most_recent_activity_multi_page(
                                                get_driver,
                                                urls=["file://" + file_path_3,
                                                      "file://" + file_path_2,
                                                      "file://" + file_path_1],
                                                sleep_after_loading=0)
        simulation_time_2 = datetime.now() - start
        
        # Check the efficiency exit from the first ordering is quicker
        assert simulation_time_1 < simulation_time_2



def test_create_search_url_01():
    assert crawler.create_search_url("unc '24") == "https://twitter.com/search?q=unc%20%2724&src=typed_query&f=user"


def test_create_search_url_02():
    assert crawler.create_search_url("charlotte, nc") == "https://twitter.com/search?q=charlotte%2C%20nc&src=typed_query&f=user"

def test_create_search_url_03():
    assert crawler.create_search_url('''charlotte !"#$%&'()*+,/:;=?@[]''') == "https://twitter.com/search?q=charlotte%20!%22%23%24%25%26%27()*%2B%2C%2F%3A%3B%3D%3F%40%5B%5D&src=typed_query&f=user"





class TestCrawlUserPageFollowCriteria():
    def test_get_follower_count_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_01-posts.html")
        get_driver.get("file://" + file_path)

        # Valid posts page
        assert crawler.get_follower_count(get_driver) == 309800

    def test_get_follower_count_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_01-likes.html")
        get_driver.get("file://" + file_path)

        # Valid likes page
        assert crawler.get_follower_count(get_driver) == 309800

    def test_get_follower_count_03(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_02-posts.html")
        get_driver.get("file://" + file_path)

        # Valid posts page, empty
        assert crawler.get_follower_count(get_driver) == 0

    def test_get_follower_count_04(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_02-likes.html")
        get_driver.get("file://" + file_path)

        # Valid likes page, empty
        assert crawler.get_follower_count(get_driver) == 0

    def test_get_follower_count_05(self, get_driver):
        # Invalid page
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/following_scroll_2.html")
        get_driver.get("file://" + file_path)

        assert crawler.get_follower_count(get_driver) == -1
    
    def test_get_follower_count_06(self, get_driver):
        # Protected page
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_protected_pg.html")
        get_driver.get("file://" + file_path)

        assert crawler.get_follower_count(get_driver) == 1306

    def test_get_follower_count_07(self, get_driver):
        # Protected page
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_protected_pg2.html")
        get_driver.get("file://" + file_path)

        assert crawler.get_follower_count(get_driver) == 561
    

    def test_get_posts_count_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_01-posts.html")
        get_driver.get("file://" + file_path)

        # Valid posts page
        assert crawler.get_post_count(get_driver) == 33100

    def test_get_posts_count_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_01-likes.html")
        get_driver.get("file://" + file_path)

        # Valid likes page
        assert crawler.get_post_count(get_driver) == 20600

    def test_get_posts_count_03(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_02-posts.html")
        get_driver.get("file://" + file_path)

        # Valid posts page, empty
        assert crawler.get_post_count(get_driver) == 0

    def test_get_posts_count_04(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_02-likes.html")
        get_driver.get("file://" + file_path)

        # Valid likes page, empty
        assert crawler.get_post_count(get_driver) == 0
    
    

    def test_get_posts_date_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_01-posts.html")
        get_driver.get("file://" + file_path)

        # Valid posts page, make sure it doesn't return reserved values 0 or 9999
        assert crawler.get_time_lapsed_since_most_recent_activity_single_page(
            get_driver,
            stop_checking_after_days_threshold_met=7,
            already_loaded=True).days != 0
        assert crawler.get_time_lapsed_since_most_recent_activity_single_page(
            get_driver,
            stop_checking_after_days_threshold_met=7,
            already_loaded=True).days != 9999
    

    def test_get_posts_date_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/following_scroll_2.html")
        get_driver.get("file://" + file_path)

        # Not a valid page, should return error value
        assert crawler.get_time_lapsed_since_most_recent_activity_single_page(
            get_driver,
            stop_checking_after_days_threshold_met=7,
            already_loaded=True).days == 9999


    def test_get_posts_count_05(self, get_driver):
        # Invalid page
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/following_scroll_2.html")
        get_driver.get("file://" + file_path)

        assert crawler.get_post_count(get_driver) == -1
    
    def test_page_load_fail_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/page_load_fail.html")
        get_driver.get("file://" + file_path)

        # Check to make sure this default failing value hasn't been changed. Other functions check for it explicitly.
        assert crawler.get_time_lapsed_since_most_recent_activity_single_page(get_driver, already_loaded = True).days == 9999


    def test_get_protected_status_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/page_load_fail.html")
        get_driver.get("file://" + file_path)

        # Page load fail should get fallback option of False
        assert crawler.get_protected_status(get_driver) == False
    
    def test_get_protected_status_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_01-posts.html")
        get_driver.get("file://" + file_path)

        # Standard non-protected page
        assert crawler.get_protected_status(get_driver) == False
    

    def test_get_protected_status_03(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/protected_profile_page.html")
        get_driver.get("file://" + file_path)

        # Protected page
        assert crawler.get_protected_status(get_driver) == True
    

    def test_get_protected_status_04(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/user_protected_and_verified.html")
        get_driver.get("file://" + file_path)

        # Protected page AND verified
        assert crawler.get_protected_status(get_driver) == True

    
    def test_get_blocked_page_center_text_01(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/page_load_fail.html")
        get_driver.get("file://" + file_path)

        # Failed load entirely
        assert crawler.get_blocked_page_center_text(get_driver) == ""
    
    def test_get_blocked_page_center_text_02(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/test_user_profile_page_01-posts.html")
        get_driver.get("file://" + file_path)

        # Standard page, should not be any blocked page text
        assert crawler.get_blocked_page_center_text(get_driver) == ""
    

    def test_get_blocked_page_center_text_03(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/account_doesnt_exist_profile_page.html")
        get_driver.get("file://" + file_path)

        # Account doesn't exist
        assert crawler.get_blocked_page_center_text(get_driver) == "This account doesn’t exist"
    
    def test_get_blocked_page_center_text_04(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/account_suspended_profile_page.html")
        get_driver.get("file://" + file_path)

        # Account suspended
        assert crawler.get_blocked_page_center_text(get_driver) == "Account suspended"
    
    def test_get_blocked_page_center_text_05(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/account_restricted_profile_page.html")
        get_driver.get("file://" + file_path)

        # Account restricted
        assert crawler.get_blocked_page_center_text(get_driver) == "Caution: This account is temporarily restricted"
    
    def test_get_blocked_page_center_text_06(self, get_driver):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "Testing_Resources/account_sensitive_profile_page.html")
        get_driver.get("file://" + file_path)

        # Account sensitive
        assert crawler.get_blocked_page_center_text(get_driver) == "Caution: This profile may include potentially sensitive content"