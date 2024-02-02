from datetime import datetime, timedelta

# Other TwitterTools imports
from .User import User
from .data_tools import *

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



def get_df_of_user_to_unfollow(handles_to_skip = [], unfollow_after_days = 7):
    '''
    Args
    ----
    `handles_to_skip` - list of twitter handles that should be skipped because they should be followed regardless of whather they meet unfollowing rules
        format example - `["johnsmith", "hornets", ...]`

    Returns
    ----
    Dataframe of the rows of users that are eligible to unfollow.
    
    This dataframe has extra columns from processing in this function (skip, time_following)
    '''
    # Read in overall following list
    df = get_following_df()

    # add column for whether or not account is in the skip argument
    df["skip"] = df["handle"].isin(handles_to_skip)

    # Add calculated row
    df["time_following"] = datetime.today() - df["followed_before"]

    # Vectorized calculation for to filter which rows should be unfollowed
    unfollow_rows = df[(df["following_me"] == False) &
                       (df["currently_following"] == True) & 
                       (df["time_following"] > timedelta(days=unfollow_after_days)) &
                       (df["skip"] == False)]
    
    # Sort from the oldest to newest follow
    unfollow_rows = unfollow_rows.sort_values(by=['followed_before'])
    
    return unfollow_rows
