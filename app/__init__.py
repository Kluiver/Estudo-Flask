# Importando a classe Flask
from flask import Flask, request

# Importando a ferramenta responsável pelo banco de dados
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#startando o app
app = Flask(__name__) # Pegando o nome para o aplicativo do arquivo que estou trabalhando
# Configurando o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #define qual o caminho para o banco de dados do nosso sistema
# Desativando o check automático de modificações
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criando o banco de dados
db = SQLAlchemy(app)
# Definindo o aplicativo de migração passando o app e o banco de dados criado
migrate = Migrate(app, db)

# PARA CRIAR O BANCO DE DADOS, RODA NO TERMINAL "flask db init"
# APÓS ISSO, RODAR O COMANDO "flask db --message migrate '<mensagem de commit>' "
# EM SEGUIDA, RODAR O COMANDO "flask db upgrade" PARA QUE AS ALTERAÇOES SUBAM PARA O BANCO

from app.views import homepage
from app.models import Contato