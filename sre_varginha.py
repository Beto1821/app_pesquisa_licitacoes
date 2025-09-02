# sre_varginha.py
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://srevarginha.educacao.mg.gov.br/index.php/licitacoes"
CARDS_PER_PAGE = 6


def get_website_content_varginha(start_param=0):
    url = f"{BASE_URL}?start={start_param}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar conteúdo de {url}: {e}")
        return None


def scrape_website_cards_varginha(max_pages_to_scrape=9):
    all_cards_data = []
    page_number = 0
    while page_number < max_pages_to_scrape:
        print(
            f"Raspando página: {page_number + 1} "
            f"(start={page_number * CARDS_PER_PAGE})"
        )
        html_content = get_website_content_varginha(
            start_param=page_number * CARDS_PER_PAGE
        )
        if not html_content:
            print(
                f"Não foi possível obter o conteúdo da página "
                f"{page_number + 1}. Interrompendo."
            )
            return all_cards_data
        soup = BeautifulSoup(html_content, 'html.parser')
        current_page_articles = soup.find_all('article', class_='item')
        if not current_page_articles:
            print(
                f"Nenhum card encontrado na página "
                f"{page_number + 1}. Interrompendo."
            )
            break
        for article in current_page_articles:
            card_html = str(article)
            all_cards_data.append({
                'full_html_content': card_html
            })
        page_number += 1
    return all_cards_data
