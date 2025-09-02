import requests
from flask import Flask, render_template, request, redirect, url_for
from sre_varginha import scrape_website_cards_varginha
from sre_pocoscaldas import scrape_website_cards_pocoscaldas

app = Flask(__name__)


# URL base do site de licitações
BASE_URL = "https://srevarginha.educacao.mg.gov.br/index.php/licitacoes"
CARDS_PER_PAGE = 6  # Número de cards por página


def get_website_content(start_param=0):
    """
    Faz uma requisição HTTP para a URL de licitações.
    Retorna o HTML da página ou None em caso de erro.
    """

    url = f"{BASE_URL}?start={start_param}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar conteúdo de {url}: {e}")
        return None


# Rota principal: exibe o formulário para seleção do SRE
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota inicial: exibe o dropdown para seleção do SRE
    e redireciona para a rota escolhida.
    """
    if request.method == 'POST':
        site_selected = request.form.get('site_select', 'varginha')
        return redirect(url_for(site_selected))
    return render_template('index.html', search_query='', cards=[], site_select='varginha', max_pages=1)


# Rota para exibir cards da SRE Varginha
@app.route('/varginha', methods=['GET', 'POST'])
def varginha():
    """
    Exibe cards de licitações da SRE Varginha,
    com filtro por termo de busca.
    """
    search_query = request.form.get('search_query', '')
    max_pages = int(request.form.get('max_pages', 1))
    cards = scrape_website_cards_varginha(max_pages)
    filtered_cards = []
    # Filtra os cards pelo termo de busca
    if request.method == 'POST' and search_query:
        for card in cards:
            if search_query.lower() in card.get(
                'full_html_content', ''
            ).lower():
                filtered_cards.append(card)
    else:
        filtered_cards = cards
    return render_template(
        'index.html',
        search_query=search_query,
        cards=filtered_cards,
        site_select='varginha',
        max_pages=max_pages
    )


# Rota para exibir cards da SRE Poços de Caldas
@app.route('/pocoscaldas', methods=['GET', 'POST'])
def pocoscaldas():
    """
    Exibe cards de licitações da SRE Poços de Caldas,
    com filtro por termo de busca.
    """
    search_query = request.form.get('search_query', '')
    max_pages = int(request.form.get('max_pages', 1))
    cards = scrape_website_cards_pocoscaldas(max_pages)
    filtered_cards = []
    # Filtra os cards pelo termo de busca usando apenas a seção 'ESPECIFICAÇÃO DO OBJETO:'
    if request.method == 'POST' and search_query:
        for card in cards:
            if search_query.lower() in card.get('especificacao_text', '').lower():
                filtered_cards.append(card)
    else:
        filtered_cards = cards
    return render_template(
        'index.html',
        search_query=search_query,
        cards=filtered_cards,
        site_select='pocoscaldas',
        max_pages=max_pages
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
