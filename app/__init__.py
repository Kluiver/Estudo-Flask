# Importando a classe Flask
from flask import Flask, request

# Importando a ferramenta responsável pelo banco de dados
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Importando o dotenv
from dotenv import load_dotenv
# Importando o login manager
from flask_login import LoginManager
# Importando o criptografador de senha
from flask_bcrypt import Bcrypt
# Importando a bibliotesa OS
import os

# Carregando as variáveis de ambiente do.env
load_dotenv('.env')

#startando o app
app = Flask(__name__) # Pegando o nome para o aplicativo do arquivo que estou trabalhando
# Configurando o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') #define qual o caminho para o banco de dados do nosso sistema a partir do arquivo .env
# Desativando o check automático de modificações
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#passando o token de segurança
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Configurando pasta pala upload de arquivos do usuário
app.config['UPLOAD_FILES'] = r'static/data'

# Criando o banco de dados
db = SQLAlchemy(app)
# Definindo o aplicativo de migração passando o app e o banco de dados criado
migrate = Migrate(app, db)

# Configurando o login e o bcrypt
login_manager = LoginManager(app)
# Essa opção serve para criar páginas que precisam estar logado para acessar
login_manager.login_view = 'homepage'
bcrypt = Bcrypt(app)

# PARA CRIAR O BANCO DE DADOS, RODA NO TERMINAL "flask db init"
# APÓS ISSO, RODAR O COMANDO "flask db --message migrate '<mensagem de commit>' "
# EM SEGUIDA, RODAR O COMANDO "flask db upgrade" PARA QUE AS ALTERAÇOES SUBAM PARA O BANCO

from app.views import homepage
from app.models import Contato