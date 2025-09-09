# sre_caxambu.py
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://srecaxambu.educacao.mg.gov.br/escolas-aquisicao-simplificada/"


def get_website_content_caxambu():
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar conteúdo de {BASE_URL}: {e}")
        return None


def scrape_website_cards_caxambu():
    html_content = get_website_content_caxambu()
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, 'html.parser')
    # Supondo que a tabela de licitações seja a primeira <table> da página
    table = soup.find('table')
    if not table:
        print("Tabela de licitações não encontrada.")
        return []
    cards = []
    rows = table.find_all('tr')
    header = True
    from datetime import datetime
    import re
    for row in rows:
        if header:
            header = False
            continue  # pula o cabeçalho
        cols = row.find_all(['td', 'th'])
        if len(cols) < 6:
            continue
        municipio = cols[0].get_text(strip=True)
        escola = cols[1].get_text(strip=True)
        caixa_escolar = cols[2].get_text(strip=True)
        objeto = cols[3].get_text(strip=True)
        data_divulgacao = cols[4].get_text(strip=True)
        processo = cols[5].get_text(strip=True)
        # Link: href é o número do processo, se for link
        processo_tag = cols[5].find('a', href=True)
        processo_href = processo_tag['href'] if processo_tag else None
        processo_link = f'<a href="{processo_href}" target="_blank" class="text-blue-400 underline font-bold">{processo}</a>' if processo_href else processo

        # Filtro: só exibe se data_divulgacao >= hoje
        match = re.search(r'(\d{2}/\d{2}/\d{2,4})', data_divulgacao)
        if not match:
            continue
        try:
            data_str = match.group(1)
            if len(data_str.split('/')[-1]) == 2:
                data_str = data_str[:-2] + '20' + data_str[-2:]
            data_dt = datetime.strptime(data_str, '%d/%m/%Y')
            hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if data_dt < hoje:
                continue
        except Exception:
            continue

        card_html = f'''
            <div>
                <p class="font-bold text-lg mb-1">{escola}</p>
                <p class="text-gray-300 mb-1">Município: <span class="font-semibold">{municipio}</span></p>
                <p class="mb-1">Caixa Escolar: <span class="font-semibold">{caixa_escolar}</span></p>
                <p class="mb-1">Objeto: <span class="font-semibold">{objeto}</span></p>
                <p class="mb-1">Data Divulgação: <span class="font-semibold">{data_divulgacao}</span></p>
                <p class="mb-1">Processo nº: {processo_link}</p>
            </div>
        '''
        cards.append({
            'full_html_content': card_html,
            'municipio': municipio,
            'escola': escola,
            'caixa_escolar': caixa_escolar,
            'objeto': objeto,
            'data_divulgacao': data_divulgacao,
            'processo': processo,
            'processo_href': processo_href
        })
    return cards
    return cards
