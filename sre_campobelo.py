# sre_campobelo.py
from bs4 import BeautifulSoup
import requests
import time

BASE_URL = "https://srecampobelo.educacao.mg.gov.br/index.php/licitacoes"
CARDS_PER_PAGE = 6


def get_website_content_campobelo(start_param=0):
    url = f"{BASE_URL}?start={start_param}" if start_param else BASE_URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar conteúdo de {url}: {e}")
        return None


def scrape_website_cards_campobelo(max_pages=10):
    all_cards = []
    page_number = 0
    while page_number < max_pages:
        print(f"Raspando página: {page_number + 1} (start={page_number * CARDS_PER_PAGE})")
        html_content = get_website_content_campobelo(start_param=page_number * CARDS_PER_PAGE)
        if not html_content:
            print(f"Não foi possível obter o conteúdo da página {page_number + 1}. Interrompendo.")
            break
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article', class_='item')
        if not articles:
            print(f"Nenhum card encontrado na página {page_number + 1}. Interrompendo.")
            break
        for article in articles:
            leia_mais = article.find('a', string=lambda t: t and 'leia mais' in t.lower())
            if leia_mais and leia_mais.has_attr('href'):
                href = leia_mais['href']
                if not href.startswith('http'):
                    href = f"https://srecampobelo.educacao.mg.gov.br{href}"
                try:
                    detalhe_resp = requests.get(href, timeout=10)
                    detalhe_resp.raise_for_status()
                    detalhe_soup = BeautifulSoup(detalhe_resp.text, 'html.parser')
                    detalhe_card = detalhe_soup.find('article', class_='item')
                    card_html = str(detalhe_card) if detalhe_card else detalhe_resp.text[:2000]
                except Exception as e:
                    print(f"Erro ao buscar detalhes do card: {e}")
                    card_html = f"<div>Erro ao buscar detalhes: {e}</div>"
            else:
                card_html = str(article)
            all_cards.append({'full_html_content': card_html})
            time.sleep(0.5)  # Evita sobrecarga no servidor
        page_number += 1
    return all_cards
