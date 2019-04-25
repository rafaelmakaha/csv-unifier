import pandas as pd
import glob
import csv
import os

def get_description(maquina):
    df = pd.read_csv(maquina)
    return df.iloc[0]['Descrição']
        
def check_names(nome_lista, maquina_atual):
    return nome_lista in maquina_atual

def filter_name(nome_lista):
    return nome_lista.replace(";", "")

def listagem_maquinas():
    # Lê todos os caminhos para os arquivos das máquinas
    maquinas = glob.glob('maquinas/*.csv')
    
    # Lê a listagem de nomes das máquinas
    nomes = pd.read_csv('nomes/nomes_maquinas.csv')
    
    # Cria arquivo de saida 
    with open('lista.csv', 'w', encoding='UTF-8') as csvfile:
        filewriter = csv.writer(
            csvfile, 
            lineterminator='\n',
            delimiter=',',
            quotechar='|', 
            quoting=csv.QUOTE_MINIMAL
        )
        
        # Cria colunas
        filewriter.writerow(['Nome', 'Descricao'])

        # Percorre o nome de todas as máquinas
        for i in range(nomes.shape[0]):
            
            # Limpa o nome da máquina
            nome_puro = filter_name(nomes.iloc[i][0])

            # Procura a máquina nos arquivos individuais
            for j in range(len(maquinas)):
                
                # Caso exista, adiciona a sua descrição
                if check_names(nome_puro, maquinas[j]) == True:
                    descricao = get_description(maquinas[j])
                    filewriter.writerow([nome_puro,descricao])
                    break
                    
            # Caso não exista, adiciona informação de não exportado
            else:
                descricao = "nao exportado"
                filewriter.writerow([nome_puro,descricao])

def adiciona_novas_colunas():
    df = pd.read_csv('lista.csv')
    
    # remove a coluna de Descrição
    df = df.drop(['Descricao'], axis=1) 
    
    # Adiciona as seguintes colunas
    df['Patrimonio'] = 'Vazio'
    df['Modelo'] = 'Vazio'
    df['Setor'] = 'Vazio'
    df['Sala'] = 'Vazio'
    
    df.to_csv('nova_lista.csv', index=False)

# def adiciona_informacoes(caminho):
caminho = 'infos/Relatório de Microcomputadores agupados por UL (Endereço).csv'
count =0

def is_number(row):
    try:
        int(row[0])
        return True
    except ValueError:
        return False

cont = 0
    
# with open('teste.csv', 'w', encoding='utf-8') as csvfile:
#     filewriter = csv.writer(
#             csvfile, 
#             lineterminator='\n',
#             delimiter=',',
#             quotechar='|', 
#             quoting=csv.QUOTE_MINIMAL
#         )
        
with open(caminho, 'r', encoding='utf-8') as maquinas:
    df = pd.read_csv('nova_lista.csv')
    for row in maquinas:
        index = 0
        if 'U.A.:' in row:
            setor = row[16:-16]
            index = setor.find(' -')
            setor = setor[:index]
#                 print(setor)
        if 'Endereço:' in row:
            index = row.find('- ')
            endereco = row[index+2:-13]
            endereco = endereco.replace('SAFS QD2 LT3','')
            if '(' in endereco:
                index = endereco.find('(')
                index2 = endereco.find(')')
                setor = setor + " " + endereco[index:index2+1]
#                 print(setor)

            index = endereco.find('- ')
            index2 = endereco.find(' ', index+7)
            sala = endereco[index+2:index2]
            sala = sala.replace('SALA ','')
            sala = sala.replace(' (SALA','')
#                 sala = ""
#                 print(endereco)
#                 print(endereco)
#             print(sala)
#                 print("")


        if '3000' in row:
            index = row.find('3000')
#                 print(index)
            patrimonio = row[index:index+8]
#                 print(patrimonio)
            if not 'MODELO:' in row:
                modelo = ""
            else:
                index = row.find('MODELO:')
                index2 = row.find('-', index)
                modelo = row[index+8:index2-1]
#                 print(modelo)
            
            for i in range(df.shape[0]):
                if patrimonio in df.iloc[i]['Nome']:
                    df.at[i,'Patrimonio'] = patrimonio
                    df.at[i,'Modelo'] = modelo
                    df.at[i,'Setor'] = setor
                    df.at[i,'Sala'] = sala
                    print(df.iloc[i])
                
# df
#     print(cont)
df.to_csv('nova_lista.csv', index=False)


listagem_maquinas()

adiciona_novas_colunas()

df = pd.read_csv('nova_lista.csv')
for i in range(df.shape[0]):
    if '(DEPOSITO' in df.iloc[i]['Sala']:
        novo = df.iloc[i]['Sala']
        novo = novo.replace(' (DEPOSITO', '')
        df.at[i,'Sala'] = novo
df.to_csv('nova_lista.csv', index=False)

df = pd.read_csv('nova_lista.csv')
df.iloc[0]['Sala']
