import os
import json
import getpass
from datetime import datetime

### ↓  ↓ ###
### ↑  ↑ ###

### ↓ Json files ↓ ###
with open('barcode.json', 'r') as f:
    barcode = json.load(f)

with open('notebooks_in_stock.json', 'r') as f:
    notebooks_in_stock = json.load(f)

with open('notebooks_in_events.json', 'r') as f:
    notebooks_in_events = json.load(f)

with open('notebooks_out_of_use.json', 'r') as f:
    notebooks_out_of_use = json.load(f)
### ↑ Json files ↑ ###

### ↓ Clear function ↓ ###
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
cls()
### ↑ Clear function ↑ ###

### ↓ Time ↓ ###
currentTime = datetime.now()
time = '{}:{}:{} no dia {}/{}/{}'.format(currentTime.hour, currentTime.minute, currentTime.second, currentTime.day, currentTime.month, currentTime.year)
### ↑ Time ↑ ###


### ↓ Login ↓ ###
users = ['henrique@pleno', 'daniel@pleno', 'rogerio@pleno', 'motta@pleno', 'fonseca@pleno', 'rodrigo@pleno']

def login():
    global user
    user = getpass.getpass('ID: ')
    if user in users:
        logs = open('logs.txt', '+a')
        logs.write('\nACCESS: Usuário {} conectado ás {}'.format(user, time))
        logs.close()
        cls()
        print('SISTEMA: Acesso Autorizado!')
        menu()
    else:
        cls()
        print('ERROR: Usuário inválido!')
        login()
### ↑ Login ↑ ###

### ↓ Menu ↓ ###
def menu():
    print('\n========= MENU =========\n\n[1] Retirar Notebook \n[2] Devolver Notebook \n[3] Resumo estoque \n[4] Lista de notebooks fora de uso \n[0] Sair\n')
    choice = input('Digite o número da opção desejada:')
    cls()
    if choice == '1':
        withdraw()
    elif choice == '2':
        return_notebook()
    elif choice == '3':
        notebooks_details()
        menu()
    elif choice == '4':
        out_of_use()
    elif choice == '0':
        login()
    else:
        print('ERROR: Opção inválida.')
        menu()
### ↑ Menu ↑ ###

### ↓ Print notebooks details ↓ ###
def notebooks_details():
    print('\n========= Resumo notebooks =========')
    print_notebooks_in_stock()
    print_notebooks_in_events()
    print_notebooks_out_of_use()
### ↑ Print notebooks details ↑ ###

### ↓ Print Notebooks in stock ↓ ###
def print_notebooks_in_stock():
    total_notebooks_in_stock = len(notebooks_in_stock.keys())
    print('\n    ↓ Notebooks no estoque Total: {} ↓'.format(total_notebooks_in_stock))
    for key, value in notebooks_in_stock.items():
        print(key, ': ', value)
    print('    ↑ Notebooks no estoque Total: {} ↑'.format(total_notebooks_in_stock))
### ↑ Print Notebooks in stock ↑ ###

### ↓ Print notebooks in events ↓ ###
def print_notebooks_in_events():
    total_notebooks_in_events = len(notebooks_in_events.keys())
    print('\n    ↓ Notebooks em eventos Total: {} ↓'.format(total_notebooks_in_events))
    for key, value in notebooks_in_events.items():
        print(key, ': ', value)
    print('    ↑ Notebooks em eventos Total: {} ↑'.format(total_notebooks_in_events))
### ↑ Print notebooks in events ↑ ###

### ↓ Print_notebooks_out_of_use ↓ ###
def print_notebooks_out_of_use():
    total_notebooks_out_of_use = len(notebooks_out_of_use.keys())
    print('\n    ↓ Notebooks fora de uso Total: {} ↓'.format(total_notebooks_out_of_use))
    for key, value in notebooks_out_of_use.items():
        print(key, ': ', value)
    print('    ↑ Notebooks fora de uso Total: {} ↑'.format(total_notebooks_out_of_use))
