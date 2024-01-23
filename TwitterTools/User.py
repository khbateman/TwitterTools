class User:
    def __init__(self, handle, following_me = False, following_them = False, protected_account = False):
        '''
        Note - following is whether the account is following ME
        following_them is whether I follow them
        '''
        self.handle = handle
        self.url = f"https://twitter.com/{handle}"
        self.following_me = following_me
        self.following_them = following_them
        self.protected_account = protected_account
    
    @classmethod
    def from_url(cls, url, following_me = False, following_them = False, protected_account = False):
        handle = url.split("twitter.com/")[1]
        # If there are additional slashes after the user name, remove everything after that
        handle = handle.split("/")[0]
        return cls(handle=handle, following_me=following_me, following_them=following_them, protected_account=protected_account)

    def __str__(self):
        return "Handle: @" + self.handle + "\nURL: " + self.url + "\nFollowing me: " + str(self.following_me) + "\nFollowing them: " + str(self.following_them)