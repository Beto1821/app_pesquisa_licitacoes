# sre_itajuba.py
from bs4 import BeautifulSoup
import requests


# URL da página de Aquisições Simplificadas
BASE_URL = "https://sreitajuba.educacao.mg.gov.br/index.php/licitacoes/aquisicao-simplificada"


def get_website_content(url):
    """
    Faz uma requisição HTTP para uma URL e retorna o conteúdo HTML.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar conteúdo de {url}: {e}")
        return None


def scrape_website_cards_itajuba(max_pages_to_scrape=1):
    """
    Raspa os cards de licitações da SRE Itajubá.
    
    Esta função é diferente das demais. Ela:
    1. Raspa a tabela principal de escolas.
    2. Para cada escola, faz uma nova requisição para obter os detalhes.
    3. Extrai apenas as informações de PROCESSO, PRAZO e ESPECIFICAÇÃO.
    """
    all_cards_data = []
    
    # Etapa 1: Raspar a página principal e encontrar os links de escolas
    print("Raspando a página principal de Aquisição Simplificada da SRE Itajubá.")
    html_content = get_website_content(BASE_URL)
    if not html_content:
        return all_cards_data
    
    soup = BeautifulSoup(html_content, 'html.parser')
    table_links = soup.select('table a')
    
    # Etapa 2: Iterar sobre os links e raspar os detalhes de cada escola
    for link in table_links:
        school_url = link.get('href')
        if not school_url:
            continue

        if not school_url.startswith('http'):
            school_url = 'https://sreitajuba.educacao.mg.gov.br' + school_url

        print(f"Visitando página da escola: {school_url}")
        school_html_content = get_website_content(school_url)
        if not school_html_content:
            continue

        resultados = parse_tabela_aquisicao(school_html_content)
        for resultado in resultados:
            if resultado.get('processo_link'):
                processo_html = f"<a href='{resultado['processo_link']}' target='_blank' class='text-blue-600 underline'>{resultado['processo']}</a>"
            else:
                processo_html = resultado['processo']
            simple_html_content = f"""
                <h3 class='font-bold text-lg mb-2'>Processo: {processo_html}</h3>
                <p class='data-ate'>Prazo: {resultado['prazo']}</p>
                <p><strong>Especificação:</strong> {resultado['especificacao']}</p>
            """
            all_cards_data.append({
                'full_html_content': simple_html_content,
                'specification_text': resultado['especificacao'],
            })

    return all_cards_data


def parse_tabela_aquisicao(html):
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.find('table')
    resultados = []
    if not tabela:
        return resultados

    linhas = tabela.find_all('tr')
    for tr in linhas[1:]:  # pula o cabeçalho
        tds = tr.find_all('td')
        if len(tds) >= 3:
            processo_tag = tds[0].find('a')
            if processo_tag:
                processo = processo_tag.get_text(strip=True)
                processo_link = processo_tag.get('href')
            else:
                processo = tds[0].get_text(strip=True)
                processo_link = None
            prazo = tds[1].get_text(strip=True)
            especificacao = tds[2].get_text(strip=True)
            if processo or prazo or especificacao:
                resultados.append({
                    'processo': processo,
                    'processo_link': processo_link,
                    'prazo': prazo,
                    'especificacao': especificacao
                })
    return resultados


def scrape_and_filter_cards(max_pages, search_query):
    all_cards = scrape_website_cards_itajuba(max_pages)
    if search_query:
        search_term = search_query.lower()
        return [card for card in all_cards if search_term in card['specification_text'].lower()]
    return all_cards
