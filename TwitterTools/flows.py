# TwitterTools imports
from TwitterTools.data_tools import get_df_of_user_to_unfollow, pd
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
        users_to_scrape_followers = [], 
        # accounts_to_skip = [], 
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
    # accounts_to_follow_df = pd.read_excel("accounts_to_follow.xlsx")
    # accounts_to_follow_df = accounts_to_follow_df[accounts_to_follow_df["followed"] == False]
    # accounts_to_follow_df.reset_index(drop=True, inplace=True)


    # Get existing handles from the data and convert
    # them to sets for quicker querying on repeated calls below
    handles_to_skip = set(get_handles_list("accounts_to_skip.xlsx"))
    handles_to_follow = set(get_handles_list("accounts_to_follow.xlsx"))
    handles_following = set(get_handles_list("following.xlsx"))

    # Combine accounts to follow and skip for arguments below
    handles_to_skip = handles_to_skip.union(handles_to_follow)

    # Skip any accounts that are already on the accounts-to-follow df
    # accounts_already_on_follow_list = list(accounts_to_follow_df["handle"])
    # handles_to_skip += handles_to_follow

    # accounts_to_follow_df = pd.DataFrame([], columns=["handle", "url", "followed"])
    # accounts_to_follow_df["source"] = "-"



    # already_followed_df = pd.read_excel("following.xlsx")
    # already_followed = list(already_followed_df["handle"])

    # Wrap the whole process in a try block so if something goes wrong, 
    # the script saves the dataframe at that point rather than losing data
    try:

        # First crawl every account from arguments passed in
        for user in users_to_scrape_followers:
            followers = scrape_follow_pages(driver,
                                            twitter_handle = user,
                                            following = False,
                                            verified_followers = True,
                                            followers = True)
            
            update_accounts_to_follow_excel_from_user_list(
                users = followers,
                source = f"following {user}",
                ready_to_follow = False,
                validate_users = True,
                accounts_following = handles_following,
                accounts_to_skip = handles_to_skip
            )
            # checked_followers = []
            # for follower in followers:
            #     # Verify it the account meets criteria for following
            #     if is_account_to_follow(follower, handles_following, handles_to_skip):
            #         checked_followers += follower

            #         # Since we haven't followed this account yet, it will be False
            #         # Since these accounts may not be relevant, ready_to_follow is also False by default
            #         # tmp_row = pd.DataFrame([[follower.handle, follower.url, False, False, f"following {user}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
            #         # accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)

            
            # df = users_list_to_accounts_to_follow_df(checked_followers, 
            #                                          source = f"following {user}",
            #                                          ready_to_follow=False)
            
            # accounts_to_follow_df_to_excel(df)



        # Crawl specified search queries for users
        # Note - there is a call to is_account_to_follow from within 
        # crawl_users_from_search so we don't need that check for this
        # specific type of crawl
        for query in search_queries:
            new_accounts = crawl_users_from_search(driver,
                                                query = query,
                                                num_accounts = num_search_query_accounts,
                                                accounts_to_skip = handles_to_skip, 
                                                terminate_after_seconds = terminate_each_search_query_scrape_after_seconds,
                                                already_followed_handles = handles_following)
            
            update_accounts_to_follow_excel_from_user_list(
                users = new_accounts,
                source = f"Search: {query}",
                validate_users = False,
                ready_to_follow = False,
                accounts_following = handles_following,
                accounts_to_skip = handles_to_skip
            )
            
            # df = users_list_to_accounts_to_follow_df(new_accounts, 
            #                                         source = f"Search: {query}",
            #                                         ready_to_follow=False)
        
            # accounts_to_follow_df_to_excel(df)


            # for account in new_accounts:
                # # If the user doesn't follow me, I don't follow them, and I've never followed them before, they're a candidate to follow
                # if is_account_to_follow(account, handles_following, handles_to_skip):
                #     tmp_row = pd.DataFrame([[account.handle, account.url, False, False, f"Search: {query}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                #     accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)


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
                users, user_urls = scrape_single_follow_page(driver, f"{cleaned_url}/likes")
                # new_accounts = scrape_follow_pages(driver, direct_url = f"{cleaned_url}/likes")

                update_accounts_to_follow_excel_from_user_list(
                    users = users,
                    source = f"Liked post: {cleaned_url}",
                    validate_users = True,
                    ready_to_follow = True,
                    accounts_following = handles_following,
                    accounts_to_skip = handles_to_skip
                )

                # checked_accounts = []
                # for user in users:
                #     # Verify it the account meets criteria for following
                #     if is_account_to_follow(user, handles_following, handles_to_skip):
                #         checked_accounts += user
                
                # df = users_list_to_accounts_to_follow_df(checked_followers, 
                #                                      source = f"Liked post: {cleaned_url}",
                #                                      ready_to_follow=True)
            
                # accounts_to_follow_df_to_excel(df)



                # for account in new_accounts:
                #     # If the user doesn't follow me, I don't follow them, and I've 
                #     if is_account_to_follow(account, handles_following, handles_to_skip):
                #         tmp_row = pd.DataFrame([[account.handle, account.url, False, True, f"Liked post: {cleaned_url}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                #         accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)

            if scrape_post_reposts:
                new_accounts, user_urls = scrape_single_follow_page(driver, f"{cleaned_url}/retweets")

                update_accounts_to_follow_excel_from_user_list(
                    users = new_accounts,
                    source = f"Reposted post: {cleaned_url}",
                    validate_users = True,
                    ready_to_follow = True,
                    accounts_following = handles_following,
                    accounts_to_skip = handles_to_skip
                )

                # for account in new_accounts:
                #     if is_account_to_follow(account, handles_following, handles_to_skip):
                #         tmp_row = pd.DataFrame([[account.handle, account.url, False, True, f"Reposted post: {cleaned_url}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                #         accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)

            if scrape_post_quotes:
                new_accounts, user_urls = scrape_single_follow_page(driver, f"{cleaned_url}/quotes", quote_page=True)

                update_accounts_to_follow_excel_from_user_list(
                    users = new_accounts,
                    source = f"Quoted post: {cleaned_url}",
                    validate_users = True,
                    ready_to_follow = True,
                    accounts_following = handles_following,
                    accounts_to_skip = handles_to_skip
                )

                # for account in new_accounts:
                #     if is_account_to_follow(account, handles_following, handles_to_skip):
                #         tmp_row = pd.DataFrame([[account.handle, account.url, False, True, f"Quoted post: {cleaned_url}"]], columns=["handle", "url", "followed", "ready_to_follow", "source"])
                #         accounts_to_follow_df = pd.concat([accounts_to_follow_df, tmp_row], axis = 0)
    except:
        pass


    # accounts_to_follow_df = accounts_to_follow_df.drop_duplicates(subset=['handle'])
    # accounts_to_follow_df.reset_index(drop=True, inplace=True)
    # accounts_to_follow_df.to_excel("accounts_to_follow.xlsx", index=False)

    # return accounts_to_follow_df



