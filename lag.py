# pip install streamlit
# pip install streamlit-lottie
# cd C:/Users/joao.souza/Music/Biblioteca
# streamlit run lag.py
import streamlit as st
import pandas as pd
import csv
import os

# Inicialização dos dicionários para armazenamento de dados em memória
livros = {}
usuarios = {}
livros_emprestados = {}

# Funções para leitura de dados de arquivos CSV
def ler_livros():
    if os.path.exists("livros.csv"):
        with open("livros.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho do CSV
            for row in reader:
                if len(row) == 4:
                    id_livro, nome, autor, quantidade = row
                    try:
                        livros[id_livro] = {"Nome": nome, "Autor": autor, "Quantidade": int(quantidade)}
                    except ValueError:
                        print(f"Erro na conversão de quantidade para o livro {nome}. Verifique os dados.")
                else:
                    print(f"Linha ignorada (dados incompletos): {row}")


def ler_usuarios():
    if os.path.exists("usuarios.csv"):
        with open("usuarios.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho do CSV
            for row in reader:
                id_usuario, nome, endereco = row
                usuarios[id_usuario] = {"Nome": nome, "Endereço": endereco}

def ler_emprestimos():
    if os.path.exists("emprestimos.csv"):
        with open("emprestimos.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho do CSV
            for row in reader:
                id_livro, id_usuario, data = row
                livros_emprestados[id_livro] = {"Usuário": id_usuario, "Data Empréstimo": data}

# Funções para salvar dados em arquivos CSV
def salvar_livros():
    with open("livros.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nome", "Autor", "Quantidade"])
        for id_livro, info in livros.items():
            writer.writerow([id_livro, info["Nome"], info["Autor"], info["Quantidade"]])

def salvar_usuarios():
    with open("usuarios.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nome", "Endereço"])
        for id_usuario, info in usuarios.items():
            writer.writerow([id_usuario, info["Nome"], info["Endereço"]])

def salvar_emprestimos():
    with open("emprestimos.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID Livro", "ID Usuário", "Data Empréstimo"])
        for id_livro, info in livros_emprestados.items():
            writer.writerow([id_livro, info["Usuário"], info["Data Empréstimo"]])

# Carrega os dados ao iniciar a aplicação
ler_livros()
ler_usuarios()
ler_emprestimos()

# Configuração da interface do Streamlit
st.title("📚 Biblioteca Virtual")
st.markdown("Bem-vindo à biblioteca virtual! Gerencie livros, usuários e empréstimos de maneira intuitiva.")

# Criação de abas para organizar as seções
tabs = st.tabs(["Adicionar Livro", "Listar Livros Disponíveis", "Adicionar Usuário", "Listar Usuários", "Emprestar Livro", "Listar Livros Emprestados"])

# Aba Adicionar Livro
with tabs[0]:
    st.header("Adicionar Livro")
    with st.form("form_adicionar_livro"):
        id_livro = st.text_input("ID do Livro")
        nome_livro = st.text_input("Nome do Livro")
        autor_livro = st.text_input("Autor do Livro")
        quantidade = st.number_input("Quantidade de Exemplares", min_value=1, step=1)
        submit_livro = st.form_submit_button("Confirmar Adição")
        
        if submit_livro:
            livros[id_livro] = {"Nome": nome_livro, "Autor": autor_livro, "Quantidade": quantidade}
            salvar_livros()
            st.success("📚 Livro adicionado com sucesso!")

# Aba Listar Livros Disponíveis
with tabs[1]:
    st.header("Livros Disponíveis")
    livros_disponiveis = pd.DataFrame(livros).T
    if livros_disponiveis.empty:
        st.write("📭 Não há livros disponíveis no momento.")
    else:
        with st.expander("Ver livros disponíveis"):
            st.dataframe(livros_disponiveis)

# Aba Adicionar Usuário
with tabs[2]:
    st.header("Adicionar Usuário")
    with st.form("form_adicionar_usuario"):
        id_usuario = st.text_input("ID do Usuário")
        nome_usuario = st.text_input("Nome do Usuário")
        endereco_usuario = st.text_input("Endereço do Usuário")
        submit_usuario = st.form_submit_button("Confirmar Adição de Usuário")
        
        if submit_usuario:
            usuarios[id_usuario] = {"Nome": nome_usuario, "Endereço": endereco_usuario}
            salvar_usuarios()
            st.success("👤 Usuário adicionado com sucesso!")

# Aba Listar Usuários
with tabs[3]:
    st.header("Usuários Registrados")
    usuarios_registrados = pd.DataFrame(usuarios).T
    if usuarios_registrados.empty:
        st.write("📭 Não há usuários registrados no momento.")
    else:
        with st.expander("Ver usuários registrados"):
            st.dataframe(usuarios_registrados)

# Aba Emprestar Livro
with tabs[4]:
    st.header("Emprestar Livro")
    with st.form("form_emprestar_livro"):
        id_livro = st.text_input("ID do Livro para Empréstimo")
        id_usuario = st.text_input("ID do Usuário")
        data_emprestimo = st.date_input("Data de Empréstimo")
        submit_emprestimo = st.form_submit_button("Confirmar Empréstimo")
        
        if submit_emprestimo:
            if id_livro in livros and id_usuario in usuarios:
                livros_emprestados[id_livro] = {"Usuário": id_usuario, "Data Empréstimo": str(data_emprestimo)}
                salvar_emprestimos()
                st.success("📅 Livro emprestado com sucesso!")
            else:
                st.error("❌ ID do livro ou usuário não encontrado!")

# Aba Listar Livros Emprestados
with tabs[5]:
    st.header("Livros Emprestados")
    emprestados = pd.DataFrame(livros_emprestados).T
    if emprestados.empty:
        st.write("📭 Não há livros emprestados no momento.")
    else:
        with st.expander("Ver livros emprestados"):
            st.dataframe(emprestados)
