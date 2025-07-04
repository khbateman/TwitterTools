import pytest
import time
import os
from TwitterTools import data_tools, User
import pandas as pd
import shutil
from datetime import datetime, timedelta
import numpy as np


def copy_file_from_testing_resources_to_tmp_dir(file_name, tmp_dir_path, new_file_name):
    current_dir = os.path.dirname(__file__)
    file_to_copy = os.path.join(current_dir, "Testing_Resources", file_name)

    # copy the file
    shutil.copy(file_to_copy, os.path.join(tmp_dir_path, data_tools._get_data_dir_name()))

    # Rename that copied file
    os.rename(os.path.join(tmp_dir_path, data_tools._get_data_dir_name(), file_name),
              os.path.join(tmp_dir_path, data_tools._get_data_dir_name(), new_file_name))



def lists_match(list1, list2):
    all_items_match = True
    
    if len(list1) == len(list2):
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                all_items_match = False
    else:
        all_items_match = False

    return all_items_match


def compare_tmp_file_with_test_file(tmp_dir, tmp_file_name, testing_file_name, cols_to_ignore = []):
    '''
    Reads in the file located at ./{`tmp_dir`}/{`tmp_file_name`}
    and compares it to the file at tests/Testing_Resources/{`testing_file_name`}

    If certain columns will create comparison issues (ex - datetime values), those can be ignored by passing the column names into `cols_to_ignore`
    '''
    current_dir = os.path.dirname(__file__)
    testing_file_path = os.path.join(current_dir, "Testing_Resources", testing_file_name)
    tmp_file_path = os.path.join(tmp_dir, data_tools._get_data_dir_name(),tmp_file_name)

    tmp_df = pd.read_excel(tmp_file_path)
    test_df = pd.read_excel(testing_file_path)

    # First need to remove any cols that we don't 
    # want to compare
    test_df_cols = list(test_df.columns)
    tmp_df_cols = list(tmp_df.columns)

    for col in cols_to_ignore:
        try:
            test_df_cols.remove(col)
        except:
            pass

        try:
            tmp_df_cols.remove(col)
        except:
            pass
    
    # Need to remove those cols for comparison
    tmp_df = tmp_df.loc[:, tmp_df_cols]
    test_df = test_df.loc[:, test_df_cols]

    # It will read in blank cells as NaN so we need to convert those
    # back to empty string
    tmp_df.fillna("", inplace=True)
    test_df.fillna("", inplace=True)


    try:
        if tmp_df.shape == test_df.shape:

            # Check cols match
            if len(tmp_df.columns) == len(test_df.columns):
                cols_match = True
                for i in range(len(test_df.columns)):
                    if tmp_df.columns[i] != test_df.columns[i]:
                        cols_match = False

                if cols_match:
                    # if we get here, columns and shape match, so check data
                    if np.all(tmp_df.loc[:, tmp_df_cols] == test_df.loc[:, test_df_cols]):
                        return True
    except:
        return False

    return False



def test_create_data_dir_01(create_working_dir):
    # if directory doesn't exist, gets created
    assert data_tools._get_data_dir_name() not in os.listdir()
    data_tools.create_data_dir()
    assert data_tools._get_data_dir_name() in os.listdir()


def test_create_data_dir_02(create_working_dir_with_data_dir):
    # directory already exists, make sure it's still there
    data_tools.create_data_dir()
    assert data_tools._get_data_dir_name() in os.listdir()


def test_create_data_dir_03(create_working_dir_with_data_dir):
    # directory already exists, make sure no files were deleted
    open(f"{data_tools._get_data_dir_name()}/file1.txt", "w")
    open(f"{data_tools._get_data_dir_name()}/file2.txt", "w")
    open(f"{data_tools._get_data_dir_name()}/file3.txt", "w")

    data_tools.create_data_dir()
    assert data_tools._get_data_dir_name() in os.listdir()

    files = set(os.listdir(f"./{data_tools._get_data_dir_name()}"))
    assert files == set(["file1.txt", "file2.txt", "file3.txt"])



def test_create_empty_df_01(create_working_dir_with_data_dir):
    # Check that a proper file gets created with specified cols
    cols = ["a", "b", "c", "some_col"]
    file_name = "test.xlsx"

    data_tools.create_empty_df(file_name, cols)

    df = pd.read_excel(f"{data_tools._get_data_dir_name()}/{file_name}")

    assert df.shape == (0, len(cols))
    assert set(df.columns) == set(cols)


def test_rename_file_with_appended_num_01(create_working_dir_with_data_dir):
    open(f"{data_tools._get_data_dir_name()}/conflict.xlsx", "w")

    data_tools.rename_file_with_appended_num("conflict.xlsx")

    assert "conflict_01.xlsx" in os.listdir(f"{data_tools._get_data_dir_name()}")


def test_rename_file_with_appended_num_02(create_working_dir_with_data_dir):
    open(f"{data_tools._get_data_dir_name()}/conflict.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_01.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_02.xlsx", "w")

    data_tools.rename_file_with_appended_num("conflict.xlsx")

    assert "conflict_03.xlsx" in os.listdir(f"{data_tools._get_data_dir_name()}")


def test_rename_file_with_appended_num_03(create_working_dir_with_data_dir):
    open(f"{data_tools._get_data_dir_name()}/conflict.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_01.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_02.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_03.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_04.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_05.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_06.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_07.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_08.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_09.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_10.xlsx", "w")
    open(f"{data_tools._get_data_dir_name()}/conflict_11.xlsx", "w")

    data_tools.rename_file_with_appended_num("conflict.xlsx")

    assert "conflict_12.xlsx" in os.listdir(f"{data_tools._get_data_dir_name()}")


