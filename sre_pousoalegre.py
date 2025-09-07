# sre_pousoalegre.py
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://srepousoalegre.educacao.mg.gov.br/index.php/aquisicao-simplificada/editais-licitacao-por-municipio-2025"


def scrape_website_cards_pousoalegre():
    """
    Raspagem dos editais da SRE Pouso Alegre.
    Retorna uma lista de dicionários com os campos:
    - numero_processo
    - periodo_divulgacao
    - link_acesso
    - descricao_objeto
    - full_html_content (HTML do card)
    """
    try:
        response = requests.get(BASE_URL, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {BASE_URL}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    cards = []
    # Procura todas as tabelas na página
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            numero_processo = cols[0].get_text(strip=True)
            periodo_divulgacao = cols[1].get_text(strip=True)
            link_tag = cols[2].find("a", href=True)
            link_acesso = link_tag["href"] if link_tag else ""
            # Corrige link relativo para absoluto
            if link_acesso and link_acesso.startswith("/"):
                link_acesso = f"https://srepousoalegre.educacao.mg.gov.br{link_acesso}"
            descricao_objeto = cols[3].get_text(strip=True)
            # Ignora linhas de cabeçalho ou sem valor real
            if (
                not numero_processo
                or numero_processo.lower() == "nº do processo"
                or periodo_divulgacao.lower() == "período de divulgação"
                or descricao_objeto.lower() == "descrição do objeto"
            ):
                continue
            # Monta HTML do card
            card_html = f"""
            <div><strong>Nº do Processo:</strong> {numero_processo}</div>
            <div><strong>Período de Divulgação:</strong> {periodo_divulgacao}</div>
            <div><strong>Link de Acesso:</strong> <a href='{link_acesso}' target='_blank' rel='noopener noreferrer' class='text-blue-600 underline'>Edital</a></div>
            <div><strong>Descrição do Objeto:</strong> {descricao_objeto}</div>
            """
            cards.append({
                "numero_processo": numero_processo,
                "periodo_divulgacao": periodo_divulgacao,
                "link_acesso": link_acesso,
                "descricao_objeto": descricao_objeto,
                "full_html_content": card_html
            })
    return cards
