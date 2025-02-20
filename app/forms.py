#importando o formulário do flask
from flask_wtf import FlaskForm
#importando os campos string e de envio do flask wtf
from wtforms import StringField, SubmitField, PasswordField, FileField
#importando os validadores do wtforms
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
#importando o modelo
from app.models import Contato, User, Post, Comentario
#importando o banco de dados
from app import db, bcrypt, app
# Importando OS
import os
# Módulo responsável por cuidar dos nomes dos arquivos para o banco de dados
from werkzeug.utils import secure_filename

# Classe de forumulário para usuário
class UserForm(FlaskForm):
    
    #definindo a categoria de cada campo do formulário
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])#possui validador para conferir com a senha digitada anteriormente
    btn_submit = SubmitField('Cadastrar')

    # Função validadora para verificar se o e-mail já foi cadastrado
    # Função PRECISA ter o nome validade no inicio e o nome do campo em que quer validar
    def validate_email(self, email):
        # Verificando se o email existe no banco de dados
        if User.query.filter_by(email=email.data).first():
            # Se o usuário já existe no banco, retorno erro de validação
            raise ValidationError('Usuário já cadastrado com esse E-mail!')
        
    # Função para salvar no banco de dados
    def save(self):
        # Criptografando a senha antes de salvar no banco de dados
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        #criando um novo usuário
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )
        
        # Salvando no banco de dados
        db.session.add(user)
        db.session.commit()
        #retorno o usuário
        return user


# Classe de formulário para login de usuário
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btn_submit = SubmitField('Login')

    # Função para login
    def login(self):
        # recuperar o usuário do e-mail
        user = User.query.filter_by(email=self.email.data).first()
        # Verificar se a senha é válida
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                # se a senha é válida, retorna o usuário
                return user
            # Se a senha é inválida
            else:
                raise Exception('Senha inválida!')
        else:
            raise Exception('Usuário não encontrado')


#criando a classe responsável por criar o formulário
class ContatoForm(FlaskForm):
    #definindo a categoria de cada campo do formulário
    #campos de texto
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    #campo de botão
    btn_submit = SubmitField('Enviar', validators=[DataRequired()])


    #função para salvar o formulario
    def save(self):
        # Pegando um contato para salvar na classe contato
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )

        #adicionando ao banco de dados
        db.session.add(contato)
        db.session.commit()


# Formulário para criação de post
class PostForm(FlaskForm):
    # campo de mensagem para o post
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[DataRequired()])
    # Botão para enviar o post
    btn_submit = SubmitField('Postar', validators=[DataRequired()])

    # Função para salvar o post
    def save(self, user_id):
        # Salvando a imagem no banco de dados
        imagem = self.imagem.data
        # Alterando o nome da imagem para um nome seguro
        nome_seguro = secure_filename(imagem.filename)
        post = Post(
            mensagem = self.mensagem.data,
            user_id = user_id,
            imagem = nome_seguro
        )

        # Salvando a imagem no diretório
        caminho = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), # Pegar a pasta que está o projeto
            app.config['UPLOAD_FILES'], # Definir a pasta que configuramos para upload
            'post', # Pasta que está os posts
            nome_seguro
        )

        imagem.save(caminho)
        # Salvando no banco de dados
        db.session.add(post)
        db.session.commit()


# Formulário para criação de comentário
class ComentarioForm(FlaskForm):
    # campo de comentário
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    # Botão para enviar o comentário
    btn_submit = SubmitField('Enviar', validators=[DataRequired()])

    # TODO: Verificar problema no nome do usuario
    # Função para salvar o comentário
    def save(self, user_id, post_id):
        comentario = Comentario(
            mensagem = self.mensagem.data,
            user_id = user_id,
            post_id = post_id
        )

        # Salvando no banco de dados
        db.session.add(comentario)
        db.session.commit()

        