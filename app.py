# --- Rotas Flask ---
import re
from flask import Flask, render_template, request, redirect, url_for
from sre_varginha import scrape_website_cards_varginha
from sre_pocoscaldas import scrape_website_cards_pocoscaldas
from sre_itajuba import scrape_website_cards_itajuba
from sre_pousoalegre import scrape_website_cards_pousoalegre
from sre_caxambu import scrape_website_cards_caxambu
from sre_campobelo import scrape_website_cards_campobelo
from sre_saojoaodelrey import scrape_website_cards_saojoaodelrey

app = Flask(__name__)


# Rota principal: exibe o formulário para seleção do SRE
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota inicial: exibe o dropdown para seleção do SRE
    e redireciona para a rota escolhida.
    """
    if request.method == 'POST':
        site_selected = request.form.get('site_select', '')
        if not site_selected:
            # Não faz nada, apenas renderiza a tela inicial
            return render_template('index.html', search_query='', cards=[], site_select='')
        return redirect(url_for(site_selected))
    return render_template('index.html', search_query='', cards=[], site_select='')


# Rota para exibir cards da SRE Varginha
@app.route('/varginha', methods=['GET', 'POST'])
def varginha():
    """
    Exibe cards de licitações da SRE Varginha,
    com filtro por termo de busca.
    """
    search_query = request.form.get('search_query', '')
    cards = scrape_website_cards_varginha(10)  # Sempre 10 páginas/60 cards
    filtered_cards = []

    def prazo_maior_que_hoje(card):
        import re
        from datetime import datetime
        conteudo = card.get('full_html_content', '')
        match = re.search(r'(\d{2}/\d{2}/\d{2,4})', conteudo)
        if not match:
            return False
        try:
            data_str = match.group(1)
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
        site_select='varginha'
    )


# Rota para exibir cards da SRE Poços de Caldas
@app.route('/pocoscaldas', methods=['GET', 'POST'])
def pocoscaldas():
    """
    Exibe cards de licitações da SRE Poços de Caldas,
    com filtro por termo de busca.
    """
    search_query = request.form.get('search_query', '')
    from datetime import datetime
    cards = scrape_website_cards_pocoscaldas(10)  # Sempre 10 páginas/60 cards
    filtered_cards = []
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
        site_select='pocoscaldas'
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

@app.route('/campobelo', methods=['GET', 'POST'])
def campobelo():
    """
    Exibe cards de licitações da SRE Campo Belo,
    com filtro por termo de busca (múltiplas palavras).
    """
    search_query = request.form.get('search_query', '')
    cards = scrape_website_cards_campobelo()
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
        site_select='campobelo',
        max_pages=1
    )


# Rota para exibir cards da SRE São João Del Rey
@app.route('/saojoaodelrey', methods=['GET', 'POST'])
def saojoaodelrey():
    """
    Exibe cards de licitações da SRE São João Del Rey,
    com filtro por termo de busca (múltiplas palavras).
    """
    search_query = request.form.get('search_query', '')
    cards = scrape_website_cards_saojoaodelrey(10)  # Sempre 10 páginas/60 cards
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
        site_select='saojoaodelrey'
    )

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


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
