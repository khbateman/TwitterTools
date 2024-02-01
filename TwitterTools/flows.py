# TwitterTools imports
from TwitterTools.data_tools import pd
from TwitterTools.user_management import is_account_to_follow
import pandas as pd
from .driver_tools import *
from .crawler import *
from .data_tools import *
from .user_management import *


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


def display_unfollow_count(handles_to_skip = [], unfollow_after_days = 7):
    df = get_df_of_user_to_unfollow(handles_to_skip, unfollow_after_days)

    print("Ready to unfollow:", df.shape[0])


def update_excel_file_with_accounts_to_follow(
        driver, 
        users_to_scrape = [], 
        accounts_to_skip = [], 
        search_queries = [], 
        num_search_query_accounts = 100, 
        terminate_each_search_query_scrape_after_seconds = 120, 
        post_urls = [], 
        scrape_post_quotes = True, 
        scrape_post_reposts = True, 
        scrape_post_likes = True):
    # start with existing lists
    # Make everyone we add "followed" = False, which will be changed
    # as we actually open the tabs to follow them so we don't have to recrawl this

    # Open existing list and keep anyone that hasn't yet been followed
    # Reindex to clean it up
    accounts_to_follow_df = pd.read_excel("accounts_to_follow.xlsx")
    accounts_to_follow_df = accounts_to_follow_df[accounts_to_follow_df["followed"] == False]
    accounts_to_follow_df.reset_index(drop=True, inplace=True)

    # Skip any accounts that are already on the accounts-to-follow df
    accounts_already_on_follow_list = list(accounts_to_follow_df["handle"])
    accounts_to_skip += accounts_already_on_follow_list

    # accounts_to_follow_df = pd.DataFrame([], columns=["handle", "url", "followed"])
    # accounts_to_follow_df["source"] = "-"

    already_followed_df = pd.read_excel("following.xlsx")
    already_followed = list(already_followed_df["handle"])

    # Wrap the whole process in a try block so if something goes wrong, 
    # the script saves the dataframe at that point rather than losing data
    try:

        # First crawl similar account users
        for user in users_to_scrape:
            followers = scrape_follow_pages(driver,
                                            twitter_handle = user,
                                            following = False,
                                            verified_followers = True,
                                            followers = True)

            for follower in followers:
                # If the user doesn't follow me, I don't follow them, and I've never followed them before, they're a candidate to follow
                if not follower.following_me and not follower.following_them and follower.handle not in already_followed and not follower.protected_account and follower.handle not in accounts_to_skip:
                    # Since we haven't followed this account yet, it will be False
                    # Since these accounts may not be relevant, ready_to_follow is also False by default
                    tmp_row = pd.DataFrame([[follower.handle, follower.url, False, False, f"following {user}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                    accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)

        # Crawl specified search queries for users
        for query in search_queries:
            new_accounts = crawl_users_from_search(driver,
                                                query = query,
                                                num_accounts = num_search_query_accounts,
                                                accounts_to_skip = accounts_to_skip, terminate_after_seconds = terminate_each_search_query_scrape_after_seconds,
                                                already_followed_handles = already_followed)
            for account in new_accounts:
                # If the user doesn't follow me, I don't follow them, and I've never followed them before, they're a candidate to follow
                if is_account_to_follow(account, already_followed, accounts_to_skip):
                    tmp_row = pd.DataFrame([[account.handle, account.url, False, False, f"Search: {query}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                    accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)


        # Go through posts to scrape engagements
        # Note that any direct post engagement will be noted that it's TRUE for ready_to_follow
        for post_url in post_urls:
            # Clean the URL to allow for input of URLs either ending in / or not
            if post_url[-1] == "/":
                cleaned_url = post_url[:-1]
            else:
                cleaned_url = post_url

            # Add specific post engagement URLs based on arguments
            # Default is to crawl all 3, but can set any to false to limit scraping
            if scrape_post_likes:
                new_accounts = scrape_follow_pages(driver, direct_url = f"{cleaned_url}/likes")

                for account in new_accounts:
                    # If the user doesn't follow me, I don't follow them, and I've 
                    if is_account_to_follow(account, already_followed, accounts_to_skip):
                        tmp_row = pd.DataFrame([[account.handle, account.url, False, True, f"Liked post: {cleaned_url}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                        accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)

            if scrape_post_reposts:
                new_accounts = scrape_follow_pages(driver, direct_url = f"{cleaned_url}/retweets")

                for account in new_accounts:
                    if is_account_to_follow(account, already_followed, accounts_to_skip):
                        tmp_row = pd.DataFrame([[account.handle, account.url, False, True, f"Reposted post: {cleaned_url}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                        accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)

            if scrape_post_quotes:
                new_accounts = scrape_follow_pages(driver, direct_url = f"{cleaned_url}/quotes")

                for account in new_accounts:
                    if is_account_to_follow(account, already_followed, accounts_to_skip):
                        tmp_row = pd.DataFrame([[account.handle, account.url, False, True, f"Quoted post: {cleaned_url}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                        accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)
    except:
        pass


    accounts_to_follow_df = accounts_to_follow_df.drop_duplicates(subset=['handle'])
    accounts_to_follow_df.reset_index(drop=True, inplace=True)
    accounts_to_follow_df.to_excel("accounts_to_follow.xlsx", index=False)

    return accounts_to_follow_df