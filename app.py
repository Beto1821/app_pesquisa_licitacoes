import requests
from flask import Flask, render_template, request, redirect, url_for
from sre_varginha import scrape_website_cards_varginha
from sre_pocoscaldas import scrape_website_cards_pocoscaldas
from sre_itajuba import scrape_website_cards_itajuba

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
    from datetime import datetime
    cards = scrape_website_cards_varginha(max_pages)
    filtered_cards = []
    # Filtra os cards pelo termo de busca e prazo
    import re
    def prazo_maior_que_hoje(card):
        # Tenta extrair a data de todos os campos possíveis
        import re
        data_sources = [card.get('data_ate'), card.get('prazo'), card.get('full_html_content', '')]
        for source in data_sources:
            if not source:
                continue
            match = re.search(r'(\d{2}/\d{2}/\d{4})', source)
            if match:
                try:
                    data_card = datetime.strptime(match.group(1), '%d/%m/%Y')
                    if data_card >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                        return True
                except Exception:
                    continue
        return False

    if request.method == 'POST':
        for card in cards:
            if (not search_query or search_query.lower() in card.get('full_html_content', '').lower()) and prazo_maior_que_hoje(card):
                filtered_cards.append(card)
    else:
        filtered_cards = [card for card in cards if prazo_maior_que_hoje(card)]
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
    from datetime import datetime
    cards = scrape_website_cards_pocoscaldas(max_pages)
    filtered_cards = []
    import re
    def prazo_maior_que_hoje(card):
        import re
        data_sources = [card.get('data_ate'), card.get('prazo'), card.get('full_html_content', '')]
        for source in data_sources:
            if not source:
                continue
            match = re.search(r'(\d{2}/\d{2}/\d{4})', source)
            if match:
                try:
                    data_card = datetime.strptime(match.group(1), '%d/%m/%Y')
                    if data_card >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                        return True
                except Exception:
                    continue
        return False

    if request.method == 'POST':
        for card in cards:
            if (not search_query or search_query.lower() in card.get('especificacao_text', '').lower()) and prazo_maior_que_hoje(card):
                filtered_cards.append(card)
    else:
        filtered_cards = [card for card in cards if prazo_maior_que_hoje(card)]
    return render_template(
        'index.html',
        search_query=search_query,
        cards=filtered_cards,
        site_select='pocoscaldas',
        max_pages=max_pages
    )

# Rota para exibir cards da SRE Itajubá
@app.route('/itajuba', methods=['GET', 'POST'])
def itajuba():
    """
    Exibe cards de licitações da SRE Itajubá,
    com filtro por termo de busca.
    """
    search_query = request.form.get('search_query', '')
    # Ignora o filtro 'Publicações' (max_pages) para Itajubá, sempre busca todas as publicações
    from datetime import datetime
    import re
    cards = scrape_website_cards_itajuba()
    filtered_cards = []
    def prazo_maior_que_hoje(card):
        import re
        data_sources = [card.get('data_ate'), card.get('prazo'), card.get('full_html_content', '')]
        for source in data_sources:
            if not source:
                continue
            match = re.search(r'(\d{2}/\d{2}/\d{4})', source)
            if match:
                try:
                    data_card = datetime.strptime(match.group(1), '%d/%m/%Y')
                    if data_card >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                        return True
                except Exception:
                    continue
        return False

    if request.method == 'POST':
        for card in cards:
            if (not search_query or search_query.lower() in card.get('specification_text', '').lower()) and prazo_maior_que_hoje(card):
                filtered_cards.append(card)
    else:
        filtered_cards = [card for card in cards if prazo_maior_que_hoje(card)]
    return render_template(
        'index.html',
        search_query=search_query,
        cards=filtered_cards,
        site_select='itajuba'
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