def test_rename_file_with_appended_num_04(create_working_dir_with_data_dir):
    # Make sure no data is lost
    with open(f"{data_tools._get_data_dir_name()}/conflict.txt", "w") as f:
        f.write("this is a test")

    open(f"{data_tools._get_data_dir_name()}/conflict_01.txt", "w")

    data_tools.rename_file_with_appended_num("conflict.txt")

    assert "conflict_02.txt" in os.listdir(f"{data_tools._get_data_dir_name()}")

    with open(f"{data_tools._get_data_dir_name()}/conflict_02.txt", "r") as f:
        assert f.readlines()[0] == "this is a test"



def test_copy_file_from_testing_resources_to_tmp_dir_01(create_working_dir_with_data_dir):
    assert "abc.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    copy_file_from_testing_resources_to_tmp_dir("following_01.xlsx", 
                            tmp_dir_path=create_working_dir_with_data_dir, 
                            new_file_name="abc.xlsx")
    
    assert "abc.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))


def test_validate_or_create_file_01(create_working_dir_with_data_dir):
    # File isn't there at all, create empty file

    # Make sure it's not there to start
    assert "following.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))
    
    data_tools.validate_or_create_file("following.xlsx", data_tools._get_following_cols())

    # Should be there now
    assert "following.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    # Make sure it has ONLY the correct columns
    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))

    assert lists_match(df.columns, data_tools._get_following_cols())



def test_validate_or_create_file_02(create_working_dir_with_data_dir):
    # Example where file exists, but the columns are wrong

    # Make sure it's not there to start
    assert "following.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    copy_file_from_testing_resources_to_tmp_dir("following_02.xlsx",
                                                tmp_dir_path=create_working_dir_with_data_dir,
                                                new_file_name="following.xlsx")

    # Should be there now
    assert "following.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))
    orig_shape = df.shape

    # Those columns should be wrong
    assert not lists_match(df.columns, data_tools._get_following_cols())

    # Run method
    data_tools.validate_or_create_file("following.xlsx", data_tools._get_following_cols())

    
    # Should be fixed now
    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))
    assert lists_match(df.columns, data_tools._get_following_cols())

    # Data shouldn't be lost since the original data should be preserved
    assert orig_shape[0] == df.shape[0]



def test_validate_or_create_file_03(create_working_dir_with_data_dir):
    # Example where file exists, but the columns are wrong

    # Make sure it's not there to start
    assert "following.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    copy_file_from_testing_resources_to_tmp_dir("following_03.xlsx",
                                                tmp_dir_path=create_working_dir_with_data_dir,
                                                new_file_name="following.xlsx")

    # Should be there now
    assert "following.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))
    orig_shape = df.shape

    # Those columns should be wrong
    assert not lists_match(df.columns, data_tools._get_following_cols())

    # Run method
    data_tools.validate_or_create_file("following.xlsx", data_tools._get_following_cols())

    
    # Should be fixed now
    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))
    assert lists_match(df.columns, data_tools._get_following_cols())

    # Data shouldn't be lost since the original data should be preserved
    assert orig_shape[0] == df.shape[0]


def test_validate_or_create_file_04(create_working_dir_with_data_dir):
    # Example where file exists, but the columns are wrong

    # Make sure it's not there to start
    assert "following.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    copy_file_from_testing_resources_to_tmp_dir("following_04.xlsx",
                                                tmp_dir_path=create_working_dir_with_data_dir,
                                                new_file_name="following.xlsx")

    # Should be there now
    assert "following.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))
    orig_shape = df.shape

    # Those columns should be wrong
    assert not lists_match(df.columns, data_tools._get_following_cols())

    # Run method
    data_tools.validate_or_create_file("following.xlsx", data_tools._get_following_cols())

    
    # Should be fixed now
    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))
    assert lists_match(df.columns, data_tools._get_following_cols())

    # Data shouldn't be lost since the original data should be preserved
    assert orig_shape[0] == df.shape[0]



def test_validate_or_create_file_05(create_working_dir_with_data_dir):
    # A column is MISSING from exising file, so file should be preserved
    # and new empty file should be created

    # Make sure it's not there to start
    assert "following.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    copy_file_from_testing_resources_to_tmp_dir("following_05.xlsx",
                                                tmp_dir_path=create_working_dir_with_data_dir,
                                                new_file_name="following.xlsx")

    # Should be there now
    assert "following.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))
    orig_shape = df.shape

    # Those columns should be wrong
    assert not lists_match(df.columns, data_tools._get_following_cols())

    # Run method
    data_tools.validate_or_create_file("following.xlsx", data_tools._get_following_cols())

    # Orig file should have been preserved
    assert "following_01.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))
    assert "following.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))
    
    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following_01.xlsx"))
    orig_shape_after_dup = df.shape
    assert orig_shape == orig_shape_after_dup

    
    # Should be fixed now
    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))
    assert lists_match(df.columns, data_tools._get_following_cols())

    assert orig_shape_after_dup != df.shape


def test_setup_data_files_01(create_working_dir):
    # Base setup with nothing set up, no directory or files

    # Make sure the directory isn't there
    assert data_tools._get_data_dir_name() not in os.listdir(create_working_dir)

    # Run it
    data_tools.setup_data_files()

    # Directory should be there now
    assert data_tools._get_data_dir_name() in os.listdir(create_working_dir)

    # Make sure proper files are there
    files_in_dir = os.listdir(os.path.join(create_working_dir, data_tools._get_data_dir_name()))
    assert set(["following.xlsx", "accounts_to_follow.xlsx", "accounts_to_skip.xlsx"]).issubset(set(files_in_dir))