def validate_accounts_to_follow(driver, num_rows_to_validate = -1, activity_within_days = 60, sleep_after_loading = 2, sleep_between_users = (3, 7), print_progress = False):
    '''
    If `num_rows_to_validate` is -1, rows are not limited

    Takes a logged-in driver and validates any row in the data where the user is
    1) not followed
    2) hasn't already been validated through other means (ex - recently liking a relevant post)

    If a user has been successfully evaluated, they'll either be
    1) Valid (`followed` will remain False and `ready_to_follow` will be changed to True)
    2) Invalid (`followed` will be changed to True so the row will be removed next crawl)
    
    If there is an error in crawling, nothing gets updated for that user
    '''
    rows_to_validate = get_rows_to_validate(num_rows_to_validate)

    for index, row in rows_to_validate.iterrows():

        if print_progress:
            print(f"Validating {row['handle']}", end = "")

        # Placeholder in case second page doesn't get crawled
        overall_validation_result = None

        driver.get(row["url"])
        time.sleep(sleep_after_loading)

        num_likes = -1
        post_count = get_post_count(driver)
        follower_count = get_follower_count(driver)
        days_since_last_post = get_time_lapsed_since_most_recent_activity_single_page(
                        driver, 
                        stop_checking_after_days_threshold_met = activity_within_days, 
                        already_loaded = True)
        
        # This will only be True or None with the num_likes value as -1
        first_page_validation_result = meets_additional_account_following_criteria(
                                            num_posts = post_count, 
                                            num_likes = num_likes, 
                                            num_followers = follower_count, 
                                            days_since_most_recent_activity = days_since_last_post)
        

        if first_page_validation_result is None:
            # Extreme cases not met, need to continue on to likes page for full validation
            driver.get(f"https://twitter.com/{row['handle']}/likes")
            time.sleep(sleep_after_loading)

            num_likes = get_post_count(driver)
            days_since_last_like = get_time_lapsed_since_most_recent_activity_single_page(
                        driver, 
                        stop_checking_after_days_threshold_met = activity_within_days, 
                        already_loaded = True)
            
            if days_since_last_like < days_since_last_post:
                days_since_last_activity = days_since_last_like
            else:
                days_since_last_activity = days_since_last_post
            

            overall_validation_result = meets_additional_account_following_criteria(
                                            num_posts = post_count, 
                                            num_likes = num_likes, 
                                            num_followers = follower_count, 
                                            days_since_most_recent_activity = days_since_last_activity)

    

        # Can't omit the ==True check because it will error out when it's None
        if first_page_validation_result == True or overall_validation_result == True:
            # Update row in file
            update_accounts_to_follow_row(handle = row["handle"], ready_to_follow = True)
            
            if print_progress:
                print(f" | Result: True (1st Page: {first_page_validation_result} Overall: {overall_validation_result})")
        elif overall_validation_result == False:
            # Update row in file so it will be filtered out next time
            update_accounts_to_follow_row(handle = row["handle"], followed = True)

            # And add the handle to accounts_to_skip
            add_user_to_accounts_to_skip(row["handle"])

            print(f" | Result: False (1st Page: {first_page_validation_result} Overall: {overall_validation_result})")
        

        # Pause between validating another user to avoid rate limits
        time.sleep(random.randint(sleep_between_users[0], sleep_between_users[1]))

    
