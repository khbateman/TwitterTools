import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def create_driver():
    # Launch driver and open webpage
    options = webdriver.safari.options.Options()
    driver = webdriver.Safari(options=options)

    # wait for 0.01 seconds to find objects that may take 
    # time to load before throwing exception. By setting this
    # essenetially at zero, other waits need to be built into
    # pages that take time to load. But this allows certain functions
    # to quickly "fail" and move on when certain elements aren't found
    # rather than waiting for them to load, when the reality is it's
    # never going to load.
    driver.implicitly_wait(0.01) 

    # Make window big enough to see
    driver.set_window_size(1600,1000)

    return driver


def log_in_twitter(driver, username, password, sleep_time = 2):
    driver.get("https://twitter.com/login")
    time.sleep(sleep_time)
    driver.find_element(By.TAG_NAME, "input").send_keys(f"{username}\n")
    # driver.find_element(By.TAG_NAME, "input").send_keys("\n")
    time.sleep(sleep_time)
    driver.find_element(By.TAG_NAME, "input").send_keys(f"{password}\n")
    time.sleep(1)