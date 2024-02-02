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



