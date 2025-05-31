import json
import hashlib
import time
import statistics
import os
import re
from getpass import getpass  # para ocultar a senha
 
DB_FILE = "usuarios.json"
TERMO_LGPD = "Ao se cadastrar, você aceita os termos da LGPD e autoriza o uso de seus dados apenas para fins educacionais e estatísticos."
 
def carregar_dados():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Arquivo de dados corrompido. Será recriado.")
        return {}
 
def salvar_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)
 
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()
 
def email_valido(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None
 
def cadastrar_usuario():
    print("\n👤 Cadastro de Usuário")
    nome = input("Nome: ")
 
    while True:
        try:
            idade = int(input("Idade: "))
            if idade > 0:
                break
            print("Idade deve ser um número positivo.")
        except ValueError:
            print("Digite um número válido.")
 
    while True:
        email = input("Email: ").strip().lower()
        if email_valido(email):
            break
        print("❌ Email inválido. Tente novamente.")
 
    senha = getpass("Crie uma senha segura: ")
 
    dados = carregar_dados()
 
    if email in dados:
        print("❌ Usuário já cadastrado.")
        return
 
    print("\n" + TERMO_LGPD)
    confirm = input("Digite 'sim' para continuar: ").strip().lower()
    if confirm != "sim":
        print("Cadastro cancelado.")
        return
 
    dados[email] = {
        "nome": nome,
        "idade": idade,
        "senha_hash": hash_senha(senha),
        "acessos": []
    }
 
    salvar_dados(dados)
    print("✅ Usuário cadastrado com sucesso!")
 
def login():
    print("\n🔐 Login")
    tentativas = 3
    dados = carregar_dados()
 
    while tentativas > 0:
        email = input("Email: ").strip().lower()
        senha = getpass("Senha: ")
 
        user = dados.get(email)
        if user and user["senha_hash"] == hash_senha(senha):
            print(f"👋 Bem-vindo(a), {user['nome']}!")
            inicio = time.time()
            input("Pressione Enter para encerrar a sessão...")
            duracao = round(time.time() - inicio)
            user["acessos"].append(duracao)
            salvar_dados(dados)
            print(f"⏱️ Sessão registrada: {duracao} segundos.")
            return
 
        tentativas -= 1
        print(f"❌ Dados inválidas. Tentativas restantes: {tentativas}")
 
    print("🔒 Tentativas excedidas. Tente novamente mais tarde.")
 
def redefinir_senha():
    print("\n🔄 Redefinição de Senha")
    email = input("Email: ").strip().lower()
    dados = carregar_dados()
 
    if email not in dados:
        print("❌ Email não encontrado.")
        return
 
    nova_senha = getpass("Nova senha: ")
    confirm = getpass("Confirme a nova senha: ")
 
    if nova_senha != confirm:
        print("❌ As senhas não coincidem.")
        return
 
    dados[email]["senha_hash"] = hash_senha(nova_senha)
    salvar_dados(dados)
    print("🔐 Senha atualizada com sucesso.")
 
def modulo_logica_computacional():
    print("\n📘 Módulo: Lógica Computacional")
    print("Pergunta: Qual o próximo número na sequência: 2, 4, 6, 8, __?")
    tentativas = 3
    while tentativas > 0:
        resposta = input("Resposta: ").strip()
        if resposta == "10":
            print("✅ Correto!")
            return
        else:
            tentativas -= 1
            if tentativas > 0:
                print(f"❌ Tente novamente. Tentativas restantes: {tentativas}")
            else:
                print("❌ Número máximo de tentativas ja foi atingido. A resposta correta seria 10.")
 
def modulo_programacao_python():
    print("\n💻 Módulo: Programação em Python")
    nome = input("Digite seu nome: ")
    print(f"Olá, {nome}! Vamos somar dois números?")
    while True:
        try:
            x = int(input("Número 1: "))
            y = int(input("Número 2: "))
            break
        except ValueError:
            print("Digite valores válidos.")
    print(f"Resultado: {x} + {y} = {x + y}")
    print("🎉 Parabéns, você somou 2 números.")
 
def relatorios_estatisticos():
    print("\n📊 Relatórios Estatísticos")
    dados = carregar_dados()
    idades = [user["idade"] for user in dados.values()]
    acessos = [len(user["acessos"]) for user in dados.values()]
 
    if not idades:
        print("Nenhum dado disponível.")
        return
 
    print(f"👥 Idades - Média: {statistics.mean(idades):.2f}, Mediana: {statistics.median(idades)}, Moda: {statistics.mode(idades)}")
    print(f"🕒 Acessos - Média: {statistics.mean(acessos):.2f}, Mediana: {statistics.median(acessos)}, Moda: {statistics.mode(acessos)}")
 
    print("\n🏆 Top usuários por tempo total de acesso:")
    ranking = sorted(
        dados.items(),
        key=lambda item: sum(item[1]["acessos"]),
        reverse=True
    )
    for i, (email, user) in enumerate(ranking[:3], start=1):
        total = sum(user["acessos"])
        print(f"{i}º {user['nome']} ({email}) - {total} segundos")
 
def menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n=== 🎓 Plataforma de Educação Digital ===")
        print("1️⃣  Cadastrar usuário")
        print("2️⃣  Fazer login")
        print("3️⃣  Relatórios estatísticos")
        print("4️⃣  Lógica Computacional")
        print("5️⃣  Programação em Python")
        print("6️⃣  Redefinir senha")
        print("7️⃣  Sair")
 
        opcao = input("Escolha uma opção: ").strip()
       
        if not opcao.isdigit():
            print("Opção inválida. Por favor, digite um número de 1 a 7.")
        elif opcao == "1":
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
            redefinir_senha()
        elif opcao == "7":
            print("👋 Até logo!")
            break
        else:
            print("Opção inválida. Por favor, digite um número de 1 a 7.")
 
        input("\nPressione Enter para continuar...")
 
if __name__ == "__main__":
    menu()
