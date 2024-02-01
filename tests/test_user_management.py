import pytest
from datetime import datetime, timedelta
from TwitterTools import user_management, User, data_tools
from .test_data_tools import copy_file_from_testing_resources_to_tmp_dir

USER_TEST_CASES = [([True, True, True, True], False),
                   ([True, True, False, True], False),
                   ([True, False, True, True], False),
                   ([True, False, False, True], False),
                   ([False, True, True, True], False),
                   ([False, True, False, True], False),
                   ([False, False, True, True], False),
                   ([False, False, False, True], True),
                   ]

@pytest.mark.parametrize('test_case', USER_TEST_CASES)
def test_is_account_to_follow(test_case):
    # Create the user
    user = User.User("kenanbateman", 
                     following_me=test_case[0][0],
                     following_them=test_case[0][1],
                     protected_account=test_case[0][2],
                     verified=test_case[0][3])
    
    assert user_management.is_account_to_follow(user) == test_case[1]

@pytest.mark.parametrize('test_case', USER_TEST_CASES)
def test_is_account_to_follow_already_followed(test_case):
    # Create the user
    user = User.User("kenanbateman", 
                     following_me=test_case[0][0],
                     following_them=test_case[0][1],
                     protected_account=test_case[0][2],
                     verified=test_case[0][3])
    
    assert user_management.is_account_to_follow(user, already_followed=["kenanbateman"]) == False


@pytest.mark.parametrize('test_case', USER_TEST_CASES)
def test_is_account_to_follow_accounts_to_skip(test_case):
    # Create the user
    user = User.User("kenanbateman", 
                     following_me=test_case[0][0],
                     following_them=test_case[0][1],
                     protected_account=test_case[0][2],
                     verified=test_case[0][3])
    
    assert user_management.is_account_to_follow(user, accounts_to_skip=["kenanbateman"]) == False



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
    
    unfollow_df = user_management.get_df_of_user_to_unfollow()

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

    unfollow_df = user_management.get_df_of_user_to_unfollow()

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

    unfollow_df = user_management.get_df_of_user_to_unfollow()

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
    

    unfollow_df = user_management.get_df_of_user_to_unfollow(handles_to_skip=["kenanbateman", "some_account_not_in_the_list", "KaiGolfHQ"])

    expected = ["https://twitter.com/Rackaveli919"]

    assert len(expected) == unfollow_df.shape[0]
    assert set(unfollow_df["url"]).issubset(set(expected))