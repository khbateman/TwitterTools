import pandas as pd
from datetime import datetime
import numpy as np

def save_df_to_excel(df):
    # Sort by date and clean up index values (from adding rows)
    df.sort_values(by = ["followed_before"], ascending = False, inplace=True)
    df.reset_index(drop=True, inplace = True)

    # Save it and size excel columns so data is viewable
    # Use this writer so certain column widths can be set
    writer = pd.ExcelWriter('following.xlsx')
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Get the column widths
    for column in df:
        column_length = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)

    # The above method doesn't set the first 2 columnS correctly, so hardcode those
    # writer.sheets['Sheet1'].set_column(df.columns.get_loc("date"), df.columns.get_loc("date"), 19.0)
    # writer.sheets['Sheet1'].set_column(df.columns.get_loc("tweet"), df.columns.get_loc("tweet"), 124.0)
    
    writer.save() 



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