### ↑ Print_notebooks_out_of_use ↑ ###

### ↓ Withdraw from stock ↓ ###
def withdraw():
    print_notebooks_in_stock()
    scanned_barcode = getpass.getpass('\nEscaneie o código de barras do notebook que você deseja retirar do estoque:')
    if scanned_barcode in barcode:
        selected_notebook = barcode.get(scanned_barcode)
        if selected_notebook in notebooks_in_stock:
            event = 'Evento ' + input('Nome do evento:')
            data = 'Retorna ' + input('Data de retorno:')
            logs = open('logs.txt', 'a+')
            logs.write('\nWITHDRAW: Usuário {} retirou o notebook {} ás '.format(user, selected_notebook) + time + ' para o Evento: ' + event)
            logs.close()
            notebooks_in_stock.pop(selected_notebook)
            notebooks_in_events[selected_notebook] = (event, data)
            with open('notebooks_in_stock.json', 'w') as f:
                json.dump(notebooks_in_stock, f)
            with open('notebooks_in_events.json', 'w') as f:
                json.dump(notebooks_in_events, f)
            cls()
            print_notebooks_in_stock()
            print_notebooks_in_events()
            print('\n{} retirado com sucesso.'.format(selected_notebook))
            
            def confirm_withdraw():
                choice = input('\nGostaria de retirar outro notebook? \n[1] Mesmo evento \n[2] Diferente evento \n[0] Não \nDigite o número da opção desejada:')
                if choice == '1':
                    print_notebooks_in_stock()
                    scanned_barcode = getpass.getpass('\nEscaneie o código de barras do notebook que você deseja retirar do estoque:')
                    if scanned_barcode in barcode:
                        selected_notebook = barcode.get(scanned_barcode)
                        if selected_notebook in notebooks_in_stock:
                            notebooks_in_stock.pop(selected_notebook)
                            logs = open('logs.txt', 'a+')
                            logs.write('\nWITHDRAW: Usuário {} retirou o notebook {} ás '.format(user, selected_notebook) + time)
                            logs.close()
                            notebooks_in_events[selected_notebook] = (event, data)
                            with open('notebooks_in_stock.json', 'w') as f:
                                json.dump(notebooks_in_stock, f)
                            with open('notebooks_in_events.json', 'w') as f:
                                json.dump(notebooks_in_events, f)
                            cls()
                            print_notebooks_in_stock()
                            print_notebooks_in_events()
                            print('\nSISTEMA: {} retirado com sucesso.'.format(selected_notebook))
                            confirm_withdraw()
                elif choice == '2':
                    cls()
                    withdraw()
                elif choice == '0':
                    cls()
                    menu()
                else:
                    cls()
                    print('Opção inválida.')
                    menu()
            confirm_withdraw()
            menu()
        else:
            cls()
            print('ERROR: Notebook ainda está registrado que está em evento.')
            menu()
    else:
        cls()
        print("Código de barras inválido.")
        menu()
    print()
### ↑ Withdraw from stock ↑ ###

### ↓ Return notebook to stock ↓ ###
def return_notebook():
    print_notebooks_in_events()
    scanned_barcode = getpass.getpass('\nEscaneie o código de barras do notebook que você deseja retornar ao estoque:')
    if scanned_barcode in barcode:
        selected_notebook = barcode.get(scanned_barcode)
        if selected_notebook in notebooks_in_events:
            logs = open('logs.txt', '+a')
            logs.write('\nRETURN: Usuário {} retorno o notebook {} ás '.format(user, selected_notebook) + time)
            logs.close()
            notebooks_in_events.pop(selected_notebook)
            notebooks_in_stock[selected_notebook] = 'No estoque.'
            with open('notebooks_in_events.json', 'w') as f:
                json.dump(notebooks_in_events, f)
            with open('notebooks_in_stock.json', 'w') as f:
                json.dump(notebooks_in_stock, f)
            cls()
            print_notebooks_in_stock()
            print_notebooks_in_events()
            print('\nSISTEMA: {} retornado com sucesso.'.format(selected_notebook))
            def confirm_return():
                choice = input('\nGostaria de retornar outro notebook? \n[1] Sim \n[0] Não \nDigite o número da opção desejada:')
                if choice == '1':
                    return_notebook()
                elif choice == '0':
                    cls()
                    menu()
                else:
                    print('Opção inválida.')
                    menu()
            confirm_return()
        else:
            print('ERROR: Notebook ainda está registrado que está no estoque.')
    else:
        print('Código de barras inválido.')
        menu()
            
