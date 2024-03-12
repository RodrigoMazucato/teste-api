import requests
from flask import Flask

app = Flask('teste')
apikey = 'e51a115c'

def requisicao_busca(texto_buscar, tipo='null'):
    try:
        url = f"http://www.omdbapi.com/?apikey={apikey}&s={texto_buscar}&type={tipo}"
        resposta = requests.get(url).json()
        return resposta['totalResults']
    except:
        return f'Termo não encontrado!', 400

@app.route('/qtd/geral/<texto>') 
def busca_qtd_geral(texto):
    return requisicao_busca(texto)
    
@app.route('/qtd/filme/<texto>')  
def busca_qtd_filmes(texto):
    return requisicao_busca(texto, 'movie')
   
@app.route('/qtd/serie/<texto>')  
def busca_qtd_series(texto):
    return requisicao_busca(texto, 'series')

@app.route('/qtd/jogo/<texto>')  
def busca_qtd_jogos(texto):
    return requisicao_busca(texto, 'game')
    
def requisicao_id(texto):
    url = f"http://www.omdbapi.com/?apikey={apikey}&i={texto}"
    return requests.get(url).json()
    
@app.route('/filme/nome/<texto>')
def busca_nome_filme_por_id(texto):
    try:
        resposta = requisicao_id(texto)
        return resposta['Title']
    except:
        return f'Filme não encontrado!', 400
    
@app.route('/filme/ano/<texto>')
def busca_ano_filme_por_id(texto):
    try:
        resposta = requisicao_id(texto)
        return resposta['Released']
    except:
        return f'Filme não encontrado!', 400
    
@app.route('/filme/info/<texto>')
def dicionario_do_filme_por_id(texto):
    try:
        resposta = ''
        dic = requisicao_id(texto)
        for chave in ['Title', 'Released', 'Director', 'Genre']:
            resposta += f'{dic[chave]} | '
        return resposta
    except:
        return f'Filme não encontrado!', 400

# Faça uma função busca_filmes que, dada uma busca, retorna
# os dez primeiros items (filmes, series, jogos ou o que for)
# que batem com a busca.

# A sua resposta deve ser uma lista, cada filme representado por 
# um dicionário. cada dicionario deve conter os campos
# 'nome' (valor Title da resposta) e 'ano' (valor Year da resposta).
# '''
@app.route('/buscar/<texto>') 
def busca_filmes(texto):
    lista = []
    url = f"http://www.omdbapi.com/?apikey={apikey}&s={texto}"
    resposta = requests.get(url).json()
    for item in resposta['Search']:
        dic = {'nome': item['Title'], 'ano': item['Year']}
        lista.append(dic)
    return lista

# '''
# Faça uma função busca_filmes_grande que, dada uma busca, retorna
# os VINTE primeiros filmes que batem com a busca.
# '''
@app.route('/buscar-info-grande/<texto>/<pags>') 
def busca_filmes_grande_info(texto, pags):
    resultado = []
    for i in range(1, int(pags)+1):
        url = f"http://www.omdbapi.com/?apikey={apikey}&s={texto}&page={i}"
        resposta = requests.get(url).json()
        resultado.extend(resposta['Search'])
    return resultado

@app.route('/buscar-grande/<texto>/<pags>') 
def busca_filmes_grande(texto, pags):
    resultado = []
    for i in range(1, int(pags)+1):
        url = f"http://www.omdbapi.com/?apikey={apikey}&s={texto}&page={i}"
        resposta = requests.get(url).json()
        for item in resposta['Search']:
            dic = {'nome': item['Title'], 'ano': item['Year']}
            resultado.append(dic)
    return resultado

app.run(debug=True)