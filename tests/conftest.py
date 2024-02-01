import pytest
import os
from TwitterTools import driver_tools, data_tools

# As a session scope, the driver gets set up once and can be re-used through all tests
# @pytest.fixture(scope="session")
# @pytest.fixture(scope="function")
@pytest.fixture(scope="class")
def get_driver():
    driver = driver_tools.create_driver()
    driver.implicitly_wait(0.01) # since everything is local, don't need to wait for other things to load
    yield driver

    # At the end, close the driver explicitly
    # because some tests run so quickly that the old driver
    # isn't completely closed and it'll fail to create a new one
    # if not done explicitly
    driver.quit()

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


@pytest.fixture(scope="function")
def create_working_dir_with_data_dir_and_files(tmpdir_factory):
    # Create the directory
    my_tmpdir = tmpdir_factory.mktemp("tmp_directory")

    # Navigate to it to run from within that directory
    os.chdir(my_tmpdir)

    os.mkdir(data_tools._get_data_dir_name())

    data_tools.setup_data_files()

    yield my_tmpdir


