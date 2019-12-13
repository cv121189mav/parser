from bs4 import BeautifulSoup
import user_agent
import requests


class ParserWeb:

    def init(self):
        pass

    category_links_origin = []
    category_links_figured = []
    start_link = 'https://prom.ua/promo'

    useragent = user_agent.generate_user_agent(device_type='desktop')
    headers = {'User-Agent': useragent}
    req = requests.get('https://prom.ua/consumer-goods/', headers=headers)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    def get_links_origin(self):
        for link in self.soup.find_all('a', class_='x-category-tile__title'):
            self.category_links_origin.append(link.get('href'))
        return self.category_links_origin

    def get_valid_link(self):
        for i in self.category_links_origin:
            self.category_links_figured.append(self.start_link + i) if not i.startswith(self.start_link) \
                else self.category_links_figured.append(i)
        return self.category_links_figured


c = ParserWeb()
c.get_links_origin()
first_tree_category_links = c.get_valid_link()

for i in first_tree_category_links:
    req = requests.get(i)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', class_='promoPageTile__tileLink--2msRL')]
