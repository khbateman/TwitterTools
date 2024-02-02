
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



