# sre_pocoscaldas.py
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://srepocoscaldas.educacao.mg.gov.br/index.php/licitacoes"
CARDS_PER_PAGE = 6


def get_website_content_pocoscaldas(start_param=0):
    url = f"{BASE_URL}?start={start_param}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar conteúdo de {url}: {e}")
        return None


def scrape_website_cards_pocoscaldas(max_pages_to_scrape=9):
    all_cards_data = []
    page_number = 0
    while page_number < max_pages_to_scrape:
        print(
            f"Raspando página: {page_number + 1} "
            f"(start={page_number * CARDS_PER_PAGE})"
        )
        html_content = get_website_content_pocoscaldas(
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
            leia_mais_link = None
            link_tag = article.find('a', href=True)
            if link_tag:
                href = link_tag['href']
                if href.startswith('http'):
                    leia_mais_link = href
                else:
                    href_clean = href.lstrip('/')
                    leia_mais_link = (
                        'https://srepocoscaldas.educacao.mg.gov.br/'
                        f'{href_clean}'
                    )
            all_cards_data.append({
                'leia_mais_link': leia_mais_link
            })
        page_number += 1
    return all_cards_data
