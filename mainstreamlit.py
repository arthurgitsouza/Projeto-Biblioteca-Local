# pip install streamlit
# pip install streamlit-lottie
# cd C:/Users/joao.souza/Music/Biblioteca
# streamlit run mainstreamlit.py

import pandas as pd
import os
import streamlit as st
import csv

st.set_page_config(page_title="Sistema de Gerenciamento da Biblioteca", page_icon="📚", layout="wide")

livros = {}
usuarios = {}
livros_emprestados = {}

class Livro:
    @staticmethod
    def adicionar_livro(id, nome, autor, quantidade):
        livro = {'Id do Livro:': id, 'Nome do Livro:': nome, 'Autor do Livro:': autor, 'Quantidade de Exemplares:': quantidade}
        if nome not in livros: 
            livros[nome] = livro
            return True
        else:
            return False

    @staticmethod
    def listar_disponiveis():
        return pd.DataFrame(livros).T

class Usuario:
    @staticmethod
    def adicionar_usuario(id, nome, end):
        usuario = {'Id do Usuário:': id, 'Nome do Usuário:': nome, 'Endereço:': end, 'Livros Emprestados:': 0, 'Histórico de Leitura:': []} 
        for dado in usuarios.values():
            if id == dado['Id do Usuário:']:
                return False
        usuarios[nome] = usuario
        return True

    @staticmethod
    def listar_usuarios():
        return pd.DataFrame(usuarios).T

class Emprestimo:
    @staticmethod
    def emprestar_livro(nomelivro, nomeusuario, dataemprestimo):
        if nomelivro in livros:
            if livros[nomelivro]['Quantidade de Exemplares:'] >= 1:
                if nomeusuario in usuarios and usuarios[nomeusuario]['Livros Emprestados:'] < 3:
                    livros_emprestados[nomelivro] = {'Nome do Livro:': nomelivro, 'Nome do usuário responsável:': nomeusuario, 'Data de empréstimo:': dataemprestimo}
                    livros[nomelivro]['Quantidade de Exemplares:'] -= 1
                    usuarios[nomeusuario]['Livros Emprestados:'] += 1
                    return True
                else:
                    return "Usuário já atingiu o limite de 3 livros emprestados!"
            else:
                return "O livro não tem exemplares disponíveis!"
        else:
            return "O livro não existe ou não está disponível para empréstimo!"

    @staticmethod
    def listar_emprestados():
        return pd.DataFrame(livros_emprestados).T

class Devolucao:
    @staticmethod
    def devolver_livro(nomelivro, nomeusuario):
        if nomelivro in livros_emprestados:
            if nomeusuario in usuarios:
                # Remove o livro da lista de emprestados
                del livros_emprestados[nomelivro]
                # Adiciona um exemplar de volta
                livros[nomelivro]['Quantidade de Exemplares:'] += 1
                usuarios[nomeusuario]['Livros Emprestados:'] -= 1
                usuarios[nomeusuario]['Histórico de Leitura:'].append(nomelivro)
                return True
            else:
                return "Usuário não encontrado."
        else:
            return "O livro não está emprestado."

# Funções de leitura e escrita em CSV
# Funções de leitura e escrita em CSV
def salvar_livros():
    with open('livros.csv', 'w', newline="") as csvfile: 
        cabecalio = ['Id do Livro:', 'Nome do Livro:', 'Autor do Livro:', 'Quantidade de Exemplares:']
        writer = csv.DictWriter(csvfile, fieldnames=cabecalio)
        writer.writeheader()
        for livro, dados_livros in livros.items():
            writer.writerow(dados_livros)

