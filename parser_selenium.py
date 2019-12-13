from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 30)
# driver.get('https://prom.ua/promo/free-delivery')

# check_height = driver.execute_script("return document.body.scrollHeight;")
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     try:
#         wait.until(lambda driver: driver.execute_script("return document.body.scrollHeight;")  > check_height)
#         check_height = driver.execute_script("return document.body.scrollHeight;")
#     except TimeoutException:
#         break
#
# all_links = [a.get_attribute('href') for a in driver.find_elements_by_xpath("//a[@href]")]
# all_goods_info = [a.text for a in driver.find_elements_by_css_selector('.promoGrid__root--1-Ak8 .promoGrid__item--3H-dV')]
#
# goods_links = [goods_links for goods_links in all_links
#                if goods_links.startswith('https://my.prom.ua/remote/context_ads/')]
#
# c = dict(zip(all_goods_info, goods_links))


def has_subcategory():
    return True if driver.find_elements_by_class_name('x-category-tile__item') else False


def get_category():
    return [sub_cat.get_attribute('href') for sub_cat in driver.find_elements_by_class_name('x-category-tile__title')]


driver.get('https://prom.ua/consumer-goods')

all_categories = get_category()
sub_categories = []
sub_sub_categories = []
sub_sub_sub_categories = []

for category in all_categories:
    driver.get(category)
    sub_categories = get_category() if has_subcategory() else []
    for sub_sub_category in sub_categories:
        driver.get(sub_sub_category)
        sub_sub_categories = get_category() if has_subcategory() else []
        for sub_sub_sub_category in sub_sub_categories:
            sub_sub_sub_categories = get_category() if has_subcategory() else []

all_categories = all_categories + sub_categories + sub_sub_categories + sub_sub_sub_categories

print(len(set(all_categories)))




