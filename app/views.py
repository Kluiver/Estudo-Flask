#importando o app do meu módulo
from app import app

#importando render template, arquivo responsável por renderizar o arquivo HTML
# URL_FOR é para direcionar links
from flask import render_template, url_for

#criando a rota para o aplicativo
#colocando a barra sem nada para ser a página inicial
@app.route('/')
#função que vai renderizar a pagina
def homepage():
    #Informaçoes do backend para o front end
    usuario = 'Kluiver'
    idade = 24

    #salvando as informações do backend em um dicionário para passar mais facilmente para o front-end
    context = {
        'usuario': usuario,
        'idade': idade
    }
    return render_template('index.html', context=context) #Passando o dicionário com as informaçoes para o front


#criando outra rota
@app.route('/nova')
def nova_pagina():
    return 'Nova página.'
