import pandas as pd
import os
from time import sleep
import csv

livros = {}
usuarios = {}
livros_emprestados = {}

class livro:
    def adicionar_livro(id, nome, autor, quantidade):
        livro = {'Id do Livro:': id, 'Nome do Livro:': nome, 'Autor do Livro:': autor, 'Quantidade de Exemplares:': quantidade}
        if nome not in livros: 
            livros[nome] = livro
            print('\nLivro adicionado com Sucesso!!')
            sleep(2)
        else:
            print(f'\nO livro "{nome}" já está na lista de livros!')
            sleep(2)

    def listar_disponiveis():
        livros_disponiveis = pd.DataFrame(livros).T
        if livros_disponiveis.empty:
            print("\nNão há livros disponíveis!")
        else:
            print(livros_disponiveis)
        sleep(7)

class usuario:
    def adicionar_usuario(id, nome, end):
        usuario = {'Id do Usuário:': id, 'Nome do Usuário:': nome, 'Endereço:': end, 'Livros Emprestados:': 0, 'Histórico de Leitura:': []} 
        for dado in usuarios.values():
            if id == dado['Id do Usuário:']:
                print(f"\nJá existe um usuário com o ID {id}, nome: {dado['Nome do Usuário:']}!")
                sleep(2)
                return
        usuarios[nome] = usuario
        print("\nUsuário adicionado com sucesso!")
        sleep(2)

    def listar_usuarios():
        if usuarios:
            lista_usuarios = pd.DataFrame(usuarios).T
            print(lista_usuarios)
        else:
            print('\nNão há usuários adicionados.')
        sleep(4)

class emprestimo: # 3h só para fazer a lógica dessa classe
    def emprestar_livro(nomelivro, nomeusuario, dataemprestimo):
        if nomelivro in livros:
            if livros[nomelivro]['Quantidade de Exemplares:'] >= 1:
                if nomeusuario in usuarios and usuarios[nomeusuario]['Livros Emprestados:'] < 3:
                    livros_emprestados[nomelivro] = {'Nome do Livro:': nomelivro, 'Nome do usuário responsável:': nomeusuario, 'Data de empréstimo:': dataemprestimo}
                    livros[nomelivro]['Quantidade de Exemplares:'] -= 1
                    usuarios[nomeusuario]['Livros Emprestados:'] += 1
                    print("\nLivro emprestado com sucesso!")
                else:
                    print(f"\nUsuário '{nomeusuario}' já atingiu o limite de 3 livros emprestados!")
            else:
                print(f"\nO livro '{nomelivro}' não tem exemplares disponíveis!")
        else:
            print("\nO livro não existe ou não está disponível para empréstimo!")
        sleep(2)

    def listar_emprestados():
        if livros_emprestados:
            lista_emprestados = pd.DataFrame(livros_emprestados).T
            print(lista_emprestados)
        else:
            print("\nNão há livros emprestados!")
        sleep(4)

class devolucao:
    def devolver_livro(nomelivro, nomeusuario, idlivro, autorlivro, datadevolucao):
        if nomelivro in livros_emprestados and nomeusuario in usuarios:
            del(livros_emprestados[nomelivro])
            livros[nomelivro]['Quantidade de Exemplares:'] += 1
            usuarios[nomeusuario]['Livros Emprestados:'] -= 1
            usuarios[nomeusuario]['Histórico de Leitura:'].append(nomelivro)
            salvar_usuarios()  
            print("\nLivro devolvido com sucesso!")
        else:
            print(f"\nO livro '{nomelivro}' não está emprestado.")
        sleep(2)

# Funções de Livros

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
                idlivro = row['Id do Livro:']  
                nomelivro = row['Nome do Livro:']
                autorlivro = row['Autor do Livro:'] 
                quantidade = int(row['Quantidade de Exemplares:'])
                livros[nomelivro] = {'Id do Livro:': idlivro, 'Nome do Livro:': nomelivro, 'Autor do Livro:': autorlivro, 'Quantidade de Exemplares:': quantidade}

# Funções de Usuários

def salvar_usuarios():
    with open('usuarios.csv', 'w', newline='') as csvfileusuarios:
        cabecalio = ['Id do Usuário:', 'Nome do Usuário:', 'Endereço:', 'Livros Emprestados:', 'Histórico de Leitura:']
        writer = csv.DictWriter(csvfileusuarios, fieldnames=cabecalio)
        writer.writeheader()
        for dados_usuarios in usuarios.values():
            # Converter lista em string para salvar no CSV
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


# Funções de Empréstimos

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

# PROGRAMA PRINCIPAL:

def principal():
    ler_livros()
    ler_usuarios()
    ler_emprestimos()
    while True:
        print("\n----- Sistema de Gerenciamento da Biblioteca -----")
        print("1. Adicionar Livro")
        print("2. Adicionar Usuário")
        print("3. Emprestar Livro")
        print("4. Devolver Livro")
        print("5. Listar Livros Disponíveis")
        print("6. Listar Livros Emprestados") # Nessa opção também é possível ver a quantidade de livros emprestados ao usuário, como requerido na atividade.
        print("7. Listar Usuários")
        print("8. Sair")
        
        op = int(input("Digite a opção desejada: "))
    
        if op == 1:
            id_livro = int(input("ID do livro: "))
            nome_livro = str(input("Nome do livro: ")).upper().strip()
            autor_livro = str(input("Autor do livro: ")).upper().strip()
            quantidade = int(input("Quantidade de exemplares: "))
            livro.adicionar_livro(id_livro, nome_livro, autor_livro, quantidade)
            salvar_livros()

        elif op == 2:
            id_usuario = int(input("Id do usuário: "))
            nome_usuario = str(input("Nome do usuário: ")).upper().strip()
            endereco_usuario = str(input("Digite seu endereço: ")).upper().strip()
            usuario.adicionar_usuario(id_usuario, nome_usuario, endereco_usuario)
            salvar_usuarios()
        
        elif op == 3:
            nome_livro = str(input("Digite o nome do livro a ser emprestado: ")).upper().strip()
            nome_usuario = str(input("Digite o nome do usuário responsável: ")).upper().strip()
            data_emprestimo = str(input("Digite a data de empréstimo do livro: "))
            emprestimo.emprestar_livro(nome_livro, nome_usuario, data_emprestimo)
            salvar_livros()
            salvar_emprestimos()
            salvar_usuarios()
        
        elif op == 4:
            id_livro = int(input("Digite o ID do livro emprestado: "))
            nome_livro = str(input("Digite o nome do livro a ser devolvido: ")).upper().strip()
            autor_livro = str(input("Digite o autor do livro:"))
            nome_usuario = str(input("Digite o nome do usuário responsável: ")).upper().strip()
            data_devolucao = str(input("Digite a data de devolução do livro: "))
            devolucao.devolver_livro(nome_livro, nome_usuario, id_livro, autor_livro, data_devolucao)
            salvar_livros()
            salvar_emprestimos()
            
        elif op == 5:
            livro.listar_disponiveis()
        
        elif op == 6:
            salvar_emprestimos()
            ler_usuarios()
            emprestimo.listar_emprestados()

        elif op == 7:
            ler_usuarios()
            usuario.listar_usuarios()
        
        elif op == 8:
            print("Fechando sistema...")
            sleep(1)
            print('3')
            sleep(1)
            print('2')
            sleep(1)
            print('1')
            break   
        
        else:
            print("\nOpção inválida, tente novamente!")
            sleep(2)

principal()