import pandas as pd
from datetime import datetime
import numpy as np
import os

from .user_management import is_account_to_follow

def _get_data_dir_name():
    return "TwitterTools_data"

def _get_following_cols():
    return ["handle", "url", "following_me", "currently_following", "followed_before"]

def _get_accounts_to_follow_cols():
    return ["handle", "url", "followed", "ready_to_follow", "source"]

def _get_accounts_to_skip_cols():
    return ["handle"]


def create_data_dir():
    '''
    Creates the directory for the data files if it does not exist
    '''
    if _get_data_dir_name() not in os.listdir():
        os.mkdir(_get_data_dir_name())



def create_empty_df(file_name, cols):
    tmp_df = pd.DataFrame(columns = cols)
    tmp_df.to_excel(f"{_get_data_dir_name()}/{file_name}",
                    index = False)



def rename_file_with_appended_num(file_name):
    '''
    Renames argument file (in the data directory) with an 
    underscore and next available number
    '''
    new_file_name_num = 1
    while new_file_name_num < 100:
        file_pre_extension = file_name.split('.')[0]
        file_extension = file_name.split('.')[1]
        if new_file_name_num < 10:
            new_file_name = f"{file_pre_extension}_0{new_file_name_num}.{file_extension}"
        else:
            new_file_name = f"{file_pre_extension}_{new_file_name_num}.{file_extension}"
        
        if new_file_name not in os.listdir(f"{_get_data_dir_name()}"):
            os.rename(f"{_get_data_dir_name()}/{file_name}", f"{_get_data_dir_name()}/{new_file_name}")
            return new_file_name
        else:
            new_file_name_num += 1


def get_following_df():
    '''
    Returns dataframe of data from `following.xlsx`
    '''
    # Read in existing data
    following_file_path = os.path.join(_get_data_dir_name(), "following.xlsx")

    return pd.read_excel(following_file_path, parse_dates=["followed_before"])

def get_accounts_to_follow_df():
    '''
    Returns dataframe of data from `accounts_to_follow.xlsx`
    '''
    # Read in existing data
    following_file_path = os.path.join(_get_data_dir_name(), "accounts_to_follow.xlsx")

    return pd.read_excel(following_file_path,)


def get_handles_list(file_name):
    '''
    Returns list of handles from specified file (following.xlsx, accounts_to_skip.xlsx, accounts_to_follow.xlsx)
    '''
    try:
        # Read in existing data
        following_file_path = os.path.join(_get_data_dir_name(), file_name)

        df = pd.read_excel(following_file_path)

        return list(df["handle"])
    except:
        return []




def validate_or_create_file(file_name, cols):
    '''
    Checks that the file exists and has only the columns specified
    '''
    if file_name not in os.listdir(_get_data_dir_name()):
        # file doesn't exist, need to create it
        create_empty_df(file_name, cols)
    else:
        # File exists, validate it
        df = pd.read_excel(os.path.join(_get_data_dir_name(), file_name))

        # Check if all the columns needed are present
        if set(cols).issubset(set(df.columns)):
            # all columns are here, re-arrange them and save
            rearranged_df = df[cols]
            rearranged_df.to_excel(os.path.join(_get_data_dir_name(), file_name), index=False)
        else:
            # something is missing. Rename orig, and create empty
            rename_file_with_appended_num(file_name)
            create_empty_df(file_name, cols)



def setup_data_files():
    # creates directory if it doesn't exist
    create_data_dir() 

    # Create files if they don't exist and/or don't match correct cols
    validate_or_create_file("following.xlsx", _get_following_cols())
    validate_or_create_file("accounts_to_follow.xlsx", _get_accounts_to_follow_cols())
    validate_or_create_file("accounts_to_skip.xlsx", _get_accounts_to_skip_cols())


def save_df_to_excel(df, file_name):
    # For the following.xlsx file, sort by the date they were followed
    try:
        # Sort by date and clean up index values (from adding rows)
        df.sort_values(by = ["followed_before"], ascending = False, inplace=True)
    except:
        pass

    # Clean up index values
    df.reset_index(drop=True, inplace = True)

    # Save it and size excel columns so data is viewable
    # Use this writer so certain column widths can be set
    writer = pd.ExcelWriter(os.path.join(_get_data_dir_name(), file_name))
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Get the column widths
    for column in df:
        column_length = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)

    # The above method doesn't set the first 2 columnS correctly, so hardcode those
    # writer.sheets['Sheet1'].set_column(df.columns.get_loc("date"), df.columns.get_loc("date"), 19.0)
    # writer.sheets['Sheet1'].set_column(df.columns.get_loc("tweet"), df.columns.get_loc("tweet"), 124.0)
    
    writer.close() 