### ↑ Return notebook to stock ↑ ###

### ↓ Notebooks out of use ↓ ###
def out_of_use():
    print('\n========= Lista de notebooks fora de uso =========')
    choice = input('\n[1] Mover notebook a list de fora de uso. \n[2] Adicionar notebook ao estoque novamente. \n \nDigite o número da opção desejada:')
    if choice == '1':
        cls()
        print_notebooks_in_stock()
        print_notebooks_in_events()
        scanned_barcode = getpass.getpass('\nEscaneie o código de barras do notebook que você deseja mover para lista de fora de uso:')
        if scanned_barcode in barcode:
            selected_notebook = barcode.get(scanned_barcode)
            if selected_notebook in notebooks_in_stock or selected_notebook in notebooks_in_events:
                event = 'Evento: ' + input('Nome do evento ou local do acontecimento: ')
                date = 'Data: ' + input('Data do acontecimento: ')
                description = 'Descrição: ' + input('Descrição: ')
                logs = open('logs.txt', 'a+')
                logs.write('\nOUT-OF-USE: Usuário: {} moveu {} para fora de uso ás '.format(user, selected_notebook) + time)
                logs.close()
                try:
                    notebooks_in_stock.pop(selected_notebook)
                except:
                    notebooks_in_events.pop(selected_notebook)
                notebooks_out_of_use[selected_notebook] = (event, date, description)
                with open('notebooks_in_stock.json', 'w') as f:
                    json.dump(notebooks_in_stock, f)
                with open('notebooks_in_events.json', 'w') as f:
                    json.dump(notebooks_in_events, f)
                with open('notebooks_out_of_use.json', 'w') as f:
                    json.dump(notebooks_out_of_use, f)
                cls()
                print_notebooks_out_of_use()
                print('\nSISTEMA: {} movido para a lista de notebooks fora de uso com sucesso!'.format(selected_notebook))
                menu()
            else:
                print('ERROR: Notebook não está registrado em evento ou que está no estoque.')
                menu()
        else:
            print('ERROR: Código de barras inválido.')
            menu()
    elif choice == '2':
        cls()
        print_notebooks_out_of_use()
        scanned_barcode = getpass.getpass('\nEscaneie o código de barras do notebook que você deseja mover para o estoque novamente:')
        if scanned_barcode in barcode:
            selected_notebook = barcode.get(scanned_barcode)
            if selected_notebook in notebooks_out_of_use:
                logs = open('logs.txt', '+a')
                logs.write('\nFIXED: Usuário {} retorno o notebook {} para o estoque ás '.format(user, selected_notebook) + time)
                logs.close()
                notebooks_out_of_use.pop(selected_notebook)
                notebooks_in_stock[selected_notebook] = 'No estoque'
                with open('notebooks_out_of_use.json', 'w') as f:
                    json.dump(notebooks_out_of_use, f)
                with open('notebooks_in_stock.json', 'w') as f:
                    json.dump(notebooks_in_stock, f)
                cls()
                print_notebooks_in_stock()
                print_notebooks_out_of_use()
                print('\nSISTEMA: {} adicionado novamente ao estoque.'.format(selected_notebook))
                menu()
            else:
                print('ERROR: Código do notebook escaneado não faz parte da lista de notebooks fora de uso!')
                menu()
        else:
            print('ERROR: Código de barras inválido!')
            menu()
    else:
        print('ERROR: Opção inválida.')
        menu()
        
### ↑ Notebooks out of use ↑ ###

login()