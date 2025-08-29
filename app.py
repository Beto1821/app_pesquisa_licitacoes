# app.py
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import re
import os # Importar a biblioteca os

app = Flask(__name__)


# URL base do site de licitações
BASE_URL = "https://srevarginha.educacao.mg.gov.br/index.php/licitacoes"
CARDS_PER_PAGE = 6  # Número de cards por página


def get_website_content(start_param=0):
    """
    Faz uma requisição HTTP para a URL de licitações.
    Usa o parâmetro de paginação.
    """
    url = f"{BASE_URL}?start={start_param}"
    try:
        response = requests.get(url, timeout=10)
        # Lança um HTTPError para respostas de erro (4xx ou 5xx)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar conteúdo de {url}: {e}")
        return None


def scrape_website_cards(max_pages_to_scrape=9):
    """
    Raspa cards de múltiplas páginas do site de licitações.
    A paginação é controlada pelo parâmetro 'start'.
    """
    all_cards_data = []
    page_number = 0

    while page_number < max_pages_to_scrape:
        print(
            f"Raspando página: {page_number + 1} "
            f"(start={page_number * CARDS_PER_PAGE})"
        )
        html_content = get_website_content(
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
            return all_cards_data

        for card_article in current_page_articles:
            # Adiciona classes CSS nos <p> desejados
            for p in card_article.find_all('p'):
                if "CAIXA ESCOLAR" in p.get_text():
                    p['class'] = p.get('class', []) + ['caixa-escolar']
                if p.get_text().strip().startswith("ATÉ"):
                    p['class'] = p.get('class', []) + ['data-ate']

            # HTML original do card (agora com classes)
            full_html_content = str(card_article)

            # Extrai título e especificação para busca
            title_tag = card_article.find('h2', class_='item-title')
            title = title_tag.get_text(strip=True) if title_tag else 'Sem Título'
            content_text = card_article.get_text(" ", strip=True)

            # Regex para especificação
            specification_match = re.search(
                r'ESPECIFICAÇÃO DO OBJETO:\s*(.*?)(?=(?:PRAZO PARA APRESENTAÇÃO|'
                r'INFORMAÇÕES DE CONDIÇÃO DE CONTRATAÇÃO|NÚMERO DO TERMO DE COMPROMISSO|'
                r'LOCAL:|OBSERVAÇÃO:|AVISO DE PUBLICAÇÃO|$))',
                content_text,
                re.IGNORECASE | re.DOTALL
            )
            specification_text = ""
            if specification_match:
                specification_text = specification_match.group(1).strip()
            else:
                simple_spec_match = re.search(
                    r'ESPECIFICAÇÃO DO OBJETO:\s*(.*)',
                    content_text,
                    re.IGNORECASE | re.DOTALL
                )
                if simple_spec_match:
                    specification_text = simple_spec_match.group(1).strip()

            all_cards_data.append({
                'title': title,
                'specification': specification_text,
                'full_html_content': full_html_content
            })

        # Se o número de cards raspados for menor que o esperado por página,
        # assumimos que é a última página
        if len(current_page_articles) < CARDS_PER_PAGE:
            print(
                f"Menos de {CARDS_PER_PAGE} cards na página "
                f"{page_number + 1}. Fim da paginação."
            )
            return all_cards_data

        page_number += 1

    return all_cards_data


@app.route('/', methods=['GET', 'POST'])
def index():
    search_term = ""
    filtered_cards = []
    
    # Recebe o valor do dropdown do formulário, se existir
    try:
        max_pages = int(request.form.get('max_pages', 9))
    except (TypeError, ValueError):
        max_pages = 9
    all_cards = scrape_website_cards(max_pages_to_scrape=max_pages)

    if request.method == 'POST':
        search_term = request.form.get('search_query', '').lower()
        if search_term:
            for card in all_cards:
                # Busca apenas na parte da ESPECIFICAÇÃO DO OBJETO
                if search_term in card['specification'].lower():
                    filtered_cards.append(card)
        else:
            # Se o termo de busca estiver vazio, mostra todos os cards
            filtered_cards = all_cards
    else:
        # Na primeira carga da página, mostra todos os cards
        filtered_cards = all_cards

    return render_template(
        'index.html',
        cards=filtered_cards,
        search_query=search_term
    )


if __name__ == '__main__':
    # Esta linha só será executada quando o script for rodado diretamente (localmente).
    # Em ambientes de produção como o Railway, o Gunicorn inicia a aplicação.
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port) # Mudado debug para False e host para '0.0.0.0'
