import requests
from bs4 import BeautifulSoup

from models.reader import Reader


class URLReader(Reader):
    def __init__(self, url: str):
        self.__url = url

    def read(self) -> str:
        return self.__get_url_endpoint_content()

    def __get_url_endpoint_content(self) -> str:
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
