import User

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# import time
# import pandas as pd
# import numpy as np
# import pickle
# from datetime import datetime, timedelta
# import math
# import os
# from requests import request
# import json
# import keyring
# import random


# def create_driver():
#     # Launch driver and open webpage
#     options = webdriver.safari.options.Options()
#     driver = webdriver.Safari(options=options)
#     driver.implicitly_wait(5) # wait for 5 seconds to find objects that may take time to load before throwing exception

#     # Make window big enough to see
#     driver.set_window_size(1600,1000)

#     return driver


# def log_in_twitter(driver, username, password, sleep_time = 2):
#     driver.get("https://twitter.com/login")
#     time.sleep(sleep_time)
#     driver.find_element(By.TAG_NAME, "input").send_keys(f"{username}\n")
#     # driver.find_element(By.TAG_NAME, "input").send_keys("\n")
#     time.sleep(sleep_time)
#     driver.find_element(By.TAG_NAME, "input").send_keys(f"{password}\n")
#     time.sleep(1)