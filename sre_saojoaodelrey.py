# sre_saojoaodelrey.py
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://sresjdelrei.educacao.mg.gov.br/index.php/licitacoes"
CARDS_PER_PAGE = 6

def get_website_content_saojoaodelrey(start_param=0):
    url = f"{BASE_URL}?start={start_param}" if start_param else BASE_URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar conteúdo de {url}: {e}")
        return None

def scrape_website_cards_saojoaodelrey(max_pages=8):
    all_cards = []
    page_number = 0
    while page_number < max_pages:
        print(f"Raspando página: {page_number + 1} (start={page_number * CARDS_PER_PAGE})")
        html_content = get_website_content_saojoaodelrey(start_param=page_number * CARDS_PER_PAGE)
        if not html_content:
            print(f"Não foi possível obter o conteúdo da página {page_number + 1}. Interrompendo.")
            break
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article', class_='item')
        if not articles:
            print(f"Nenhum card encontrado na página {page_number + 1}. Interrompendo.")
            break
        for article in articles:
            card_html = str(article)
            all_cards.append({'full_html_content': card_html})
        page_number += 1
    return all_cards