def combine_dataframes(df1, df2):
    '''
    Adds the rows from df2 to the bottom of df1

    If dataframes have the same number of columns, 
    columns will be preserved from df1 and df2 will
    be forced into those columns

    If they have a different number of columns, df1 will be returned
    and df2 will **NOT** be appended

    if df2 has the same columns as df1 but EXTRA columns, the extras
    will be dropped and the remaining df2 will be appended
    '''
    # columns can be mapped. Since they may be in a different order,
    # remap them using df1 cols
    if set(df1.columns).issubset(set(df2.columns)):
        remapped_df2 = df2.loc[:, df1.columns]


        # To avoid concatenating empty dfs, if we know
        # the cols are present, we can return the non-empty df
        if df1.shape[0] == 0:
            final_df = remapped_df2
        elif remapped_df2.shape[0] == 0:
            final_df = df1
        else:
            final_df = pd.concat([df1, remapped_df2], axis = 0)

    # If they have the same number of columns, force df2 to df1 cols
    elif df1.shape[1] == df2.shape[1]:
        df2.columns = df1.columns
        final_df = pd.concat([df1, df2], axis = 0)

    else:
        print("NOTE: The columns of df2 can't be mapped to df1. Returning df1")
        return df1

    # Clean up index values
    final_df.reset_index(drop=True, inplace = True)

    return final_df


def users_list_to_following_df(users):
    '''
    Takes a list of Users and returns a dataframe 
    with expected columns for later processing
    '''
    df = pd.DataFrame(columns = _get_following_cols())

    for user in users:
        try:
            row = pd.DataFrame([[user.handle, user.url, user.following_me, user.following_them, datetime.now()]], columns = _get_following_cols())

            # Empty dataframes throw a warning, so if it's empty, don't concat, just make it the row 
            if df.shape[0] == 0:
                df = row
            else:
                df = combine_dataframes(df, row)
        except:
            pass

    return df


def users_list_to_accounts_to_follow_df(users, source, ready_to_follow = False):
    '''
    Takes a list of Users and returns a dataframe 
    with expected columns for later processing

    `source` - a string representing where the users came from (ex - "Liked post {url}")

    `ready_to_follow` - some users are scraped from places that inherently already make them ready to follow without further analysis. Others may need to be verified further to see if they're useful to follow (ex - they just follow a somewhat similar account)
    '''
    df = pd.DataFrame(columns = _get_accounts_to_follow_cols())

    for user in users:
        try:
            row = pd.DataFrame([[user.handle, user.url, user.following_them, ready_to_follow, source]], columns = _get_accounts_to_follow_cols())

            # Empty dataframes throw a warning, so if it's empty, don't concat, just make it the row 
            if df.shape[0] == 0:
                df = row
            else:
                df = combine_dataframes(df, row)
        except:
            pass
    
    return df


def following_users_df_to_excel(df):
    '''
    Takes in users df (with proper columns, suggested
    to use `users_list_to_following_df` to generate)
    and adds it to following.xlsx without duplicates
    '''
    # Read in existing data
    existing_following_df = get_following_df()

    # Need to set everyone in "currently_following" to False and will
    # update based on the ones that are actually being followed right now
    # since this will change run to run
    existing_following_df["currently_following"] = False
    
    # Combine the two dataframes
    # important to keep existing_following_df FIRST
    # since any issues will preserve that and discard the second df
    final_df = combine_dataframes(existing_following_df, df)

    # Edge case where something caused nothing in df to be added to 
    # the existing df (ex - column mismatch). In this case, it's
    # really an error, so we don't want to save anything and change
    # currently following to false (since we don't *know* that).
    # Since the unchanged file still exists, just return without 
    # doing anything
    try:
        # Need to first check shape since future numpy
        # release will deprecate checking *all* against
        # an empty df
        if final_df.shape[0] > 0:
            if np.all(final_df == existing_following_df):
                return
    except:
        pass
    

    

    # Dropping duplicates
    # Since we want to keep the OLD dates if a user is already there
    # (so repeated crawls don't constantly update an otherwise old 
    # crawled user), but want to keep the NEW following data, have to 
    # sort them by date and create different duplicate dropping rules

    # Sorts new to old
    final_df.sort_values(by = ["followed_before"], ascending = False, inplace=True)

    # isolate duplicated rows
    duplicate_rows_boolean = final_df.duplicated(subset = ["handle"], keep=False)
    duplicate_rows = final_df[duplicate_rows_boolean]

    # Keep the NEW rows from the duplicates (drop old / last rows)
    duplicates_new_rows = duplicate_rows.drop_duplicates(subset = ["handle"], keep='first')

    # Now drop the new duplicates (keep old rows) from the main dataframe and update the old rows with the new data we want to update (following_me / currently_following)
    final_df.drop_duplicates(subset = ["handle"], keep='last', inplace=True)

    for row in duplicates_new_rows.iterrows():
        # Returns an (index, Series) tuple so grab the second entry
        handle = row[1]["handle"]
        final_df.loc[final_df["handle"] == handle, "following_me"] = row[1]["following_me"]
        final_df.loc[final_df["handle"] == handle, "currently_following"] = row[1]["currently_following"]


    save_df_to_excel(final_df, "following.xlsx")



