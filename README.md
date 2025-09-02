# ⚠️ **Protótipo em desenvolvimento!**

Este projeto está em fase inicial e irá integrar os dados das SREs de Varginha, Poços de Caldas, Campo Belo, Pouso Alegre, Itajubá e Caxambu para monitoramento e participação nos processos de caixa escolar.

O maior desafio é unificar informações de diferentes SREs, pois cada uma possui estrutura e padrão próprios, dificultando a padronização dos dados.

Futuramente, o projeto será migrado para Python/React, visando maior flexibilidade e escalabilidade.

O protótipo está disponível via deploy Railway em:
👉 https://apppesquisalicitacoes-production.up.railway.app/


# Pesquisador de Licitações Escolares

Este projeto é um aplicativo web desenvolvido em Python utilizando Flask, BeautifulSoup4 e Requests. Ele permite pesquisar licitações diretamente dos sites das SREs (exemplo: Varginha-MG e Poços de Caldas-MG), exibindo os resultados em uma interface moderna com Tailwind CSS.
O objetivo é criar uma ferramenta prática para uso no dia a dia, centralizando dados de várias secretarias de educação. Futuramente, o projeto pode evoluir para Python + React e abranger mais SREs.

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
├── sre_varginha.py
├── sre_pocoscaldas.py
├── templates/
│   └── index.html
├── .env (opcional, para variáveis locais)
```

## Passo a Passo para Executar o Projeto

1. **Configurar o ambiente Python**
   - Abra a pasta raiz do projeto no VS Code.
   - Certifique-se de que um interpretador Python está selecionado (veja na barra inferior do VS Code).

2. **Abrir o Terminal Integrado**
   - Menu: `Terminal > New Terminal` ou atalho `Ctrl+J`.
   - Garanta que o terminal está na pasta raiz do projeto.


3. **Instalar as dependências**
      - Ative o ambiente virtual (recomendado):
         ```bash
         python -m venv .venv
         source .venv/bin/activate
         ```
      - Instale as dependências:
         ```bash
         pip install -r requirements.txt
         ```


4. **Executar o aplicativo Flask**
      - No terminal, execute:
         ```bash
         python app.py
         ```
      - Se a porta 5000 estiver ocupada, rode em outra porta:
         ```bash
         PORT=5050 python app.py
         ```
      - O servidor Flask será iniciado. Você verá uma mensagem como:
         ```
         * Running on http://127.0.0.1:5000
         Press CTRL+C to quit
         ```

5. **Acessar o aplicativo no navegador**
   - Abra o navegador e acesse: [http://127.0.0.1:5000]

6. **Testar a funcionalidade**
   - Digite uma palavra-chave na caixa de pesquisa e clique em "Pesquisar".
   - Os cards de licitações que contêm a palavra-chave na seção "ESPECIFICAÇÃO DO OBJETO:" serão exibidos.


## Observações

- Os arquivos de scraping (`sre_varginha.py` e `sre_pocoscaldas.py`) estão na raiz do projeto.
- Os imports no `app.py` usam `from sre_varginha import ...` e `from sre_pocoscaldas import ...`.
- O Tailwind CSS é utilizado via CDN, não sendo necessário instalar nada adicional para o frontend.
- O aplicativo é para uso em ambiente de desenvolvimento. Para produção, utilize um servidor WSGI adequado.
- Se encontrar erros, compartilhe a mensagem exata do terminal ou navegador para suporte.

---
