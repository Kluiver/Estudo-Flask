from app import db
#importando date de datetime
from datetime import datetime, timezone

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