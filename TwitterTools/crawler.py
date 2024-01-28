from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta
import math
import os
from requests import request
import json
import keyring
import random

# Other TwitterTools imports
from .User import User
from .user_management import *



def create_driver():
    # Launch driver and open webpage
    options = webdriver.safari.options.Options()
    driver = webdriver.Safari(options=options)
    driver.implicitly_wait(5) # wait for 5 seconds to find objects that may take time to load before throwing exception

    # Make window big enough to see
    driver.set_window_size(1600,1000)

    return driver


def log_in_twitter(driver, username, password, sleep_time = 2):
    driver.get("https://twitter.com/login")
    time.sleep(sleep_time)
    driver.find_element(By.TAG_NAME, "input").send_keys(f"{username}\n")
    # driver.find_element(By.TAG_NAME, "input").send_keys("\n")
    time.sleep(sleep_time)
    driver.find_element(By.TAG_NAME, "input").send_keys(f"{password}\n")
    time.sleep(1)


def get_all_user_divs(driver):
    '''
    Function takes in an argument of a `selenium` driver already on a page
    with a list of users (ex - following page)

    Returns
    ----
    `list` of all selenium div container elements for each user
    '''
    # Check in case there's no users available, break out
    try:
        # Using wildcard XPATH we can find the cells of the users
        return driver.find_elements(By.XPATH, """//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[*]""")
    except:
        return []





def create_user_from_div_v1(div):
    '''
    The functionality of this is identical to the below `create_user_from_div` however
    this is MUCH slower since it tries to find an element by searching using `find_element`,
    which takes almost twice as long. The optimized version looks for exact XPATHs, which
    speeds things up considerably

    Takes in a div of a user from Twitter.

    The div is typically the format where there's a user's profile pic, name, handle, bio, and a Follow / Following button on the right.
    
    The `div` argument should be the highest level div before the list-like structure that holds them. It should be in the format of a `selenium` element from querying using `find_elements()`
    '''
    profile_url = ""
    following_me = False
    following_them = False
    protected_account = False
    verified = False

    try:
        profile_url = div.find_element(By.CSS_SELECTOR, "a").get_attribute(name="href")

        # Get all the spans in this div to see if there's the "Follows you" block or if follow button text shows following them
        for span in div.find_elements(By.TAG_NAME, "span"):
            if span.text == "Follows you":
                following_me = True
            elif span.text == "Follow":
                following_them = False
            elif span.text == "Following":
                following_them = True

        # Check the SVGs to see if the protected account is there
        # Need to put it in another try block so it doesn't blow
        # up and error out every non-svg cell
        try:
            for svg in div.find_elements(By.TAG_NAME, "svg"):
                if svg.get_attribute("aria-label") == "Protected account":
                    protected_account = True
                elif svg.get_attribute("aria-label") == "Verified account":
                    verified = True
        except:
            pass
    except:
        pass

    return User.from_url(profile_url, 
                         following_me=following_me, 
                         following_them=following_them, protected_account=protected_account,
                         verified=verified)



def create_user_from_div(div):
    '''
    Takes in a div of a user from Twitter.

    The div is typically the format where there's a user's profile pic, name, handle, bio, and a Follow / Following button on the right.
    
    The `div` argument should be the highest level div before the list-like structure that holds them. It should be in the format of a `selenium` element from querying using `find_elements()`
    '''
    profile_url = ""
    following_me = False
    following_them = False
    protected_account = False
    verified = False    

    # NOTE - the XPATHs are relative to the div being passed in, 
    # so each will have a . to start and have ONE LESS div to start (since 
    # we're relating to THAT div, it doesn't need to appear)
    try:
        profile_url = div.find_element(By.XPATH, '''.//div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/a''').get_attribute(name="href")
    except:
        pass

    try:
        follow_button_text = div.find_element(By.XPATH, '''.//div/div/div/div/div[2]/div[1]/div[2]/div/div/span/span''').text

        if follow_button_text == "Follow":
            following_them = False
        elif follow_button_text == "Following":
            following_them = True
    except:
        pass

    # Some pages have a slightly different layout and need this selector path
    try:
        follow_button_text = div.find_element(By.XPATH, '''.//div/div/div/div/div[2]/div/div[2]/div[1]/div/div/span/span''').text

        if follow_button_text == "Follow":
            following_them = False
        elif follow_button_text == "Following":
            following_them = True
    except:
        pass

    try:
        follows_you_text = div.find_element(By.XPATH, '''.//div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span''').text

        if follows_you_text == "Follows you":
            following_me = True
    except:
        pass
    
    try:
        # It is slightly unclear why the final part of the XPATH needs to be a *
        # rather than svg here. Analyzing the return of the span right before it
        # shows the next element is svg, but specifying svg makes it fail. 
        # However, allowing the anything with the * makes it work. 
        verified_svg_label = div.find_element(By.XPATH, '''.//div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[2]/span/*''').get_attribute("aria-label")
        
        if verified_svg_label == "Verified account":
            verified = True
    except:
        pass

    try:
        verified_svg_label = div.find_element(By.XPATH, '''.//div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[2]/span/*[1]''').get_attribute("aria-label")

        if verified_svg_label == "Verified account":
            verified = True
    except:
        pass


    # Need to try this twice because sometimes it might be alone and not be second
    try:
        protected_svg_label = div.find_element(By.XPATH, '''.//div/div/div/div/div[2]/div/div[1]/div/div[1]/a/div/div[2]/span/*[1]''').get_attribute("aria-label")
        if protected_svg_label == "Protected account":
            protected_account = True
    except:
        pass

    try:
        protected_svg_label = div.find_element(By.XPATH, '''.//div/div/div/div/div[2]/div/div[1]/div/div[1]/a/div/div[2]/span/*[2]''').get_attribute("aria-label")
        if protected_svg_label == "Protected account":
            protected_account = True
    except:
        pass
    

    return User.from_url(profile_url, 
                         following_me=following_me, 
                         following_them=following_them, protected_account=protected_account,
                         verified=verified)



