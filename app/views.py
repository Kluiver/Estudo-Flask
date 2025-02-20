#importando o app do meu módulo
from app import app, db

#importando render template, arquivo responsável por renderizar o arquivo HTML
# URL_FOR é para direcionar links
from flask import render_template, url_for, request, redirect

#importando a classe Contato de model
from app.models import Contato, Post

#importando o formulario
from app.forms import ContatoForm, UserForm, LoginForm, PostForm, ComentarioForm

# Funçoes para login de usuário
from flask_login import login_user, logout_user, current_user, login_required

#criando a rota para o aplicativo
#colocando a barra sem nada para ser a página inicial
@app.route('/', methods=['GET', 'POST'])
#função que vai renderizar a pagina
def homepage():
    #Informaçoes do backend para o front end
    usuario = 'Kluiver'
    idade = 24

    form = LoginForm()

    # Verificando se o formulário tá valido e foi submetido
    if form.validate_on_submit():
        #logo com o usuário
        user = form.login()
        # Faço o navegador lembrar do login
        login_user(user, remember=True)

    # Verificando o usuário logado atual
    print(current_user.is_authenticated)
    #salvando as informações do backend em um dicionário para passar mais facilmente para o front-end
    context = {
        'usuario': usuario,
        'idade': idade
    }
    return render_template('index.html', context=context, form=form) #Passando o dicionário com as informaçoes para o front


#criando rota para cadastro de usuário
@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    # Passando o formulário do usuário
    form = UserForm()
    # Verificando se o formulário tá valido e foi submetido
    if form.validate_on_submit():
        # Salvo o usuário
        user = form.save()
        # Login do usuário
        login_user(user, remember=True) # remember true para caso abra uma nova aba, o site não vai esquecer que já está logado
        # redirecioso para a home page
        return redirect(url_for('homepage'))
    # Retornando a pagina de cadastro
    return render_template('cadastro.html', form=form)


# Rota de logout
@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


#FORMATO DE FORMULÁRIO NÃO RECOMENDADO
#criando outra rota
@app.route('/contato_old/', methods=['GET', 'POST'])
@login_required
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
@app.route('/contato/', methods=['GET', 'POST'])
@login_required
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


#criando nova view para a lista de contatos
@app.route('/contato/lista/')
@login_required
def contato_lista():

    # Barrando o acesso a uma página de um usuário com base no ID
    if current_user.id == 1: return redirect(url_for('homepage'))

    #verificando se a requisição foi GET
    if request.method == 'GET':
        #pegando os argumentos pesquisados
        pesquisa = request.args.get('pesquisa', '')

    #buscando todos os contatos do banco de dados
    dados = Contato.query.order_by('nome') #query pega todos os dados do banco de dados e order by ordena por nome

    #se a pesquisa for diferente de vazio
    if pesquisa != '':
        #filtro a pesquisa
        dados = dados.filter_by(nome = pesquisa)

    # Passando os dados para o contexto
    context = {'dados':dados.all()}

    #retorno o HTML da lista de contatos
    return render_template('contato_lista.html', context=context)


# Criando rota dinâmica
@app.route('/contato/<int:id>/')
@login_required
def contato_detail(id):

    # Pegando o dado do contato e salvando em um objeto pelo ID
    obj = Contato.query.get(id)
    return render_template('contato_detail.html', obj=obj)


# Rota de criação de post
@app.route('/post/novo/', methods=['GET', 'POST'])
@login_required
def post_novo():
    # Definindo o formulário do post
    form = PostForm()
    # Se o posto foi valido e submetido
    if form.validate_on_submit():
        #salvo o post com o usuario atual
        form.save(current_user.id)
        # redireciono para a homepage
        return redirect(url_for('homepage'))
    # Retornando o HTML do post
    return render_template('post_novo.html', form=form)

#Rota para detalhes do post dinamico
@app.route('/post/<int:id>/', methods=['GET', 'POST'])
@login_required
def post_detail(id):
    #pegando o dado do post e salvando em um objeto pelo id
    obj = Post.query.get(id)
    # Pegando o formulário para comentar no post
    form = ComentarioForm()
    # Se o formulário foi valido e submetivo
    if form.validate_on_submit():
        # salva o usuário e o post atual
        form.save(current_user.id, id)
        # Recarrego a página com o post
        return redirect(url_for('post_detail', id=id))
    # Retornando o HTML do post
    return render_template('post.html', obj=obj, form=form)

# Rota de lista de posts
@app.route('/post/lista/')
@login_required
def post_lista():
    # Pegando todos os posts
    posts = Post.query.all()
    return render_template('post_lista.html', posts=posts)



