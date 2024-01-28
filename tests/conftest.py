import pytest
from TwitterTools import driver_tools

# As a session scope, the driver gets set up once and can be re-used through all tests
@pytest.fixture(scope="session")
def get_driver():
    driver = driver_tools.create_driver()
    driver.implicitly_wait(0.01) # since everything is local, don't need to wait for other things to load
    return driver