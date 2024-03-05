from flask import Flask
import requests

app = Flask('testes')

bairros_atendidos = []

def pegar_bairro(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    resp = requests.get(url).json()
    return resp['bairro']

# Alteração

@app.route("/adicionar/<cep>")
def adicionar_bairro(cep):
    with open('bairros.txt', 'a') as b:
        try:
            bairro = pegar_bairro(cep)
            if bairro not in bairros_atendidos:
                bairros_atendidos.append(bairro)
                b.write(f'{bairro}\n')
                return f'Bairro \'{bairro}\' cadastrado com sucesso!'
            else:
                return f'Bairro \'{bairro}\' já cadastrado! {bairros_atendidos}'
        except Exception as e:
            return f'CEP inválido! {e}'

@app.route("/remover/<cep>")



def remover_bairro(cep):
    try:
        bairro = pegar_bairro(cep)
        if bairro in bairros_atendidos:
            bairros_atendidos.remove(bairro)
            return f'Bairro \'{bairro}\' removido com sucesso!'
        else:
            return f'Bairro \'{bairro}\' não foi cadastrado'
    except Exception as e:
            return f'CEP inválido! {e}'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/meu-bairro/<cep>")
def new_route(cep):
    print(f'O CEP digitado foi: {cep}')
    bairro = pegar_bairro(cep)
    if bairro is None:
        return "Bairro não encontrado", 404
    
    if bairro.lower() not in bairros_atendidos:
        return f"Bairro {bairro} não atendido"
    
    return f'Atendemos no bairro {bairro}'


@app.route("/not-found")
def not_found():
    return "Página não encontrada", 404 

app.run(debug=True)