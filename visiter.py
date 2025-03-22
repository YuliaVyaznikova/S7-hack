import requests
from bs4 import BeautifulSoup
from smolagents import tool
from finder import random_delay

@tool
def visit_web_page(url: str) -> list:
    '''
    This tool can be used to visit page on web by the url. It returns text of the page.
    But not in raw format, not html, only content
    
    Args:
        url: url to the website.
    Returns:
        function is returning a list of all paragraphs of the page
    '''
    random_delay(0.1, 1)
    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')  # Создаем объект BeautifulSoup

        paragraphs = soup.find_all('p')
        lst = []
        for p in paragraphs:
            lst.append(p.get_text())
        return lst

    except requests.exceptions.RequestException as e:
        return f"error, cannot access URL: {url}, exception {e}"
    
if __name__ == '__main__':
    res = visit_web_page('https://www.airlinequality.com/airline-reviews/s7-siberia-airlines/')
    print(res)

