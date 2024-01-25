import pytest
from TwitterTools import crawler

# As a session scope, the driver gets set up once and can be re-used through all tests
@pytest.fixture(scope="session")
def get_driver():
    driver = crawler.create_driver()
    driver.implicitly_wait(0.01) # since everything is local, don't need to wait for other things to load
    return driver