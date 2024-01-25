from TwitterTools import crawler
from selenium.webdriver.common.by import By
import os

# def test_user_crawler_01():
#     # crawler.create_driver()
#     current_dir = os.path.dirname(__file__)
#     with open(os.path.join(current_dir, "Testing_Resources/user_09_not-verified_follows-me_not-following-them_protected.html")) as f:
#         html = f.readlines()[0]

#         driver = crawler.create_driver()
#         driver.get("data:text/html;charset=utf-8," + html)
#         div = driver.find_element(By.XPATH, "*")
#         crawler.create_user_from_div(div)

#         print(div.find_element(By.CSS_SELECTOR, "a").get_attribute(name="href"))



    # crawler.create_user_from_div(div)
    # print("here")


# test_user_crawler_01()

