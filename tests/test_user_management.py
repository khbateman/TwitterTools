import pytest
from TwitterTools import user_management, User

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



USER_TEST_CASES_ADDTL_CRITERIA = [([-1, 0, 0, 0], None),
                                  ([0, -1, 0, 0], None),
                                  ([0, 0, -1, 0], None),
                                  ([0, 0, 0, -1], None),
                                  ([200, 200, 200, 1], True),
                                  ([1, 200, 200, 1], False),
                                  ([200, 1, 200, 1], False),
                                  ([200, 200, 1, 1], False),
                                  ([200, 200, 200, 999], False),
                                  ([1001, -1, -1, 6], True),
                                  ([-1, 1001, -1, 6], True),
                                  ([-1, -1, 1001, 6], True),
                                    ]

@pytest.mark.parametrize('test_case', USER_TEST_CASES_ADDTL_CRITERIA)
def test_is_account_to_follow_accounts_to_skip(test_case):
    # Using above test cases as arguments to the function, make
    # sure the result is the second element in the tuple
    assert user_management.meets_additional_account_following_criteria(
        test_case[0][0],
        test_case[0][1],
        test_case[0][2],
        test_case[0][3]) == test_case[1]