def test_setup_data_files_02(create_working_dir_with_data_dir):
    # Example with 1 file present
    assert "following.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    copy_file_from_testing_resources_to_tmp_dir("following_01.xlsx",
                                                tmp_dir_path=create_working_dir_with_data_dir,
                                                new_file_name="following.xlsx")
    
    # Make sure it's there now and others aren't
    assert "following.xlsx" in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))
    assert "accounts_to_follow.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))
    assert "accounts_to_skip.xlsx" not in os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    # Run it
    data_tools.setup_data_files()


    # Make sure proper files are there
    files_in_dir = os.listdir(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name()))

    assert set(["following.xlsx", "accounts_to_follow.xlsx", "accounts_to_skip.xlsx"]).issubset(set(files_in_dir))


def test_save_df_to_excel_01(create_working_dir_with_data_dir):
    # Read the file and save it right back to make sure there are no issues
    data_tools.setup_data_files()

    df = pd.read_excel(os.path.join(create_working_dir_with_data_dir, data_tools._get_data_dir_name(), "following.xlsx"))

    row = pd.DataFrame([["somehandle", "someurl.com", True, True, '2023-09-15 08:00:00']], columns = df.columns)

    df = pd.concat([df, row])

    data_tools.save_df_to_excel(df, "following.xlsx")

    # just making sure nothing errors out, no assertion


def test_combine_dataframes_01():
    df1 = pd.DataFrame([[1, 2, 3, 4, 5]], columns = ["a", "b", "c", "d", "e"])
    df2 = pd.DataFrame([[6, 7, 8, 9, 10]], columns = ["f", "g", "h", "i", "j"])

    final_df = data_tools.combine_dataframes(df1, df2)

    # Make sure data is there and columns are correct
    assert final_df.shape == (2, 5)
    assert final_df.columns[0] == "a"
    assert final_df.columns[1] == "b"
    assert final_df.columns[2] == "c"
    assert final_df.columns[3] == "d"
    assert final_df.columns[4] == "e"


def test_combine_dataframes_02():
    df1 = pd.DataFrame([[1, 2, 3, 4, 5]], columns = ["a", "b", "c", "d", "e"])
    df2 = pd.DataFrame([[6, 7, 8, 9, 10], [11, 12, 13, 14, 15]], columns = ["f", "g", "h", "i", "j"])

    final_df = data_tools.combine_dataframes(df1, df2)

    # Make sure data is there and columns are correct
    assert final_df.shape == (3, 5)
    assert final_df.columns[0] == "a"
    assert final_df.columns[1] == "b"
    assert final_df.columns[2] == "c"
    assert final_df.columns[3] == "d"
    assert final_df.columns[4] == "e"


def test_combine_dataframes_03():
    # Columns match but in different order
    df1 = pd.DataFrame([[1, 2, 3, 4, 5]], columns = ["a", "b", "c", "d", "e"])
    df2 = pd.DataFrame([[6, 7, 8, 9, 10]], columns = ["a", "c", "b", "e", "d"])

    final_df = data_tools.combine_dataframes(df1, df2)

    # Make sure data is there and columns are correct
    assert final_df.shape == (2, 5)
    assert final_df.columns[0] == "a"
    assert final_df.columns[1] == "b"
    assert final_df.columns[2] == "c"
    assert final_df.columns[3] == "d"
    assert final_df.columns[4] == "e"

    # Make sure cols were mapped correctly
    assert final_df.iloc[1, 0] == 6
    assert final_df.iloc[1, 1] == 8
    assert final_df.iloc[1, 2] == 7
    assert final_df.iloc[1, 3] == 10
    assert final_df.iloc[1, 4] == 9


def test_combine_dataframes_04():
    df1 = pd.DataFrame([[1, 2, 3, 4, 5]], columns = ["a", "b", "c", "d", "e"])
    df2 = pd.DataFrame([[6, 7, 8, 9, 10, 11]])

    final_df = data_tools.combine_dataframes(df1, df2)

    # Too many columns in df2, result should be df1
    assert final_df.shape == (1, 5)
    assert final_df.columns[0] == "a"
    assert final_df.columns[1] == "b"
    assert final_df.columns[2] == "c"
    assert final_df.columns[3] == "d"
    assert final_df.columns[4] == "e"
    assert final_df.iloc[0, 0] == 1
    assert final_df.iloc[0, 1] == 2
    assert final_df.iloc[0, 2] == 3
    assert final_df.iloc[0, 3] == 4
    assert final_df.iloc[0, 4] == 5

def test_combine_dataframes_05():
    df1 = pd.DataFrame([[1, 2, 3, 4, 5]], columns = ["a", "b", "c", "d", "e"])
    df2 = pd.DataFrame([[6, 7, 8, 9, 10, 11]], columns = ["a", "b", "c", "d", "f", "e"])

    final_df = data_tools.combine_dataframes(df1, df2)

    # Too many columns in df2, BUT the columns from df1 are there
    # column f should be dropped and the rest mapped to append the df
    assert final_df.shape == (2, 5)
    assert final_df.columns[0] == "a"
    assert final_df.columns[1] == "b"
    assert final_df.columns[2] == "c"
    assert final_df.columns[3] == "d"
    assert final_df.columns[4] == "e"
    assert final_df.iloc[1, 0] == 6
    assert final_df.iloc[1, 1] == 7
    assert final_df.iloc[1, 2] == 8
    assert final_df.iloc[1, 3] == 9
    assert final_df.iloc[1, 4] == 11



def test_users_list_to_following_df_01():
    user_1 = User.User("johnsmith")
    user_2 = User.User("jessicaDavis", following_me=True, verified=True)
    user_3 = User.User("UNC_athletics", following_them=True, protected_account=True)

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, False, datetime.now()],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", True, False, datetime.now()],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", False, True, datetime.now()]],
        columns = data_tools._get_following_cols())
    
    output_df = data_tools.users_list_to_following_df([user_1, user_2, user_3])

    cols_to_compare = data_tools._get_following_cols()
    cols_to_compare.remove("followed_before")


    assert np.all(df.loc[:, cols_to_compare] == output_df.loc[:, cols_to_compare])
    
    # Date col is omitted above since it will always vary slightly 
    # with repeated use of datetime.now(). Just check date matches (not time)
    assert output_df.loc[0, "followed_before"].year == datetime.now().year
    assert output_df.loc[0, "followed_before"].month == datetime.now().month
    assert output_df.loc[0, "followed_before"].day == datetime.now().day