def scrape_single_follow_page(driver, url):
    '''
    This function scrapes followers off of a single follower/following page 
    (and other similarly formatted pages)

    Returns
    ----
    `tuple` : (list of users (type: `User`), 
               list of strings of user urls)
    '''
    # Since we already have wait times built in here, don't need additional waits
    # that will redundantly slow this down
    driver.implicitly_wait(0.01)

    # Navigate to following page and wait for it to load
    driver.get(url)
    time.sleep(1.0)

    users_added = True
    next_scroll_y = 0
    users = []
    user_urls = []

    while users_added:
        # Get all the divs each time (because they change on scroll)
        # First scroll so they load, then get the divs
        driver.execute_script(f"window.scrollTo(0, {next_scroll_y})")

        # Need to briefly wait after scrolling to let new users load
        time.sleep(2.0)
        
        all_divs = get_all_user_divs(driver)
        
        if len(all_divs) == 0:
            break
        
        # Change flag back to False. If we find new users, 
        # it will change to True to keep loop running
        users_added = False
        next_scroll_y += 1000

        # Go from the last div at the bottom towards the top
        for div in all_divs[::-1]:
            try:
                user = create_user_from_div(div)

                if user.url in user_urls:
                    break
                else:
                    users.append(user)
                    user_urls.append(user.url)
                    users_added = True
            except:
                pass

    # Change driver back to a 5 second wait
    driver.implicitly_wait(5)

    return users, user_urls



def scrape_follow_pages(driver, twitter_handle, following = True, verified_followers = False, followers = False, direct_url = ""):
    '''
    This function scrapes followers off of follower/following pages and other similarly formatted pages
    '''
    
    urls_to_scrape = []

    # Handling direct URLs to pages with "follow" formats (ex - post retweet / like pages)
    if direct_url != "":
        urls_to_scrape.append(direct_url)
    else:
        # If a direct URL isn't passed, follow previous logic

        # Add pages to crawl based on arguments
        if following:
            urls_to_scrape.append(f"https://twitter.com/{twitter_handle}/following")
        
        if verified_followers:
            urls_to_scrape.append(f"https://twitter.com/{twitter_handle}/verified_followers")
        
        if followers:
            urls_to_scrape.append(f"https://twitter.com/{twitter_handle}/followers")


    users = []
    user_urls = []

    for url in urls_to_scrape:
        tmp_users, tmp_user_urls = scrape_single_follow_page(driver, url)
        users += tmp_users   
        user_urls += tmp_user_urls 
    
    return users



