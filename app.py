import requests
import re
from flask import Flask, render_template, request, redirect, url_for
from sre_varginha import scrape_website_cards_varginha
from sre_pocoscaldas import scrape_website_cards_pocoscaldas
from sre_itajuba import scrape_website_cards_itajuba
from sre_pousoalegre import scrape_website_cards_pousoalegre
from sre_caxambu import scrape_website_cards_caxambu


app = Flask(__name__)

# Rota para exibir cards da SRE Pouso Alegre


@app.route('/pousoalegre', methods=['GET', 'POST'])
def pousoalegre():
    """
    Exibe cards de licitações da SRE Pouso Alegre,
    com filtro por termo de busca.
    """
    search_query = request.form.get('search_query', '')
    cards = scrape_website_cards_pousoalegre()
    filtered_cards = []
    if request.method == 'POST':
        palavras = [p.strip() for p in search_query.lower().replace(',', ' ').split() if p.strip()]
        for card in cards:
            conteudo = card.get('full_html_content', '').lower()
            if not palavras or any(p in conteudo for p in palavras):
                filtered_cards.append(card)
    else:
        filtered_cards = cards[:]
    return render_template(
        'index.html',
        search_query=search_query,
        cards=filtered_cards,
        site_select='pousoalegre',
        max_pages=1
    )


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
    # import re removido (já está no topo)
    def prazo_maior_que_hoje(card):
        import re
        from datetime import datetime
        conteudo = card.get('full_html_content', '')
        # Busca a primeira data no formato DD/MM/YY ou DD/MM/YYYY
        match = re.search(r'(\d{2}/\d{2}/\d{2,4})', conteudo)
        if not match:
            return False
        try:
            data_str = match.group(1)
            # Corrige ano com 2 dígitos para 4 dígitos
            partes = data_str.split('/')
            if len(partes[2]) == 2:
                ano = int(partes[2])
                if ano < 50:
                    partes[2] = f"20{partes[2]}"
                else:
                    partes[2] = f"19{partes[2]}"
                data_str = '/'.join(partes)
            data_card = datetime.strptime(data_str, '%d/%m/%Y')
            hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return data_card >= hoje
        except Exception:
            return False

    if request.method == 'POST':
        palavras = [p.strip() for p in search_query.lower().replace(',', ' ').split() if p.strip()]
        for card in cards:
            conteudo = card.get('full_html_content', '').lower()
            if (not palavras or any(p in conteudo for p in palavras)) and prazo_maior_que_hoje(card):
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
    # import re removido (já está no topo)

    # Função de filtro pode ser reimplementada se necessário, mas bloco anterior estava mal indentado e não era usado

    if request.method == 'POST':
        palavras = [p.strip() for p in search_query.lower().replace(',', ' ').split() if p.strip()]
        for card in cards:
            conteudo1 = card.get('especificacao_text', '').lower()
            conteudo2 = card.get('full_html_content', '').lower()
            if not palavras or any(p in conteudo1 or p in conteudo2 for p in palavras):
                filtered_cards.append(card)
    else:
        filtered_cards = cards[:]
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
    cards = scrape_website_cards_itajuba()
    filtered_cards = []

    def prazo_maior_que_hoje(card):
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
        palavras = [p.strip() for p in search_query.lower().replace(',', ' ').split() if p.strip()]
        for card in cards:
            conteudo = card.get('specification_text', '').lower()
            if (not palavras or any(p in conteudo for p in palavras)) and prazo_maior_que_hoje(card):
                filtered_cards.append(card)
    else:
        filtered_cards = [card for card in cards if prazo_maior_que_hoje(card)]
    return render_template(
        'index.html',
        search_query=search_query,
        cards=filtered_cards,
        site_select='itajuba'
    )


# Rota para exibir cards da SRE Caxambu
@app.route('/caxambu', methods=['GET', 'POST'])
def caxambu():
    """
    Exibe cards de licitações da SRE Caxambu,
    com filtro por termo de busca (múltiplas palavras).
    """
    search_query = request.form.get('search_query', '')
    cards = scrape_website_cards_caxambu()
    filtered_cards = []
    if request.method == 'POST':
        palavras = [p.strip() for p in search_query.lower().replace(',', ' ').split() if p.strip()]
        for card in cards:
            conteudo = card.get('full_html_content', '').lower()
            if not palavras or any(p in conteudo for p in palavras):
                filtered_cards.append(card)
    else:
        filtered_cards = cards[:]
    return render_template(
        'index.html',
        search_query=search_query,
        cards=filtered_cards,
        site_select='caxambu',
        max_pages=1
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
