import json
import hashlib
import time
import statistics
import os

DB_FILE = "usuarios.json"
TERMO_LGPD = "Ao se cadastrar, você aceita os termos da LGPD e autoriza o uso de seus dados apenas para fins educacionais e estatísticos."

def carregar_dados():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(DB_FILE, "w") as f:
        json.dump(dados, f, indent=4)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    email = input("Email: ")
    senha = input("Crie uma senha segura: ")
    
    dados = carregar_dados()
    if email in dados:
        print("Usuário já cadastrado.")
        return

    print("\n" + TERMO_LGPD)
    confirm = input("Digite 'sim' para continuar: ").strip().lower()
    if confirm != 'sim':
        print("Cadastro cancelado.")
        return

    dados[email] = {
        "nome": nome,
        "idade": idade,
        "senha_hash": hash_senha(senha),
        "acessos": []
    }
    salvar_dados(dados)
    print("Usuário cadastrado com sucesso!")

def login():
    print("\n--- Login ---")
    email = input("Email: ")
    senha = input("Senha: ")

    dados = carregar_dados()
    user = dados.get(email)
    if not user or user["senha_hash"] != hash_senha(senha):
        print("Credenciais inválidas.")
        return

    print(f"Bem-vindo(a), {user['nome']}!")
    inicio = time.time()
    input("Pressione Enter para encerrar a sessão...")
    fim = time.time()
    duracao = round(fim - inicio)

    user["acessos"].append(duracao)
    salvar_dados(dados)
    print(f"Tempo de sessão registrado: {duracao} segundos.")

def modulo_logica_computacional():
    print("\n📘 Módulo: Lógica Computacional")
    print("1. O que é lógica?")
    print("2. Exercício: Qual a saída lógica da expressão: (True and False) or True?")
    resposta = input("Digite sua resposta (True/False): ").strip()
    if resposta.lower() == "true":
        print("✅ Correto! Vamos continuar aprendendo!")
    else:
        print("❌ Não é isso. Revise a operação lógica AND/OR.")

def modulo_programacao_python():
    print("\n💻 Módulo: Programação em Python")
    print("1. Introdução ao Python: print, variáveis, tipos de dados.")
    nome = input("Digite seu nome para praticar: ")
    print(f"Olá, {nome}! Vamos praticar uma operação simples.")
    x = int(input("Digite um número: "))
    y = int(input("Digite outro número: "))
    print(f"A soma de {x} + {y} é: {x + y}")
    print("🎉 Parabéns por completar o exercício!")

def menu():
    while True:
        print("\n=== Plataforma de Educação Digital ===")
        print("1. Cadastrar usuário")
        print("2. Fazer login")
        print("3. Relatórios estatísticos")
        print("4. Lógica Computacional")
        print("5. Programação em Python")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            login()
        elif opcao == "3":
            relatorios_estatisticos()
        elif opcao == "4":
            modulo_logica_computacional()
        elif opcao == "5":
            modulo_programacao_python()
        elif opcao == "6":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

def relatorios_estatisticos():
    print("\n--- Relatórios Estatísticos ---")
    dados = carregar_dados()
    idades = []
    acessos = []

    for user in dados.values():
        idades.append(user["idade"])
        acessos.append(len(user["acessos"]))

    if not idades:
        print("Nenhum dado disponível.")
        return

    print(f"Idade - Média: {statistics.mean(idades):.2f}, Moda: {statistics.mode(idades)}, Mediana: {statistics.median(idades)}")
    print(f"Acessos - Média: {statistics.mean(acessos):.2f}, Moda: {statistics.mode(acessos)}, Mediana: {statistics.median(acessos)}")

if __name__ == "__main__":
    menu()