def accounts_to_follow_df_to_excel(df):
    '''
    Takes in df (with proper columns, suggested
    to use `users_list_to_accounts_to_follow_df` to generate)
    and adds it to accounts_to_follow.xlsx without duplicates
    '''
    # Read in existing data
    existing_following_df = get_accounts_to_follow_df()

    # Combine dataframes
    # important to keep existing_following_df FIRST
    # since any issues will preserve that and discard the second df
    final_df = combine_dataframes(existing_following_df, df)

    # Drop duplicates
    final_df.drop_duplicates(subset = ["handle"], keep='first', inplace=True)

    # Remove all users that have already been followed (they've been 
    # evaluated or followed, so they'll show up in one of the other 
    # data stores (ex - following / accounts to skip))
    final_df = final_df[final_df["followed"] == False]

    save_df_to_excel(final_df, "accounts_to_follow.xlsx")



def update_accounts_to_follow_excel_from_user_list(users, source, ready_to_follow = False, validate_users = True, accounts_following = [], accounts_to_skip = []):
    '''
    Takes a list of Users and saves them to accounts_to_follow.xlsx without duplicates

    `users` - list of `Users`

    `source` - a string representing where the users came from (ex - "Liked post {url}")

    `ready_to_follow` - some users are scraped from places that inherently already make them ready to follow without further analysis. Others may need to be verified further to see if they're useful to follow (ex - they just follow a somewhat similar account)

    `validate_users` - some crawling methods validate the users internally, so we can save time by not re-validating in those cases
    '''

    if validate_users:
        checked_users = []
        for user in users:
            # Verify it the account meets criteria for following
            if is_account_to_follow(user, accounts_following, accounts_to_skip):
                checked_users.append(user)
    else:
        checked_users = users

    df = users_list_to_accounts_to_follow_df(checked_users, 
                                            source = source,
                                            ready_to_follow = ready_to_follow)
            
    accounts_to_follow_df_to_excel(df)




# # Old version that is no longer needed, replaced by `following_users_df_to_excel`
# def update_following_excel_file(driver = None, scraped_twitter_following = None):
#     '''
#     `scraped_twitter_users` can be provided (list of type User)

#     If it's not provided, a driver needs to be provided to scrape the current
#     Twitter users
#     '''
#     if scraped_twitter_following is None:
#         scraped_twitter_following = scrape_follow_pages(driver)

#     # Read previously scraped following from Excel file
#     df = pd.read_excel("following.xlsx", parse_dates=["followed_before"])

#     # Need to set everyone in "currently_following" to False and will
#     # update based on the ones that are actually being followed right now
#     # since this will change run to run
#     df["currently_following"] = False
    
#     today = datetime.today()

#     for user in scraped_twitter_following:

#         if np.any(df["handle"] == user.handle):
#             # If user is already in the dataframe, update them
#             df.loc[df["handle"] == user.handle, "currently_following"] = True
#             df.loc[df["handle"] == user.handle, "following_me"] = user.following_me
#         else:
#             # User isn't in the dataframe, add them
#             tmp_row = pd.DataFrame([[user.handle, user.url, user.following_me, True, today]], columns=["handle", "url", "following_me", "currently_following", "followed_before"])

#             df = pd.concat([df, tmp_row], axis = 0)

#             # Need to reset the index each time since the queries 
#             # if they are already present could otherwise mess up
#             df.reset_index(drop=True, inplace=True)
    
#     save_df_to_excel(df)