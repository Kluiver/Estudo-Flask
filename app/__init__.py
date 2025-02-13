# Importando a classe Flask
from flask import Flask, request

#startando o app
app = Flask(__name__) # Pegando o nome para o aplicativo do arquivo que estou trabalhando

from app.views import homepage