def get_time_lapsed_since_most_recent_activity_single_page(driver, url, stop_checking_after_days_threshold_met = 7):
    # Checks the most recent date of post or post liked. Start with big number
    time_since_most_recent_activity = timedelta(days=9999)

    driver.get(url)
    time.sleep(2)

    # Get the div that holds user Tweets
    # In rare cases where this user no longer exists, this element can't be found
    # so return a default big number and exit so Exception isn't thrown
    try:
        post_divs = driver.find_elements(By.XPATH, """//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[*]""")
    except:
        return timedelta(days=9999)
    
    for div in post_divs:
        if time_since_most_recent_activity.days < stop_checking_after_days_threshold_met:
            break
        try:
            # The times are enclosed in <time> tags. Find the first one
            first_time_tag_element = div.find_element(By.TAG_NAME, "time")

            # Get the datetime attribute from this tag and parse it from format
            # 2023-09-28T10:41:25.000Z
            post_date = datetime.strptime(first_time_tag_element.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ")
                            
            time_since_post = datetime.today() - post_date

            if time_since_post < time_since_most_recent_activity:
                time_since_most_recent_activity = time_since_post
            
        except:
            pass

    return time_since_most_recent_activity


def get_time_lapsed_since_most_recent_activity_multi_page(driver, urls, stop_checking_after_days_threshold_met = 7):
    # Checks the most recent date of post or post liked 
    time_since_most_recent_activity = timedelta(days=9999)

    for url in urls:
        if time_since_most_recent_activity.days < stop_checking_after_days_threshold_met:
            break
        else:
            page_most_recent_activity = get_time_lapsed_since_most_recent_activity_single_page(driver, url, stop_checking_after_days_threshold_met = stop_checking_after_days_threshold_met)

            if page_most_recent_activity < time_since_most_recent_activity:
                time_since_most_recent_activity = page_most_recent_activity

    return time_since_most_recent_activity



def get_time_lapsed_since_most_recent_activity(driver, base_profile_url, stop_checking_after_days_threshold_met = 7):

    # Base user URL 
    base_user_url = driver.current_url
    three_pages = [base_profile_url, base_profile_url + "/with_replies", base_profile_url + "/likes"]

    # Go to base profile, replies, and likes and crawl posts
    time_since_most_recent_activity = get_time_lapsed_since_most_recent_activity_multi_page(driver, three_pages, stop_checking_after_days_threshold_met)
        
    return time_since_most_recent_activity


def show_ready_to_unfollow_count():
    pass


def open_tabs_for_unfollowing(driver, number_to_unfollow = 10, sleep_between_tabs=5, only_show_unfollow_count = False): 
    '''
    only_show_unfollow_count is an argument that can be used to only display the printed line 
    of how many accounts are ready to unfollow. Useful to check how many are ready before starting the script
    '''   
    # Read in overall following list
    df = pd.read_excel("following.xlsx", parse_dates=["followed_before"])

    # Certain accounts I follow because they're relevant to Charlotte
    # These shouldn't be suggested to unfollow
    accounts_to_skip = ["wsoctv", "axioscharlotte", "CLTMayor", "theobserver", "BofAstadium", "spectrumcenter", "unccharlotte", "KnightsBaseball", "hornets", "Panthers", "Charlottgotalot", "AllyCLTCenter", "CLTGuide", "wxbrad", "CharlotteFC", "WBTV_News", "CLTAirport", "Independence", "CharlotteFive", "shootbt", "BOAStadiumWx"]
    df["skip"] = df["handle"].isin(accounts_to_skip)


    # Calculated rows
    df["time_following"] = datetime.today() - df["followed_before"]
    
    
    unfollow_rows = df[(df["following_me"] == False) &
                       (df["currently_following"] == True) & 
                       (df["time_following"] > timedelta(days=7)) &
                       (df["skip"] == False)]

    print("Ready to unfollow:", unfollow_rows.shape[0])

    if only_show_unfollow_count:
        return
    
    opened_tabs = 1

    # Sort from the oldest to newest follow
    unfollow_rows = unfollow_rows.sort_values(by=['followed_before'])

    # Can uncomment this to check before processing
    # for row_tuple in unfollow_rows.iterrows():
    #     print(row_tuple[1])
    # return

    for row_tuple in unfollow_rows.iterrows():
        time.sleep(random.randint(0, sleep_between_tabs))

        row = row_tuple[1]

        # Go to  profile page and get the date of their latest tweet / reply / like
        days_since_last_activity = get_time_lapsed_since_most_recent_activity(driver, row["url"])
        
        # Want to unfollow if they've done something on Twitter since I've followed them
        if days_since_last_activity < row["time_following"] or days_since_last_activity.days > 30:
            # In this case, leave that tab open to manually unfollow and 
            # open a new tab to check another user if we haven't reached 
            # the max number of tabs to unfollow already
            if opened_tabs < number_to_unfollow:
                # copy the cookies from this tab (so don't have to log in again)
                # and start this over in a new tab
                cookies = driver.get_cookies()
                driver.switch_to.new_window('tab')
                for cookie in cookies:
                    driver.add_cookie(cookie)
                
                opened_tabs += 1
            else:
                return

        else:
            print(f"{row['handle']} hasn't had activity in {days_since_last_activity.days} days")




def create_search_url(query):
    url = "https://twitter.com/search?q="

    query = query.replace(",", "%2C")
    query = query.replace(" ", "%20")

    url += query
    url += "&src=typed_query&f=user"
    
    return url



def crawl_users_from_search(driver, query, num_accounts, accounts_to_skip = [], terminate_after_seconds = 120, already_followed_handles = []):
    # Since we already have wait times built in here, don't need additional waits
    # that will redundantly slow this down
    driver.implicitly_wait(0.01)

    driver.get(create_search_url(query))
    time.sleep(1.0)

    start_time = datetime.now()
    seconds_elapsed = (datetime.now() - start_time).seconds
    next_scroll_y = 0
    tmp_users = []
    tmp_user_urls = []

    # Sometimes it gets rate limited and scrolling stops returning new users
    # When this happens, this flag will go to True to break out of search
    # Need to check the next-to-last user instead of final user because
    # when search gets exhausted, the final div ends up being empty
    search_exhausted = False
    previous_loop_next_to_last_user_url = ""

    while seconds_elapsed < terminate_after_seconds and len(tmp_users) <= num_accounts and not search_exhausted:
        # Scroll to next height
        driver.execute_script(f"window.scrollTo(0, {next_scroll_y})")

        # Need to briefly wait after scrolling to let new users load
        time.sleep(2.0)

        # Get all the divs for each user (wildcard path)
        all_user_divs = driver.find_elements(By.XPATH, """//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[*]""")

        # Before starting the loop, check if nothing has changed
        # (i.e. - final user in list is different)
        # If nothing is changed, search has stalled, break out
        try:
            next_to_last_user_url = all_user_divs[-2].find_element(By.CSS_SELECTOR, "a").get_attribute(name="href")

            if next_to_last_user_url == previous_loop_next_to_last_user_url:
                search_exhausted = True
                print(f"{next_to_last_user_url} remains final user returned. Search exhaused")
                break
            else:
                previous_loop_next_to_last_user_url = next_to_last_user_url
        except:
            pass

        # Go from the last div at the bottom towards the top
        for div in all_user_divs[::-1]:
            try:
                profile_url = div.find_element(By.CSS_SELECTOR, "a").get_attribute(name="href")

                if profile_url in tmp_user_urls:
                    # Once we hit a URL we've seen before, we
                    # can scroll again since we're working bottom-up
                    break
                else:
                    following_me = False
                    following_them = False
                    protected_account = False

                    # Get all the spans in this div to see if there's the "Follows you" block or if follow button text shows following them
                    for span in div.find_elements(By.TAG_NAME, "span"):
                        if span.text == "Follows you":
                            following_me = True
                        elif span.text == "Follow":
                            following_them = False
                        elif span.text == "Following":
                            following_them = True

                    # Check the SVGs to see if the protected account is there
                    # Need to put it in another try block so it doesn't blow
                    # up and error out every non-svg cell
                    try:
                        for svg in div.find_elements(By.TAG_NAME, "svg"):
                            if svg.get_attribute("aria-label") == "Protected account":
                                protected_account = True
                    except:
                        # print("svg blew it up")
                        pass


                    user = User.from_url(profile_url, following_me=following_me, following_them=following_them, protected_account=protected_account)

                    # Helpful check so doesn't max out list with 
                    # previously followed accounts
                    if is_account_to_follow(user, already_followed_handles, accounts_to_skip):
                        tmp_users.append(user)
                        tmp_user_urls.append(profile_url)

            except:
                pass

        next_scroll_y += 1000
        seconds_elapsed = (datetime.now() - start_time).seconds
    
    print(f"Finished search crawl after {seconds_elapsed} secs and finding {len(tmp_users)} new users")

    for user in tmp_users:
        print(user.handle)
    
    # Set driver wait times back
    driver.implicitly_wait(5)
    return tmp_users



def open_tabs_for_following(driver, num_to_follow = 20, sleep_between_tabs = 0):
    '''`sleep_between_tabs` will generate a random number between 0 and that value to sleep'''

    accounts_to_follow_df = pd.read_excel("accounts_to_follow.xlsx")

    unfollowed = accounts_to_follow_df[accounts_to_follow_df["followed"] == False]
    handles_to_follow = list(unfollowed.iloc[:num_to_follow, :]["handle"])
    print(handles_to_follow)

    for i in range(len(handles_to_follow)):
        time.sleep(random.randint(0, sleep_between_tabs))
        
        handle = handles_to_follow[i]
        driver.get(f"https://www.twitter.com/{handle}")
        
        if i < len(handles_to_follow) - 1:
            # open a new tab for next loop
            # Copy cookies to put in new tab to avoid relogging in
            cookies = driver.get_cookies()
            driver.switch_to.new_window('tab')
            for cookie in cookies:
                driver.add_cookie(cookie)

        # Update dataframe so we don't revisit this again in the future
        # (before we re-run account finding script)
        accounts_to_follow_df.loc[accounts_to_follow_df["handle"] == handle, "followed"] = True
    
    accounts_to_follow_df.to_excel("accounts_to_follow.xlsx", index=False)