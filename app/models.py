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
    # Vinculando o usuário com o post NAO cria tabela, e sim uma relação
    # Coloco o nome da classe que tem relação, backref é como o Post vai chamar o usuário, lazy=True permite a relação inversa
    posts = db.relationship('Post', backref='user', lazy=True)
    # Vinculando o comentário ao usuario
    comentarios = db.relationship('Comentario', backref='user', lazy=True) 

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

# classe que vai criar a tabela post
class Post(db.Model):
    # ID
    id = db.Column(db.Integer, primary_key=True)
    # Data de criação do post
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    # Mensagem do post
    mensagem = db.Column(db.String, nullable= True)
    # Campo para upload de imagem
    imagem = db.Column(db.String, nullable= True, default='default.png')
    # Vinculando usuário que fez o post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)# Passo o nome da tabela e a coluna que preciso dessa tabela
    # Vinculando o comentário ao post
    comentarios = db.relationship('Comentario', backref='post', lazy=True)

    # Resumo do post
    def msg_resumo(self):
        return f'{self.mensagem[:10]} ... '
    
# Classe que vai criar a tabela comentarios de post
class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Data do comentário
    data_comentario = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    # Mensagem do comentário
    mensagem = db.Column(db.String, nullable= True)
    # Vinculando o post ao comentário
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable= True)
    # Vinculando o usuário que comentou
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
