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
        # handle relative urls
        if url[0] == "/":
            handle = url.lstrip("/")
        else:
            # handle Twitter urls
            handle = url.split("twitter.com/")[1]

        # If there are additional slashes after the user name, remove everything after that
        handle = handle.split("/")[0]
        return cls(handle=handle, following_me=following_me, following_them=following_them, protected_account=protected_account)

    def __str__(self):
        return "Handle: @" + self.handle + "\nURL: " + self.url + "\nFollowing me: " + str(self.following_me) + "\nFollowing them: " + str(self.following_them)
    
    def __eq__(self, other):
        handles_equal = self.handle == other.handle
        urls_equal = self.url == other.url
        following_me_equal = self.following_me == other.following_me
        following_them_equal = self.following_them == other.following_them
        protected_equal = self.protected_account == other.protected_account

        return handles_equal and urls_equal and following_me_equal and following_them_equal and protected_equal