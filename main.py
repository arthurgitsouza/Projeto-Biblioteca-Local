import pandas as pd
from tabulate import  tabulate
from time import sleep

livros = {}
usuarios = {}
livros_emprestados = {}

class livro:
    def adicionar_livro(id, nome, autor):
       livro = {'Id do Livro: ': {id}, 'Nome do Livro:': {nome}, 'Autor do Livro': {autor}} 
       if nome not in livros: 
            livros[nome] = livro
            print('\nLivro adicionado com Sucesso!!')
            print(livros)
       else:
           print(f'\n Não foi possivel adicionar, pois o livro "{nome}" já está adicionado a lista de livros da biblioteca com o respectivo id: {id}!')
       

class usuario:
    def adicionar_usuario(id, nome):
        usuario = {'Id do Usuário: ': {id}, 'Nome do Usuário:' : {nome}}
        if nome not in usuarios:
            usuarios[nome] = usuario
            print("\nUsuário Adicionado com Sucesso!")
        else:
            print(f"\nNão foi possível adicionar, pois já existe um usuário com esse ID!")
        
class emprestimo:
    def emprestar_livro(nomelivro, nomeusuario):
        livro = {'Nome do Livro:': {nomelivro}, 'Nome do usuário responsável' : {nomeusuario}} 
        if nomelivro in livros:
            if nomelivro not in livros_emprestados:
                livros_emprestados[nomelivro] = livro
                print("\nLivro emprestado com sucesso!")
                print(livros)
            if nomelivro in livros:
                del(livros[nomelivro])    
            else:
                print(f'\nO livro "{nomelivro}" já foi emprestado! Tente novamente.')
        else:
            print("\nO livro não consta dentre os disponiveis para o empréstimo! Tente novamente.")
                
class devolucao:
    def devolver_livro(nomelivro, nomeusuario, idlivro, nomeautor):
        if nomelivro in livros_emprestados:
            del(livros_emprestados[nomelivro])
            if nomelivro not in livros:
                livro = {'Id do Livro: ': {idlivro}, 'Nome do Livro:': {nomelivro}, 'Autor do Livro': {nomeautor}} 
                livros[nomelivro] = livro
                print("Livro devolvido com sucesso!")
                print(livros)
        else:
            print(f"\nO livro {nomelivro} não consta na lista de livros emprestados ou não existe! Tente novamente.")
            
        
def principal():
    while True:
        print("\n----- Sistema de Gerenciamento da Biblioteca -----")
        print("1. Adicionar Livro")
        print("2. Adicionar Usuário")
        print("3. Emprestar Livro")
        print("4. Devolver Livro")
        print("5. Listar Livros Disponíveis")
        print("6. Sair")
        
        op = int(input("Digite a opção desejada: "))
    
        if op == 1:
            id_livro = int(input("ID do livro: "))
            nome_livro = str(input("Nome do livro: ")).upper().strip()
            autor_livro = str(input("Autor do livro: ")).upper().strip()
            livro.adicionar_livro(id_livro, nome_livro, autor_livro)
            
        elif op == 2:
            id_usuario = int(input("Id do usuário: "))
            nome_usuario = str(input("Nome do usuário: "))
            usuario.adicionar_usuario(id_usuario, nome_usuario)
        
        elif op == 3:
            nome_livro = str(input("Digite o nome do livro a ser emprestado: ")).upper().strip()
            nome_usuario = str(input("Digite o nome do usuário responsável: ")).upper().strip()
            emprestimo.emprestar_livro(nome_livro, nome_usuario)
        
        elif op == 4:
            id_livro = int(input("Digite o ID do livro emprestado: "))
            nome_livro = str(input("Digite o nome do livro a ser devolvido: ")).upper().strip()
            autor_livro = str(input("Digite o autor do livro:"))
            nome_usuario = str(input("Digite o nome do usuário responsável: ")).upper().strip()
            devolucao.devolver_livro(nome_livro, nome_usuario, id_livro, autor_livro)
            
        if op > 6:
            print("\nOpção inválida, tente novamente!")
            
        if op == 6:
            print("Fechando sitema...")
            sleep(1)
            print('3')
            sleep(1)
            print('2')
            sleep(1)
            print('1')
            break   
        
        
principal()
