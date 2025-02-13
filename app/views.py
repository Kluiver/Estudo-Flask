#importando o app do meu módulo
from app import app

#importando render template, arquivo responsável por renderizar o arquivo HTML
from flask import render_template

#criando a rota para o aplicativo
#colocando a barra sem nada para ser a página inicial
@app.route('/')
#função que vai renderizar a pagina
def homepage():
    return render_template('index.html')
