import pandas as pd
from datetime import datetime
import numpy as np
import os

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



def update_following_excel_file(driver = None, scraped_twitter_following = None):
    '''
    `scraped_twitter_users` can be provided (list of type User)

    If it's not provided, a driver needs to be provided to scrape the current
    Twitter users
    '''
    if scraped_twitter_following is None:
        scraped_twitter_following = scrape_follow_pages(driver)

    # Read previously scraped following from Excel file
    df = pd.read_excel("following.xlsx", parse_dates=["followed_before"])

    # Need to set everyone in "currently_following" to False and will
    # update based on the ones that are actually being followed right now
    # since this will change run to run
    df["currently_following"] = False
    
    today = datetime.today()

    for user in scraped_twitter_following:

        if np.any(df["handle"] == user.handle):
            # If user is already in the dataframe, update them
            df.loc[df["handle"] == user.handle, "currently_following"] = True
            df.loc[df["handle"] == user.handle, "following_me"] = user.following_me
        else:
            # User isn't in the dataframe, add them
            tmp_row = pd.DataFrame([[user.handle, user.url, user.following_me, True, today]], columns=["handle", "url", "following_me", "currently_following", "followed_before"])

            df = pd.concat([df, tmp_row], axis = 0)

            # Need to reset the index each time since the queries 
            # if they are already present could otherwise mess up
            df.reset_index(drop=True, inplace=True)
    
    save_df_to_excel(df)