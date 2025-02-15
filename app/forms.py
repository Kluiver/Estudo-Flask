#importando o formulário do flask
from flask_wtf import FlaskForm
#importando os campos string e de envio do flask wtf
from wtforms import StringField, SubmitField
#importando os validadores do wtforms
from wtforms.validators import DataRequired, Email
#importando o modelo
from app.models import Contato
#importando o banco de dados
from app import db

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
