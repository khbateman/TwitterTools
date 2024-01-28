import pytest
import time
import os
from TwitterTools import data_tools
import pandas as pd
import shutil

@pytest.fixture(scope="function")
def create_working_dir(tmpdir_factory):
    # Create the directory
    my_tmpdir = tmpdir_factory.mktemp("tmp_directory")

    # Navigate to it to run from within that directory
    os.chdir(my_tmpdir)
    yield my_tmpdir 

@pytest.fixture(scope="function")
def create_working_dir_with_data_dir(tmpdir_factory):
    # Create the directory
    my_tmpdir = tmpdir_factory.mktemp("tmp_directory")

    # Navigate to it to run from within that directory
    os.chdir(my_tmpdir)

    os.mkdir(data_tools._get_data_dir_name())

    yield my_tmpdir


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
