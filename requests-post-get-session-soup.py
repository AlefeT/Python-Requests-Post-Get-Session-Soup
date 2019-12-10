#!/usr/bin/python3
# -*- coding: utf-8 -*-

# - - - - - - - - - - - - - - [ Bloco de Importar Bibliotecas (libs) ] - - - - - - - - - - - - - - #

try:
    import os
    import os.path
    import requests
    from requests import session
    from bs4 import BeautifulSoup
    from lxml import html

except Exception as E:
    print('Erro ao Importar Bibliotecas: ' + E)


# - - - - - - - - - - - - - - [ Bloco de Definicao de Variaveis (1o) ] - - - - - - - - - - - - - - #

try:
    # Headers
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}  # Variavel que guarda o User Agent que sera utilizado para os Requests via Post

    # Acao Login
    urlLogin = "https://exemplo.com/Control?action=login"  # Variavel que guarda a url base para a Acao de Login
    dataLogin = {"login": 'usuario', "password": 'senha', "button": 'Login'}  # Salva os Elementos da Acao de Login e seus Valores

    # Acao Listar
    urlListar = "https://exemplo.com/Control?action=listar"  # Variavel que guarda a url base para a Acao de Listar
    dataListar = {"version": '', "bean": '', "code": '', "onClose": '', "cpfClient": '', "dateStartFilter": '', "dateEndFilter": ''}  # Salva os Elementos da Acao Listar e seus Valores
    dataListar["dateStartFilter"] = '01/01/2019'  # Variavel que guarda a data inicial para o Filtro
    dataListar["dateEndFilter"] = '31/12/2019'  # Variavel que guarda a data final para o Filtro

    # Acao Imprimir
    codigo = '0'  # Variavel que guardara o Codigo
    urlImprimir = 'https://exemplo.com/Control?action=imprimir&codigo='  # Variavel que guarda a url base para a Acao de Imprimir
    urlImprimirAtual = ''  # Variavel que guardara a url Montada para a Acao de Imprimir

except Exception as E:
    print('Erro ao Definir as Variaveis: ' + E)

# - - - - - - - - - - - - - - [ Bloco de Execucao (2o) ] - - - - - - - - - - - - - - #

# [ Cria a Sessao utilizando os Headers e Efetua o Login ]
try:
    session = requests.Session()  # Cria a Sessao
    session.headers.update(headers)  # Seta os Headers
    requestLogin = session.post(urlLogin, data=dataLogin)  # Efetua o Post para a urlLogin com os dados de acesso para realizar Login

except Exception as E:
    print('Erro ao Criar a Sessao e Efetuar o Login: ' + E)



# [ Para cada loop: Monta o Request da Acao Listar, Executa e obtem o Codigo, depois Monta o Request da Acao Imprimir, Executa e Salva o PDF gerado ]
for i in range(0, 9):

    # [ Acao Listar ]
    try:
        dataListar["cpfClient"] = '1234567891'+str(i)  # Define os dados do Cliente para o Request via Post da Acao Listar Atual
        requestListar = session.post(urlListar, data=dataListar, cookies=requestLogin.cookies)  # Efetua o Request via Post da Acao Listar com os dados do Cliente e o Cookie da Sessao logada

        soup = BeautifulSoup(requestListar.content, 'lxml')  # Guarda o Soup do conteudo do Request da Acao Listar
        span_tag = soup.select('span')  # Obtem os Spans destes Soup

        # Encontra o Span que possui o Codigo
        for tag in span_tag:
            if str(tag.text.strip())[:3] == '000':
                codigo = str(int(tag.text.strip()))  # Guarda o Codigo, sem os zeros a esquerda

    except Exception as E:
        print('Erro ao efetuar a Acao de Listar: ' + E)


    # [ Acao Imprimir ]
    try:
        if codigo != '0' and len(codigo) >= 1:  # Verifica se o Codigo nao esta zerado ou vazio
            urlImprimirAtual = str(urlImprimir)+str(codigo)  # Monta a urlImprimirAtual com o codigo atual
            requestImprimir = session.get(url=urlImprimirAtual, cookies=requestLogin.cookies, allow_redirects=True)  # Efetua o Request via Get para a urlImprimirAtual com o Cookie da Sessao logada
            open(os.path.join('_PDFs', 'file'+str(codigo)+'.pdf'), 'wb').write(requestImprimir.content)  # Salva o PDF gerado

    except Exception as E:
        print('Erro ao efetuar a Acao de Imprimir: ' + E)