def test_users_list_to_following_df_02():
    # This should return an empty df, not fail
    
    output_df = data_tools.users_list_to_following_df([1, 2, 3])

    assert output_df.shape == (0, 5)
    assert set(output_df.columns).issubset(set(data_tools._get_following_cols()))

def test_users_list_to_following_df_03():
    # Test to see if extra non-User elements don't fail, and everything else still gets populated
    user_1 = User.User("johnsmith")
    user_2 = User.User("jessicaDavis", following_me=True, verified=True)
    user_3 = User.User("UNC_athletics", following_them=True, protected_account=True)

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, False, datetime.now()],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", True, False, datetime.now()],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", False, True, datetime.now()]],
        columns = data_tools._get_following_cols())
    
    output_df = data_tools.users_list_to_following_df([user_1, 2, user_2, 3, user_3, 4])

    cols_to_compare = data_tools._get_following_cols()
    cols_to_compare.remove("followed_before")


    assert np.all(df.loc[:, cols_to_compare] == output_df.loc[:, cols_to_compare])
    
    # Date col is omitted above since it will always vary slightly 
    # with repeated use of datetime.now(). Just check date matches (not time)
    assert output_df.loc[0, "followed_before"].year == datetime.now().year
    assert output_df.loc[0, "followed_before"].month == datetime.now().month
    assert output_df.loc[0, "followed_before"].day == datetime.now().day


def test_testing_func_compare_tmp_file_with_test_file_01(create_working_dir_with_data_dir):
    data_tools.setup_data_files()
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_empty.xlsx")


def test_testing_func_compare_tmp_file_with_test_file_02(create_working_dir_with_data_dir):
    data_tools.setup_data_files()
    assert not compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_05.xlsx")


def test_testing_func_compare_tmp_file_with_test_file_03(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("following_04.xlsx", create_working_dir_with_data_dir, "following.xlsx")

    # Same data but cols flipped
    assert not compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_01.xlsx")

def test_testing_func_compare_tmp_file_with_test_file_04(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("following_02.xlsx", create_working_dir_with_data_dir, "following.xlsx")

    # Cols don't match (extra)
    assert not compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_01.xlsx")


def test_testing_func_compare_tmp_file_with_test_file_05(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("following_02.xlsx", create_working_dir_with_data_dir, "following.xlsx")

    # Cols don't match (extra col, but it's ignored, so it should match)
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_01.xlsx", cols_to_ignore = ["extra_col"])

def test_testing_func_compare_tmp_file_with_test_file_06(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("following_02.xlsx", create_working_dir_with_data_dir, "following.xlsx")

    # Same as above test, but col name is wrong, so it doesn't match anything
    # So now nothing should be removed and they should again not match
    assert not compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_01.xlsx", cols_to_ignore = ["extra_cols"])


def test_following_users_df_to_excel_01(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, False, datetime(2024, 1, 29, 8, 4)],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", True, False, datetime(2024, 1, 29, 8, 3)],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", False, True, datetime(2024, 1, 29, 8, 2)]],
        columns = data_tools._get_following_cols())

    data_tools.following_users_df_to_excel(df)

    # Basic test where existing following.xlsx is empty and the new rows are added
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_06.xlsx", cols_to_ignore = ["followed_before"])


def test_following_users_df_to_excel_02(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    df = pd.DataFrame(columns = data_tools._get_following_cols())

    copy_file_from_testing_resources_to_tmp_dir("following_06.xlsx", create_working_dir_with_data_dir, "following.xlsx")

    data_tools.following_users_df_to_excel(df)

    # Basic test where existing following.xlsx has rows already
    # and new dataframe is empty. So it should stay the same
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_06.xlsx", cols_to_ignore = ["followed_before"])


def test_following_users_df_to_excel_03(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, False],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", True, False],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", False, True]],
        columns = ["handle", "url", "following_me", "following_them"])

    
    copy_file_from_testing_resources_to_tmp_dir("following_01.xlsx", create_working_dir_with_data_dir, "following.xlsx")

    data_tools.following_users_df_to_excel(df)

    # Basic test where existing following.xlsx has rows already
    # and new dataframe has incorrect columns. So nothing is added.
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_01.xlsx", cols_to_ignore = ["followed_before"])


def test_following_users_df_to_excel_04(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, False, datetime(2024, 1, 29, 8, 4)],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", True, False, datetime(2024, 1, 29, 8, 3)],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", False, True, datetime(2024, 1, 29, 8, 2)]],
        columns = data_tools._get_following_cols())
    
    copy_file_from_testing_resources_to_tmp_dir("following_01.xlsx", create_working_dir_with_data_dir, "following.xlsx")

    data_tools.following_users_df_to_excel(df)

    # Basic test where existing following.xlsx has rows already
    # and new dataframe is added successfully
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_07.xlsx", cols_to_ignore = ["followed_before"])


def test_following_users_df_to_excel_05(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    df = pd.DataFrame([
        ["kenanbateman", "https://twitter.com/kenanbateman", False, True, datetime(2024, 1, 29, 8, 6)],
        ["someaccount", "https://twitter.com/someaccount", True, True, datetime(2024, 1, 29, 8, 5)],
        ["johnsmith", "https://twitter.com/johnsmith", False, True, datetime(2024, 1, 29, 8, 4)],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", True, True, datetime(2024, 1, 29, 8, 3)],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", True, True, datetime(2024, 1, 30, 8, 2)]], # making newest to test which one is kept
        columns = data_tools._get_following_cols())
    
    copy_file_from_testing_resources_to_tmp_dir("following_07.xlsx", create_working_dir_with_data_dir, "following.xlsx")

    data_tools.following_users_df_to_excel(df)

    # Check that correct duplicates removed, and new data is still added
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "following.xlsx", "following_08.xlsx", cols_to_ignore = ["followed_before"])


