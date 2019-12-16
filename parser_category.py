import sqlalchemy as db

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy.orm import sessionmaker

from webdriver_manager.chrome import ChromeDriverManager

from models import Category
from settings import DATABASE_URL, PARSING_CATEGORY_URL





class Parser:

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.engine = db.create_engine(DATABASE_URL)
        # check if category has subcategory

    def has_subcategory(self):
        return bool(self.driver.find_elements_by_class_name('x-category-tile__item'))

    def parse_category(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # get category or subcategory
        def get_category(parent=None):
            return [
                Category(link=sub_cat.get_attribute('href'), parent=parent)
                for sub_cat in self.driver.find_elements_by_class_name('x-category-tile__title')
            ]

        # record data to database
        def record_to_db(parent=None):
            session.bulk_save_objects(get_category(parent))
            session.commit()
            query = session.query(Category)
            return query.filter(Category.parent == parent) if parent else query.all()

        # get into categories URL
        self.driver.get(PARSING_CATEGORY_URL)

        # record categories of main level to db
        category_list_db = record_to_db()

        # loop through all categories and record subcategories into db if they exist
        for category in category_list_db:
            self.driver.get(category.link)

            sub_categories = record_to_db(parent=category.parent) if self.has_subcategory() else []
            category_list_db.extend(sub_categories)
        return category_list_db


    def parse_product(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        # wait = WebDriverWait(driver, 30)
        # check_height = driver.execute_script("return document.body.scrollHeight;")
        # while True:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     try:
        #         wait.until(lambda driver: driver.execute_script("return document.body.scrollHeight;") > check_height)
        #         check_height = driver.execute_script("return document.body.scrollHeight;")
        #     except TimeoutException:
        #         break

        for link in session.query(Category.link):
            self.driver.get(''.join(link))
            all_goods_info = [a.text for a in
                              self.driver.find_elements_by_css_selector(
                                  '.promoGrid__root--1-Ak8 .promoGrid__item--3H-dV') if not self.has_subcategory()]
        #
        # goods_links = [goods_links for goods_links in all_links
        #                if goods_links.startswith('https://my.prom.ua/remote/context_ads/')]
        #
        # c = dict(zip(all_goods_info, goods_links))
