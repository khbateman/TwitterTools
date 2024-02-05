
# Other TwitterTools imports
from .User import User

def is_account_to_follow(user, already_followed = [], accounts_to_skip = []):
    '''
    `user` is a User object for an account

    `already_followed` list of account handle strings that this account has already followed in the past

    `accounts_to_skip` - list of account handle strings that this account should not follow
    '''
    # If the user doesn't follow me, AND
    # I don't follow them, AND
    # I've never followed them before, AND
    # they're not a protected account, AND
    # the user IS NOT in the accounts to skip
    # they're a candidate to follow

    # Additionally, errored out User creation will have a blank
    # url, so skip those

    if not user.following_me \
    and not user.following_them \
    and not user.protected_account \
    and user.handle not in already_followed \
    and user.handle not in accounts_to_skip \
    and user.handle != "":
        return True
    else:
        return False



def meets_additional_account_following_criteria(num_posts, num_likes, num_followers, days_since_most_recent_activity):
    '''
    After accounts have met basic criteria and saved to accounts_to_follow.xlsx, 
    they can be further scraped to see if they meet additional criteria. This speeds
    up following by making all opened tabs for following useful accounts and allows
    pre-processing of that data beforehand

    Allows for extreme values in any argument to immediately make them validated 
    to allow for bypassing later page loads to crawl things like likes pages

    Returns
    ----
    `True` - if all elements were successfully crawled and criteria is met

    `False` - if all elements were successfully crawled and criteria is NOT met

    `None` - if criteria wasn't successfully crawled
    '''
    # Special cases
    if num_posts >= 1000 and days_since_most_recent_activity <= 7:
        return True
    elif num_likes >= 1000 and days_since_most_recent_activity <= 7:
        return True
    elif num_followers >= 1000 and days_since_most_recent_activity <= 7:
        return True


    elif num_posts < 0 or num_likes < 0 or num_followers < 0 or days_since_most_recent_activity < 0:
        # Error cases
        return None
    else:
        # Criteria for following
        if num_posts > 100 and num_likes > 100 and num_followers > 100 and days_since_most_recent_activity < 60:
            return True
        else:
            return False