def test_users_list_to_accounts_to_follow_df_01():
    user_1 = User.User("johnsmith")
    user_2 = User.User("jessicaDavis", following_me=True, verified=True)
    user_3 = User.User("UNC_athletics", following_them=True, protected_account=True)

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, False, "this is a source"],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", False, False, "this is a source"],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", True, False, "this is a source"]],
        columns = data_tools._get_accounts_to_follow_cols())
    
    output_df = data_tools.users_list_to_accounts_to_follow_df([user_1, user_2, user_3], source = "this is a source", ready_to_follow=False)

    assert np.all(df == output_df)



def test_users_list_to_accounts_to_follow_df_02():
    user_1 = User.User("johnsmith")
    user_2 = User.User("jessicaDavis", following_me=True, verified=True)
    user_3 = User.User("UNC_athletics", following_them=True, protected_account=True)

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, False, "this is a source"],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", False, False, "this is a source"],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", True, False, "this is a source"]],
        columns = data_tools._get_accounts_to_follow_cols())
    
    # Same as above test, but throw in non-User elements to make sure it doesn't fail
    output_df = data_tools.users_list_to_accounts_to_follow_df([user_1, 1, user_2, 2, 3, user_3, 4], source = "this is a source", ready_to_follow=False)

    assert np.all(df == output_df)


def test_users_list_to_accounts_to_follow_df_03():
    user_1 = User.User("johnsmith")
    user_2 = User.User("jessicaDavis", following_me=True, verified=True)
    user_3 = User.User("UNC_athletics", following_them=True, protected_account=True)

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, True, "this is a source"],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", False, True, "this is a source"],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", True, True, "this is a source"]],
        columns = data_tools._get_accounts_to_follow_cols())
    
    # Same as #1, but change ready_to_follow arg
    output_df = data_tools.users_list_to_accounts_to_follow_df([user_1, user_2, user_3], source = "this is a source", ready_to_follow=True)

    assert np.all(df == output_df)



