# Pesquisador de Licitações Escolares

Este projeto é um aplicativo web desenvolvido em Python utilizando Flask, BeautifulSoup4 e Requests. Ele permite pesquisar licitações diretamente do site da SRE (no caso para teste, está sendo usada a secretaria de Varginha-MG), exibindo os resultados em uma interface moderna com Tailwind CSS.
Este projeto é apenas um "rabisco"para criação de uma ferramenta para uso no meu dia-a-dia, para auxiliar com dados. O futuro será, com certeza, Python + React e com tratamento de várias secretarias de educação. Centrando todas nesta ferramenta online. Útil para licitantes.

## Tecnologias Utilizadas

- **Python 3**
- **Flask**: Framework web para Python
- **BeautifulSoup4**: Biblioteca para raspagem de dados HTML
- **Requests**: Biblioteca para requisições HTTP
- **Tailwind CSS**: Utilizado via CDN para estilização da interface

## Estrutura do Projeto

```
app_pesquisa_licitacoes/
├── app.py
├── requirements.txt
├── backend/
│   ├── __init__.py
│   ├── sre_varginha.py
│   ├── sre_pocoscaldas.py
├── templates/
│   └── index.html
```

## Passo a Passo para Executar o Projeto

1. **Configurar o ambiente Python**
   - Abra a pasta raiz do projeto no VS Code.
   - Certifique-se de que um interpretador Python está selecionado (veja na barra inferior do VS Code).

2. **Abrir o Terminal Integrado**
   - Menu: `Terminal > New Terminal` ou atalho `Ctrl+J`.
   - Garanta que o terminal está na pasta raiz do projeto.

3. **Instalar as dependências**
    - Ative o ambiente virtual antes de instalar as dependências:
       ```bash
       source .venv/bin/activate
       ```
    - Depois, execute:
       ```bash
       pip install -r requirements.txt
       ```
    - Alternativamente, se não tiver o arquivo `requirements.txt`, use:
       ```bash
       pip install Flask beautifulsoup4 requests
     ```

4. **Executar o aplicativo Flask**
    - No terminal, execute:
       ```bash
       python app.py
       ```
    - Se não funcionar, tente:
       ```bash
       flask run
       ```
    - O servidor Flask será iniciado. Você verá uma mensagem como:
       ```
       * Debug mode: on
       * Running on http://127.0.0.1:5000
       Press CTRL+C to quit
       ```

5. **Acessar o aplicativo no navegador**
   - Abra o navegador e acesse: [http://127.0.0.1:5000]

6. **Testar a funcionalidade**
   - Digite uma palavra-chave na caixa de pesquisa e clique em "Pesquisar".
   - Os cards de licitações que contêm a palavra-chave na seção "ESPECIFICAÇÃO DO OBJETO:" serão exibidos.

## Observações

- Os arquivos de scraping agora estão organizados na pasta `backend/`.
- Os imports no `app.py` usam `from backend.sre_varginha import ...`.
- O Tailwind CSS é utilizado via CDN, não sendo necessário instalar nada adicional para o frontend.
- O aplicativo é para uso em ambiente de desenvolvimento. Para produção, utilize um servidor WSGI adequado.
- Se encontrar erros, compartilhe a mensagem exata do terminal ou navegador para suporte.

---