def ler_livros():
    if os.path.exists('livros.csv'):
        with open('livros.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nomelivro = row['Nome do Livro:']
                # Converter a quantidade de exemplares para um inteiro
                row['Quantidade de Exemplares:'] = int(row['Quantidade de Exemplares:'])
                livros[nomelivro] = row


def salvar_usuarios():
    with open('usuarios.csv', 'w', newline='') as csvfileusuarios:
        cabecalio = ['Id do Usuário:', 'Nome do Usuário:', 'Endereço:', 'Livros Emprestados:', 'Histórico de Leitura:']
        writer = csv.DictWriter(csvfileusuarios, fieldnames=cabecalio)
        writer.writeheader()
        for dados_usuarios in usuarios.values():
            dados_usuarios['Histórico de Leitura:'] = ','.join(dados_usuarios['Histórico de Leitura:'])
            writer.writerow(dados_usuarios)

def ler_usuarios():
    if os.path.exists('usuarios.csv'):
        with open('usuarios.csv', 'r', newline='') as csvfileusuarios:
            reader = csv.DictReader(csvfileusuarios)
            for row in reader:
                nomeusuario = row['Nome do Usuário:']
                if row['Histórico de Leitura:']:
                    row['Histórico de Leitura:'] = row['Histórico de Leitura:'].split(',')
                else:
                    row['Histórico de Leitura:'] = []
                row['Livros Emprestados:'] = int(row['Livros Emprestados:'])
                usuarios[nomeusuario] = row

def salvar_emprestimos():
    with open('emprestimos.csv', 'w', newline='') as csvfileemprestimos:
        cabecalio = ['Nome do Livro:', 'Nome do usuário responsável:', 'Data de empréstimo:']
        writer = csv.DictWriter(csvfileemprestimos, fieldnames=cabecalio)
        writer.writeheader()
        for dados_livrosemprestados in livros_emprestados.values():
            writer.writerow(dados_livrosemprestados)

def ler_emprestimos():
    if os.path.exists('emprestimos.csv'):
        with open('emprestimos.csv', 'r', newline="") as csvfileemprestimos:
            reader = csv.DictReader(csvfileemprestimos)
            for row in reader:
                nomelivro = row['Nome do Livro:']
                livros_emprestados[nomelivro] = row

# Carregando dados
ler_livros()
ler_usuarios()
ler_emprestimos()

# Interface do Streamlit
st.title("Sistema de Gerenciamento da Biblioteca")
st.sidebar.header("Menu")

menu = ["Adicionar Livro", "Adicionar Usuário", "Emprestar Livro", "Devolver Livro", "Listar Livros Disponíveis", "Listar Livros Emprestados", "Listar Usuários"]
op = st.sidebar.selectbox("Selecione uma opção:", menu)

# Estilo de Feedback
def feedback_message(success, message):
    if success:
        st.success(message)
    else:
        st.warning(message)

if op == "Adicionar Livro":
    st.header("📚 Adicionar Livro")
    col1, col2 = st.columns(2)
    with col1:
        id_livro = st.number_input("ID do livro:", min_value=1)
        nome_livro = st.text_input("Nome do livro:").upper().strip()
    with col2:
        autor_livro = st.text_input("Autor do livro:").upper().strip()
        quantidade = st.number_input("Quantidade de exemplares:", min_value=1)
    
    if st.button("Adicionar"):
        if Livro.adicionar_livro(id_livro, nome_livro, autor_livro, quantidade):
            feedback_message(True, "Livro adicionado com sucesso!")
            salvar_livros()
        else:
            feedback_message(False, f'O livro "{nome_livro}" já está na lista!')

elif op == "Adicionar Usuário":
    st.header("👤 Adicionar Usuário")
    col1, col2 = st.columns(2)
    with col1:
        id_usuario = st.number_input("ID do usuário:", min_value=1)
        nome_usuario = st.text_input("Nome do usuário:").upper().strip()
    with col2:
        endereco_usuario = st.text_input("Digite seu endereço:").upper().strip()
    
    if st.button("Adicionar"):
        if Usuario.adicionar_usuario(id_usuario, nome_usuario, endereco_usuario):
            feedback_message(True, "Usuário adicionado com sucesso!")
            salvar_usuarios()
        else:
            feedback_message(False, f"Já existe um usuário com o ID {id_usuario}.")

elif op == "Emprestar Livro":
    st.header("📖 Emprestar Livro")
    nome_livro = st.text_input("Nome do livro a ser emprestado:").upper().strip()
    nome_usuario = st.text_input("Nome do usuário responsável:").upper().strip()
    data_emprestimo = st.text_input("Data de empréstimo do livro:")
    
    if st.button("Emprestar"):
        resultado = Emprestimo.emprestar_livro(nome_livro, nome_usuario, data_emprestimo)
        if resultado == True:
            feedback_message(True, "Livro emprestado com sucesso!")
            salvar_emprestimos()
        else:
            feedback_message(False, resultado)

elif op == "Devolver Livro":
    st.header("🔄 Devolver Livro")
    nome_livro = st.text_input("Nome do livro a ser devolvido:").upper().strip()
    nome_usuario = st.text_input("Nome do usuário responsável:").upper().strip()
    
    if st.button("Devolver"):
        resultado = Devolucao.devolver_livro(nome_livro, nome_usuario)
        if resultado == True:
            feedback_message(True, "Livro devolvido com sucesso!")
            salvar_emprestimos()
        else:
            feedback_message(False, resultado)

elif op == "Listar Livros Disponíveis":
    st.header("📖 Livros Disponíveis")
    livros_disponiveis = Livro.listar_disponiveis()
    st.dataframe(livros_disponiveis)

elif op == "Listar Livros Emprestados":
    st.header("📚 Livros Emprestados")
    emprestados = Emprestimo.listar_emprestados()
    st.dataframe(emprestados)

elif op == "Listar Usuários":
    st.header("👥 Usuários")
    usuarios_df = Usuario.listar_usuarios()
    st.dataframe(usuarios_df)