def test_accounts_to_follow_df_to_excel_01(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    df = pd.DataFrame([
        ["johnsmith", "https://twitter.com/johnsmith", False, True, "this is a source"],
        ["jessicaDavis", "https://twitter.com/jessicaDavis", False, False, "this is a source"],
        ["UNC_athletics", "https://twitter.com/UNC_athletics", False, True, "this is a source"],
        ["UNC_athletics_followed", "https://twitter.com/UNC_athletics", True, True, "this is a source"]],
        columns = data_tools._get_accounts_to_follow_cols())

    data_tools.accounts_to_follow_df_to_excel(df)

    # Basic test where existing file is empty and the new rows are added
    # Note the followed row will NOT be added
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_01.xlsx")


def test_accounts_to_follow_df_to_excel_02(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_01.xlsx", create_working_dir_with_data_dir, "accounts_to_follow.xlsx")

    df = pd.DataFrame(columns = data_tools._get_accounts_to_follow_cols())
    data_tools.accounts_to_follow_df_to_excel(df)

    # Existing file has data, but new df is empty. Should match original file
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_01.xlsx")


def test_accounts_to_follow_df_to_excel_03(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_01.xlsx", create_working_dir_with_data_dir, "accounts_to_follow.xlsx")

    df = pd.DataFrame([
        ["some_acct1", "https://twitter.com/some_acct1", False, True, "this is a source", 0],
        ["some_acct2", "https://twitter.com/some_acct2", False, True, "this is a source", 0],
        ["some_acct3", "https://twitter.com/some_acct3", True, True, "this is a source", 0]], # won't be added because already followed
        columns = data_tools._get_accounts_to_follow_cols() + ["extra_col"])

    data_tools.accounts_to_follow_df_to_excel(df)

    # Basic test where existing file has rows already
    # and new dataframe has incorrect columns. 
    # However, it has the base columns, just an extra one
    # Extra col will be ignored and others will be used to add data
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_04.xlsx")


def test_accounts_to_follow_df_to_excel_04(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_01.xlsx", create_working_dir_with_data_dir, "accounts_to_follow.xlsx")

    df = pd.DataFrame([
        ["some_acct1", "https://twitter.com/some_acct1", False, True],
        ["some_acct2", "https://twitter.com/some_acct2", False, True],
        ["some_acct3", "https://twitter.com/some_acct3", True, True]],
        columns = ["handle", "url", "followed", "ready_to_follow"])
    
    data_tools.accounts_to_follow_df_to_excel(df)

    # Similar example to above, but one less col rather than extra 
    # Basic test where existing file has rows already
    # and new dataframe has incorrect columns. So nothing is added.
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_01.xlsx")



def test_accounts_to_follow_df_to_excel_05(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_01.xlsx", create_working_dir_with_data_dir, "accounts_to_follow.xlsx")

    df = pd.DataFrame([
        ["some_acct1", "https://twitter.com/some_acct1", False, True, "abc source"],
        ["some_acct2", "https://twitter.com/some_acct2", True, True, "abc source"],
        ["some_acct3", "https://twitter.com/some_acct3", False, False, "abc source"]],
        columns = data_tools._get_accounts_to_follow_cols())
    
    data_tools.accounts_to_follow_df_to_excel(df)

    # Basic test where existing file has rows already
    # and new dataframe is added successfully
    # Note row 2 WON'T be added because it's already followed
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_02.xlsx")


def test_accounts_to_follow_df_to_excel_06(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_01.xlsx", create_working_dir_with_data_dir, "accounts_to_follow.xlsx")

    df = pd.DataFrame([
        ["some_acct1", "https://twitter.com/some_acct1", False, True, "abc source"],

        # Duplicate
        ["johnsmith", "https://twitter.com/johnsmith", False, False, "this is a DIFFERENT source"],

        # Won't be added because already followed
        ["some_acct2", "https://twitter.com/some_acct2", True, True, "abc source"],

        # Duplicate
        ["UNC_athletics", "https://twitter.com/UNC_athletics", False, False, "this is a DIFFERENT source"],

        ["some_acct3", "https://twitter.com/some_acct3", False, False, "abc source"]],
        columns = data_tools._get_accounts_to_follow_cols())
    

    data_tools.accounts_to_follow_df_to_excel(df)


    # Basic test where existing file has rows already
    # and new dataframe is added successfully
    # THERE ARE DUPLICATES THAT SHOULD BE REMOVED
    # Note some_acct2 WON'T be added because it's already followed
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_02.xlsx")


def test_accounts_to_follow_df_to_excel_07(create_working_dir_with_data_dir):
    data_tools.setup_data_files()

    # Example where now John Smith is FOLLOWED to start, will be dropped
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_01b.xlsx", create_working_dir_with_data_dir, "accounts_to_follow.xlsx")

    df = pd.DataFrame([
        ["some_acct1", "https://twitter.com/some_acct1", False, True, "abc source"],

        # Duplicate, but he's now not followed in the one being added
        # Still should not be added (logically this makes sense because
        # if someone were already followed in the saved data, we're not
        # going to follow them again even if they're not followed now. 
        # They'd be filtered out anyways by their handle being in prev.
        # followed accounts)
        ["johnsmith", "https://twitter.com/johnsmith", False, False, "this is a DIFFERENT source"],

        # Won't be added because already followed
        ["some_acct2", "https://twitter.com/some_acct2", True, True, "abc source"],

        # Duplicate
        ["UNC_athletics", "https://twitter.com/UNC_athletics", False, False, "this is a DIFFERENT source"],

        ["some_acct3", "https://twitter.com/some_acct3", False, False, "abc source"]],
        columns = data_tools._get_accounts_to_follow_cols())
    

    data_tools.accounts_to_follow_df_to_excel(df)


    # Basic test where existing file has rows already
    # and new dataframe is added successfully
    # THERE ARE DUPLICATES THAT SHOULD BE REMOVED
    # Note some_acct2 WON'T be added because it's already followed
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_03.xlsx")


def test_get_handles_list_01(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_skip_01.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx")

    accounts = data_tools.get_handles_list("accounts_to_skip.xlsx")

    assert accounts == ["some_account_1", "abc", "another_account", "last_one"]


def test_get_handles_list_02(create_working_dir_with_data_dir_and_files):
    # Empty test
    accounts = data_tools.get_handles_list("accounts_to_skip.xlsx")

    assert accounts == []


def test_get_handles_list_03(create_working_dir_with_data_dir):
    # File isn't there, should be empty, not fail
    accounts = data_tools.get_handles_list("accounts_to_skip.xlsx")

    assert accounts == []

def test_get_handles_list_04(create_working_dir_with_data_dir):
    # File isn't there, should be empty, not fail
    accounts = data_tools.get_handles_list("blah")

    assert accounts == []


def test_get_handles_list_05(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("following_01.xlsx", create_working_dir_with_data_dir_and_files, "following.xlsx")

    accounts = data_tools.get_handles_list("following.xlsx")

    assert accounts == ["Rackaveli919", "KaiGolfHQ", "oceanmicrobes", "ADW_4", "almightyy_zach"]

def test_get_handles_list_06(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_01.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    accounts = data_tools.get_handles_list("accounts_to_follow.xlsx")

    assert accounts == ["johnsmith", "jessicaDavis", "UNC_athletics"]



def test_update_accounts_to_follow_excel_from_user_list_01(create_working_dir_with_data_dir):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_04.xlsx", create_working_dir_with_data_dir, "accounts_to_follow.xlsx")

    user_1 = User.User("account_1")
    user_2 = User.User("account_2", following_me=True) # skipped
    user_3 = User.User("account_3", following_them=True) #skipped
    user_4 = User.User("account_4", protected_account=True) #skipped
    user_5 = User.User("account_5") # in already followed
    user_6 = User.User("account_6") # in accounts to skip
    user_8 = User.User("account_8", verified=True)
    user_9 = User.User("jessicaDavis") # already in file, will be skipped in excel saving

    data_tools.update_accounts_to_follow_excel_from_user_list(
        users = [user_1, user_2, user_3, user_4, user_5, user_6, user_8, user_9], 
        source = "source #2", 
        ready_to_follow = False,
        validate_users = True,
        accounts_following = ["something", "something_else", "account_5", "another_account"],
        accounts_to_skip = ["abc", "123", "account_6", "account_100"])

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_05.xlsx")


def test_update_accounts_to_follow_excel_from_user_list_02(create_working_dir_with_data_dir):
    # Same test as #1 but without validating users
    # and changing ready to follow to true to make sure that's passed in
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_04.xlsx", create_working_dir_with_data_dir, "accounts_to_follow.xlsx")

    user_1 = User.User("account_1")
    user_2 = User.User("account_2", following_me=True) # skipped

    # will still be dropped because following them is filtered
    # out during saving
    user_3 = User.User("account_3", following_them=True) 
    user_4 = User.User("account_4", protected_account=True) #skipped
    user_5 = User.User("account_5") # in already followed
    user_6 = User.User("account_6") # in accounts to skip
    user_8 = User.User("account_8", verified=True)
    user_9 = User.User("jessicaDavis") # already in file, will be skipped in excel saving'

    data_tools.update_accounts_to_follow_excel_from_user_list(
        users = [user_1, user_2, user_3, user_4, user_5, user_6, user_8, user_9], 
        source = "source #2", 
        ready_to_follow = True,
        validate_users = False,
        accounts_following = ["something", "something_else", "account_5", "another_account"],
        accounts_to_skip = ["abc", "123", "account_6", "account_100"])

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir, "accounts_to_follow.xlsx", "accounts_to_follow_06.xlsx")


def test_get_urls_of_user_to_unfollow_01(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("following_09.xlsx",
                        tmp_dir_path=create_working_dir_with_data_dir_and_files,
                        new_file_name="following.xlsx")

    # Need to change some rows of the file since the date needs to be relative
    # to the test, not fixed
    df = data_tools.get_following_df()
    df.loc[df["handle"] == "KaiGolfHQ", "followed_before"] = datetime.now() - timedelta(days=2)
    df.loc[df["handle"] == "oceanmicrobes", "followed_before"] = datetime.now() - timedelta(days=2)
    df.loc[df["handle"] == "ADW_4", "followed_before"] = datetime.now() - timedelta(days=2)
    df.loc[df["handle"] == "almightyy_zach", "followed_before"] = datetime.now() - timedelta(days=2)

    # save this back to following before the function is called for the test
    data_tools.save_df_to_excel(df, "following.xlsx")

    unfollow_df = data_tools.get_df_of_user_to_unfollow()

    expected = ["https://twitter.com/Rackaveli919", "https://twitter.com/kenanbateman"]

    assert len(expected) == unfollow_df.shape[0]
    assert set(unfollow_df["url"]).issubset(set(expected))


def test_get_urls_of_user_to_unfollow_02(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("following_09.xlsx",
                        tmp_dir_path=create_working_dir_with_data_dir_and_files,
                        new_file_name="following.xlsx")

    # Make everyone's date 2 days ago
    df = data_tools.get_following_df()
    df.loc[:, "followed_before"] = datetime.now() - timedelta(days=2)

    # save this back to following before the function is called for the test
    data_tools.save_df_to_excel(df, "following.xlsx")

    unfollow_df = data_tools.get_df_of_user_to_unfollow()

    assert unfollow_df.shape[0] == 0


def test_get_urls_of_user_to_unfollow_03(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("following_09.xlsx",
                        tmp_dir_path=create_working_dir_with_data_dir_and_files,
                        new_file_name="following.xlsx")

    # Make everyone following me
    df = data_tools.get_following_df()
    df.loc[:, "following_me"] = True

    # save this back to following before the function is called for the test
    data_tools.save_df_to_excel(df, "following.xlsx")

    unfollow_df = data_tools.get_df_of_user_to_unfollow()

    assert unfollow_df.shape[0] == 0


def test_get_urls_of_user_to_unfollow_04(create_working_dir_with_data_dir_and_files):
    # same as test 01, but this time the users are in the handles_to_skip arg
    copy_file_from_testing_resources_to_tmp_dir("following_09.xlsx",
                        tmp_dir_path=create_working_dir_with_data_dir_and_files,
                        new_file_name="following.xlsx")

    # Need to change some rows of the file since the date needs to be relative
    # to the test, not fixed
    df = data_tools.get_following_df()
    df.loc[df["handle"] == "KaiGolfHQ", "followed_before"] = datetime.now() - timedelta(days=2)
    df.loc[df["handle"] == "oceanmicrobes", "followed_before"] = datetime.now() - timedelta(days=2)
    df.loc[df["handle"] == "ADW_4", "followed_before"] = datetime.now() - timedelta(days=2)
    df.loc[df["handle"] == "almightyy_zach", "followed_before"] = datetime.now() - timedelta(days=2)

    # save this back to following before the function is called for the test
    data_tools.save_df_to_excel(df, "following.xlsx")


    unfollow_df = data_tools.get_df_of_user_to_unfollow(handles_to_skip=["kenanbateman", "some_account_not_in_the_list", "KaiGolfHQ"])

    expected = ["https://twitter.com/Rackaveli919"]

    assert len(expected) == unfollow_df.shape[0]
    assert set(unfollow_df["url"]).issubset(set(expected))


def test_add_user_to_accounts_to_skip_01(create_working_dir_with_data_dir_and_files):
    data_tools.add_user_to_accounts_to_skip("some_handle")

    # Empty file with one user added
    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx", "accounts_to_skip_02.xlsx")


def test_add_user_to_accounts_to_skip_02(create_working_dir_with_data_dir_and_files):
    # File with users to start, make sure they stay and new one is added
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_skip_01.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx")


    data_tools.add_user_to_accounts_to_skip("some_handle")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx", "accounts_to_skip_03.xlsx")


def test_add_user_to_accounts_to_skip_03(create_working_dir_with_data_dir_and_files):
    # File with users to start, make sure they stay and new one is added
    # Adding multiple users in a row
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_skip_01.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx")


    data_tools.add_user_to_accounts_to_skip("some_handle")
    data_tools.add_user_to_accounts_to_skip("some_handle2")
    data_tools.add_user_to_accounts_to_skip("some_handle3")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx", "accounts_to_skip_04.xlsx")


def test_add_user_to_accounts_to_skip_04(create_working_dir_with_data_dir_and_files):
    # File with users to start, make sure they stay and new one is added
    # Making sure duplicates aren't added
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_skip_01.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx")

    data_tools.add_user_to_accounts_to_skip("some_handle")
    data_tools.add_user_to_accounts_to_skip("some_handle2")
    data_tools.add_user_to_accounts_to_skip("some_handle3")
    data_tools.add_user_to_accounts_to_skip("some_handle")
    data_tools.add_user_to_accounts_to_skip("some_handle2")
    data_tools.add_user_to_accounts_to_skip("some_handle3")


    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx", "accounts_to_skip_04.xlsx")


def test_add_user_to_accounts_to_skip_05(create_working_dir_with_data_dir_and_files):
    # File with users to start
    # Making sure duplicates aren't added (trying handle that was already to start)
    # Nothing should change
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_skip_01.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx")

    data_tools.add_user_to_accounts_to_skip("another_account")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_skip.xlsx", "accounts_to_skip_01.xlsx")




STRINGS = [("36.5K posts", 36500),
           ("1.2K posts", 1200),
           ("12.1K likes", 12100),
           ("6.5K likes", 6500),
           ("1,212 posts", 1212),
           ("4,365 likes", 4365),
           ("804 posts", 804),
           ("79 likes", 79),
           ("0 posts", 0),
           ("0 likes", 0),
           ("42.6K Followers", 42600),
           ("1.8M Followers", 1800000),
           ("2M", 2000000),
           ("8.7K", 8700),
]

@pytest.mark.parametrize('test_case', STRINGS)
def test_parse_string_number_to_int(test_case):
    assert data_tools.parse_string_number_to_int(test_case[0]) == test_case[1]

def test_parse_string_number_to_int_failure_01():
    with pytest.raises(Exception):
        data_tools.parse_string_number_to_int("No number here Followers")

def test_parse_string_number_to_int_failure_02():
    with pytest.raises(Exception):
        data_tools.parse_string_number_to_int("Zero Followers")

def test_parse_string_number_to_int_failure_03():
    with pytest.raises(Exception):
        data_tools.parse_string_number_to_int("")

def test_parse_string_number_to_int_failure_04():
    with pytest.raises(Exception):
        data_tools.parse_string_number_to_int("m followers")

def test_parse_string_number_to_int_failure_05():
    with pytest.raises(Exception):
        data_tools.parse_string_number_to_int("k followers")



def test_update_accounts_to_follow_row_01(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # valid handle with no other arguments, nothing should change
    data_tools.update_accounts_to_follow_row(handle = "UNC_athletics")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07a.xlsx")


def test_update_accounts_to_follow_row_02(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # invalid handle with no other arguments, nothing should change
    data_tools.update_accounts_to_follow_row(handle = "UNC_athletics_doesnt_exist")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07a.xlsx")


def test_update_accounts_to_follow_row_03(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Valid handle with new url
    data_tools.update_accounts_to_follow_row(handle = "UNC_athletics",
                                             url = "https://twitter.com/UNC_athletics_new_url")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07b.xlsx")


def test_update_accounts_to_follow_row_04(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Valid handle with new followed (shouldn't be deleted with followed filter)
    data_tools.update_accounts_to_follow_row(handle = "some_acct2",
                                             followed = True)

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07c.xlsx")


def test_update_accounts_to_follow_row_05(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Valid handle with new ready_to_follow
    data_tools.update_accounts_to_follow_row(handle = "account_6",
                                             ready_to_follow = False)

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07d.xlsx")


def test_update_accounts_to_follow_row_06(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Valid handle with new source
    data_tools.update_accounts_to_follow_row(handle = "some_acct1",
                                             source = "some new source")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07e.xlsx")


def test_update_accounts_to_follow_row_07(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Valid handle with new source
    data_tools.update_accounts_to_follow_row(handle = "some_acct1",
                                             source = "some new source")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07e.xlsx")


def test_update_accounts_to_follow_row_08(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Valid handle with multiple new values
    data_tools.update_accounts_to_follow_row(handle = "jessicaDavis",
                                             url = "newurl.com", 
                                             followed = True, 
                                             ready_to_follow = True, 
                                             source = "this source changed")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07f.xlsx")


def test_update_accounts_to_follow_row_09(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Valid handle with multiple new values, but one is invalid, nothing should update
    data_tools.update_accounts_to_follow_row(handle = "jessicaDavis",
                                             url = "newurl.com", 
                                             followed = 'invalid value', 
                                             ready_to_follow = True, 
                                             source = "this source changed")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07a.xlsx")

def test_update_accounts_to_follow_row_10(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07a.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Valid handle with multiple new values, but one is invalid, nothing should update
    data_tools.update_accounts_to_follow_row(handle = "jessicaDavis",
                                             url = "newurl.com", 
                                             followed = True, 
                                             ready_to_follow = 99, 
                                             source = "this source changed")

    assert compare_tmp_file_with_test_file(create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx", "accounts_to_follow_07a.xlsx")



def test_get_rows_to_validate_01(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07g.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Getting all the rows
    df = data_tools.get_rows_to_validate()

    assert df.shape[0] == 3


def test_get_rows_to_validate_02(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07g.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Getting a subset
    df = data_tools.get_rows_to_validate(2)

    assert df.shape[0] == 2

def test_get_rows_to_validate_03(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07g.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Getting a single row
    df = data_tools.get_rows_to_validate(1)

    assert df.shape[0] == 1


def test_get_rows_to_validate_04(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07g.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Getting no rows
    df = data_tools.get_rows_to_validate(0)

    assert df.shape[0] == 0

def test_get_rows_to_validate_05(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07h.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # No rows meet criteria, all ready_to_follow == True
    df = data_tools.get_rows_to_validate()

    assert df.shape[0] == 0

def test_get_rows_to_validate_06(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07i.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # No rows meet criteria, all followed == True
    df = data_tools.get_rows_to_validate()

    assert df.shape[0] == 0


def test_get_rows_to_validate_07(create_working_dir_with_data_dir_and_files):
    copy_file_from_testing_resources_to_tmp_dir("accounts_to_follow_07g.xlsx", create_working_dir_with_data_dir_and_files, "accounts_to_follow.xlsx")

    # Getting more rows than are present
    df = data_tools.get_rows_to_validate(999)

    assert df.shape[0] == 3


def test_get_rows_to_validate_08(create_working_dir_with_data_dir_and_files):

    # No rows, should be empty
    df = data_tools.get_rows_to_validate()

    assert df.shape[0] == 0