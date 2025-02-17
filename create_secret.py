# Arquivo responsável por criar a secret key para o banco de dados
import secrets

# Roda esse script para gerar uma chave secreta aleatória para o banco de dados.
sk = secrets.token_hex(36)

# Imprimindo a chave secreta
print(sk)

# ESSE SCRIPT NÃO É IMPORTANTE PARA O SITE, PODE SER DELETADO DEPOIS DE GERADO A CHAVE.