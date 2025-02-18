from app import db, login_manager
#importando date de datetime
from datetime import datetime, timezone
# Importando o modelo que usaremos para a classe de usuário
from flask_login import UserMixin


# Função para recuperar o usuário para fazer a sessão
@login_manager.user_loader
def load_user(user_id, ):
    # Retornar o usuário logado
    return User.query.get(user_id)

# Criando a classe responsável por criar o campo usuário no banco de dados
class User(db.Model, UserMixin):
    # Primary key para a classe
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    sobrenome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True) 

# Criando a classe contato reponsável por criar a tabela no banco de dados
class Contato(db.Model): #TODA classe vai herdar o modelo do banco de dados
    
    # TODA tabela precisa de um ID
    id = db.Column(db.Integer, primary_key= True) # Define essa tabela como principal
    # Definindo os dados que preciso para essa classe
    nome = db.Column(db.String, nullable= True) #String, não pode ser nulo
    data_envio = db.Column(db.DateTime, default= datetime.now(timezone.utc)) #definindo a data atual sendo a data atual
    email = db.Column(db.String, nullable= True)
    assunto = db.Column(db.String, nullable= True)
    mensagem = db.Column(db.String, nullable= True)
    respondida = db.Column(db.Integer, default= 0)

