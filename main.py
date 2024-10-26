import pandas as pd
import os
from tabulate import  tabulate
from time import sleep
import csv

livros = {}
usuarios = {}
livros_emprestados = {}
# Depois usar um contador para contar a quantidade de usuarios e livros para usar como index na tabela!
class livro:
    def adicionar_livro(id, nome, autor):
       livro = {'Id do Livro:': id, 'Nome do Livro:': nome, 'Autor do Livro:': autor} 
       if nome not in livros: 
            livros[nome] = livro
            print('\nLivro adicionado com Sucesso!!')
            print(livros)
            sleep(2)
       else:
           print(f'\n Não foi possivel adicionar, pois o livro "{nome}" já está adicionado a lista de livros da biblioteca!')
           sleep(2)
           
    def listar_disponiveis():
        livros_disponiveis = pd.DataFrame(livros).T
        print(livros_disponiveis)
        sleep(4)

class usuario:
    def adicionar_usuario(id, nome):
        usuario = {'Id do Usuário: ': id, 'Nome do Usuário:' : nome}
        for dado in usuarios.values():
            if id == dado['Id do Usuário: ']: #cap2 slide DataCamp
                print(f"\nNão foi possível adicionar, pois já existe um usuário com o ID {id}, cujo nome é {dado['Nome do Usuário:']}!")
                sleep(2)
                return # O uso do return é para encerrar a função pois já existe o ID
        usuarios[nome] = usuario
        print("\nUsuário Adicionado com Sucesso!")
        sleep(2)
            
    def listar_usuarios():
        lista_usuarios = pd.DataFrame(usuarios)
        print(lista_usuarios)
        sleep(4)      
            
class emprestimo:
    def emprestar_livro(nomelivro, nomeusuario):
        livro = {'Nome do Livro:': nomelivro, 'Nome do usuário responsável' : nomeusuario} 
        if nomelivro in livros:
            if nomelivro not in livros_emprestados:
                livros_emprestados[nomelivro] = livro
                print("\nLivro emprestado com sucesso!")
                print(livros)
            if nomelivro in livros:
                del(livros[nomelivro])    
            else:
                print(f'\nO livro "{nomelivro}" já foi emprestado! Tente novamente.')
            sleep(2)
        else:
            print("\nO livro não consta dentre os disponiveis para o empréstimo! Tente novamente.")
            sleep(2)
            
    def listar_emprestados():
        emprestados = pd.DataFrame(livros_emprestados).T
        print(emprestados) 
        sleep(4)
        
class devolucao:
    def devolver_livro(nomelivro, nomeusuario, idlivro, nomeautor):
        if nomelivro in livros_emprestados:
            del(livros_emprestados[nomelivro])
            if nomelivro not in livros:
                livro = {'Id do Livro: ': {idlivro}, 'Nome do Livro:': {nomelivro}, 'Autor do Livro': {nomeautor}} 
                livros[nomelivro] = livro
                print("Livro devolvido com sucesso!")
                print(livros)
                sleep(2)
        else:
            print(f"\nO livro {nomelivro} não consta na lista de livros emprestados ou não existe! Tente novamente.")
            sleep(2) 

# FUNÇÕES DE ARQUIVO:
         
def salvar_livros():
    with open('livros.csv', 'w', newline="") as csvfile: 
        cabecalio = ['Id do Livro', 'Nome do Livro', 'Nome do Autor']
        writer = csv.DictWriter(csvfile, fieldnames = cabecalio) # Fieldnames é o mesmo que cabeçalio
        for livro, dados_livros in livros.items(): # Livro: keys | Dados_livros: values
            # Mapeamento do dict:
            writer.writerow({
                'Id do Livro' : dados_livros['Id do Livro:'],
                'Nome do Livro' : dados_livros['Nome do Livro:'], # Lembrar das virgulas!
                'Nome do Autor' : dados_livros['Autor do Livro:']
                    })
            
def ler_livros():
    with open('livros.csv', 'r', newline='') as csvfile:
        if os.path.exists('livros.csv'): # Pois se ainda não existir, não há como fazer leitura e apresenta erro!
            reader = csv.DictReader(csvfile)
            for row in reader: # Extração das informações
                idlivro = row['Id do Livro']
                nomelivro = row['Nome do Livro']
                autorlivro = row['Nome do Autor']

                livros[nomelivro] = {'Id do Livro:' : idlivro,  'Nome do Livro:' : nomelivro, 'Autor do Livro:' : autorlivro}
    

# Programa Principal: 

def principal():
    while True:
        print("\n----- Sistema de Gerenciamento da Biblioteca -----")
        print("1. Adicionar Livro")
        print("2. Adicionar Usuário")
        print("3. Emprestar Livro")
        print("4. Devolver Livro")
        print("5. Listar Livros Disponíveis")
        print("6. Listar Livros Emprestados")
        print("7. Listar Usuários")
        print("8. Sair")
        
        salvar_livros()
        ler_livros()
        
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
            
        elif op == 5:
            livro.listar_disponiveis()
        
        elif op == 6:
            emprestimo.listar_emprestados()
        
        elif op == 7:
            usuario.listar_usuarios()
        
        elif op == 8:
            print("Fechando sitema...")
            sleep(1)
            print('3')
            sleep(1)
            print('2')
            sleep(1)
            print('1')
            break   
        
        else:
            if op > 8:
                print("\nOpção inválida, tente novamente!")
                    
principal()
 