#importando o app do meu módulo
from app import app



#verificando se estou no programa principal
if __name__ == '__main__':
    # rodando o aplicativo em debug mode
    app.run(host='0.0.0.0', port='5555', debug=True)