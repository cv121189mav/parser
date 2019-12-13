import sqlalchemy as db

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy.orm import sessionmaker

from webdriver_manager.chrome import ChromeDriverManager

from models import Category
from settings import DATABASE_URL, PARSING_CATEGORY_URL


def parse_category():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver, 30)

    engine = db.create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    def has_subcategory():
        return bool(driver.find_elements_by_class_name('x-category-tile__item'))

    def get_category(parent=None):
        return [
            Category(link=sub_cat.get_attribute('href'), parent=parent)
            for sub_cat in driver.find_elements_by_class_name('x-category-tile__title')
        ]

    def record_to_db(parent=None):
        session.bulk_save_objects(get_category(parent))
        session.commit()
        query = session.query(Category)

        if parent:
            query = query.filter(Category.parent == parent)
        return query.all()

    # get into categories URL
    driver.get(PARSING_CATEGORY_URL)

    # record categories of main level to db
    category_list_db = record_to_db()

    # get list of categories main level from db

    # loop through all categories and record them into db
    for category in category_list_db:
        driver.get(category.link)

        sub_categories = record_to_db(parent=category.parent) if has_subcategory() else []
        category_list_db.extend(sub_categories)


def parse_product():
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
    pass