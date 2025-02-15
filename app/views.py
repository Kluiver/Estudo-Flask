#importando o app do meu módulo
from app import app, db

#importando render template, arquivo responsável por renderizar o arquivo HTML
# URL_FOR é para direcionar links
from flask import render_template, url_for, request, redirect

#importando a classe Contato de model
from app.models import Contato

#importando o formulario
from app.forms import ContatoForm 

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


#FORMATO DE FORMULÁRIO NÃO RECOMENDADO
#criando outra rota
@app.route('/contato_old', methods=['GET', 'POST'])
def contato_old():
    #criando o contexto para retornar ao HTML
    context = {}
    #verificando se o request é do tipo GET
    if request.method == 'GET':
        #pego os argumentos pesquisados
        pesquisa = request.args.get('pesquisa')
        print('GET: ', pesquisa)
        # Adicionando a pesquisa no context
        context['pesquisa'] = pesquisa

    #verificando se o resquest é do tipo POST
    if request.method == 'POST':
        #pegando os dados do formulário para enviar para o banco de dados
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        #colocando os dados na minha classe Contato
        contato = Contato(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )

        #enviando os dados para o banco de dados
        db.session.add(contato)
        db.session.commit()

    return render_template('contato_old.html', context=context)


#FORMATO DE FORMULÁRIO RECOMENDADO
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    #definindo o formulário
    form = ContatoForm()
    #criando o contexto para retornar ao HTML
    context = {}
    
    #verificando se o formulário foi validado
    if form.validate_on_submit():
        #se foi validado, salvo ele
        form.save()
        #redireciono para a home page
        return redirect(url_for('homepage'))

    return render_template('contato.html', context=context, form = form)