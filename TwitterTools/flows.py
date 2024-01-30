# TwitterTools imports
from .driver_tools import *
from .crawler import *
from .data_tools import *


def create_driver_and_login(username, password, sleep_time = 3):
    driver = create_driver()
    log_in_twitter(driver, username, password, sleep_time)

    return driver


def update_my_following_data(driver, handle):
    '''
    Takes a logged in driver and Twitter handle (mine) and
    1) Crawls my following page and creates a list of Users
    2) Turns that list of Users into a dataframe
    3) Saves / appends that data to `following.xlsx`
    '''
    following_url = f"https://twitter.com/{handle}/following"
    users, user_urls = scrape_single_follow_page(driver, following_url)
    df = users_list_to_following_df(users)
    following_users_df_to_excel(df)

