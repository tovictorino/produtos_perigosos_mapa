
"""

Cálculo da capacidade ferroviária utilizada.

Aplicação de teoria dos grafos à malha ferroviária
a partir dos dados da declaração de rede 2020.

"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
# pasta principal C:\2020\ANTT\REGULAMENTAÇÃO DE PRODUTOS PERIGOSOS\Mapa
# construção do grafo
## data set das estações ferroviárias em ordem
filepath = 'C:\\2020\\ANTT\\REGULAMENTAÇÃO DE PRODUTOS PERIGOSOS\\Mapa\\'
data = pd.read_excel(filepath + 'Dados\\DR-2020_Ajustado.xlsx')

## cria nós a partir da lista de estações
df = nx.from_pandas_edgelist(data, source='A', target='B', edge_attr=True)
########

# leitura da base de fluxos retirada do SAFF
"""
COLUNAS DO SAFF!!! -> CAU liberando posso tentar automatizar essa consulta 
todas as vezes que rodarmos o programa.
['Mês/Ano', 'Ferrovia', 'Mercadoria ANTT', 'Código do Fluxo',
       'Cód. Ref. Origem do Fluxo', 'Cód. Ref. Destino do Fluxo', 'TU',
       'Dist. Média (km)']
"""

fluxos = pd.read_excel(filepath+'Dados\\producao_1519_perig.xlsx')
fluxos.head()

# Mudança da sigla de estações virtuais para estações que estão na DR
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'FOB'),'Cód. Ref. Origem do Fluxo']='VOB'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'BP1'),'Cód. Ref. Origem do Fluxo']='BVP'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'BP2'),'Cód. Ref. Origem do Fluxo']='BVP'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'EBI'),'Cód. Ref. Origem do Fluxo']='EAO'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'EPW'),'Cód. Ref. Origem do Fluxo']='VWI'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'ETB'),'Cód. Ref. Origem do Fluxo']='EBJ'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'FAZ'),'Cód. Ref. Origem do Fluxo']='FEN'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'FYB'),'Cód. Ref. Origem do Fluxo']='FAB'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'FYB'),'Cód. Ref. Origem do Fluxo']='FAB'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'IJN'),'Cód. Ref. Origem do Fluxo']='ZJY'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'PIN'),'Cód. Ref. Origem do Fluxo']='PPN'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'PIP'),'Cód. Ref. Origem do Fluxo']='PPT'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'QMG'),'Cód. Ref. Origem do Fluxo']='QRO'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'VEB'),'Cód. Ref. Origem do Fluxo']='ELF'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'FTX'),'Cód. Ref. Origem do Fluxo']='FXS'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'NSR'),'Cód. Ref. Origem do Fluxo']='NSN'
fluxos.loc[(fluxos['Cód. Ref. Origem do Fluxo'] == 'NES'),'Cód. Ref. Origem do Fluxo']='NOR'

fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'FOB'),'Cód. Ref. Destino do Fluxo']='VOB'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'BP1'),'Cód. Ref. Destino do Fluxo']='BVP'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'BP2'),'Cód. Ref. Destino do Fluxo']='BVP'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'EBI'),'Cód. Ref. Destino do Fluxo']='EAO'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'EPW'),'Cód. Ref. Destino do Fluxo']='VWI'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'ETB'),'Cód. Ref. Destino do Fluxo']='EBJ'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'FAZ'),'Cód. Ref. Destino do Fluxo']='FEN'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'FYB'),'Cód. Ref. Destino do Fluxo']='FAB'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'FYB'),'Cód. Ref. Destino do Fluxo']='FAB'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'IJN'),'Cód. Ref. Destino do Fluxo']='ZJY'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'PIN'),'Cód. Ref. Destino do Fluxo']='PPN'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'PIP'),'Cód. Ref. Destino do Fluxo']='PPT'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'QMG'),'Cód. Ref. Destino do Fluxo']='QRO'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'VEB'),'Cód. Ref. Destino do Fluxo']='ELF'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'FTX'),'Cód. Ref. Destino do Fluxo']='FXS'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'NSR'),'Cód. Ref. Destino do Fluxo']='NSN'
fluxos.loc[(fluxos['Cód. Ref. Destino do Fluxo'] == 'NES'),'Cód. Ref. Destino do Fluxo']='NOR'

# Cálculo do caminho mínimo para os fluxos da base de dados
distancias = []
roteamento = {}
roteamentoCC = {}
for i,j in zip(fluxos['Cód. Ref. Origem do Fluxo'], fluxos['Cód. Ref. Destino do Fluxo']):
    menor_dist = nx.single_source_dijkstra(df, source=i, target=j, weight='Extensão (km)')
    distancias.append(round(menor_dist[0],2))
    roteamento.update({i + ' - ' + j : menor_dist[0]})
    roteamentoCC.update({i + ' - ' + j : menor_dist[1]})

# Conferência e ajuste das distâncias encontradas
## lista com a distância Dijkstra para cada fluxo e comparação com o valor do SAFF
lista = []
listaCC = []
for i,j in zip(fluxos['Cód. Ref. Origem do Fluxo'], fluxos['Cód. Ref. Destino do Fluxo']):
    conc = i + ' - ' + j
    dist = roteamento[conc]
    distCC = roteamentoCC[conc]
    lista.append(dist)
    listaCC.append(distCC)

## inserir valores de distância no dataframe dos fluxos 
fluxos['Extensão Dijkstra'] = lista
fluxos['Diferença'] = round((fluxos['Dist. Média (km)'] / fluxos['Extensão Dijkstra'])-1,2)
fluxos['Roteamento'] = listaCC
fluxos.head()

## ajuste dos roteamentos que não seguem caminho mínimo
"""
Lista dos fluxos que não seguem caminho mínimo.
Observar a planilha de exceções e atualizá-la.
Pensar se existe uma maneira melhor para a lista de exceções!

"""

fluxos['Dist.Ajustada'] = float(0)
fluxos['Roteamento'] = fluxos['Roteamento'].astype(object)
for i in range(0, len(fluxos['Extensão Dijkstra'])):
    h = 'Z51' in fluxos.iloc[i,10]
    j = 'FSI' in fluxos.iloc[i,10]
    k = 'EPM' in fluxos.iloc[i,10]
    l = 'EEL' in fluxos.iloc[i,10]
    m = 'FAR' in fluxos.iloc[i,10]
    n = 'FCT' in fluxos.iloc[i,10]
    o = 'ZAL' in fluxos.iloc[i,10]

    #Mateus Editou#
    c = 'FJC' in fluxos.iloc[i,10]


    if abs(fluxos.iloc[i,9]) > 0.05 and h == True:
        menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='ZWW', weight='Extensão (km)')
        menor_dist2 = nx.single_source_dijkstra(df, source='ZWW', target=fluxos.iloc[i,5], weight='Extensão (km)')
        menor_distTOT = menor_dist1[0]+menor_dist2[0]
        fluxos.iloc[i,8] = menor_distTOT
        fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
        n_rot = menor_dist1[1]+menor_dist2[1]
        fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]
    
    elif abs(fluxos.iloc[i,9]) > 0.05 and j == True:
        menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='FBU', weight='Extensão (km)')
        menor_dist2 = nx.single_source_dijkstra(df, source='FBU', target=fluxos.iloc[i,5], weight='Extensão (km)')
        menor_distTOT = menor_dist1[0]+menor_dist2[0]
        fluxos.iloc[i,8] = menor_distTOT
        fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
        n_rot = menor_dist1[1]+menor_dist2[1]
        fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]

    elif abs(fluxos.iloc[i,9]) > 0.05 and k == True:
        # Mateus Editou

        if fluxos.iloc[i,5] == 'VOB':
            menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='VCS', weight='Extensão (km)')
            menor_dist2 = nx.single_source_dijkstra(df, source='VCS', target=fluxos.iloc[i,5], weight='Extensão (km)')
            menor_distTOT = menor_dist1[0]+menor_dist2[0]
            fluxos.iloc[i,8] = menor_distTOT
            fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
            n_rot = menor_dist1[1]+menor_dist2[1]
            fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]            
        #Mateus Editou acima
        else:
            menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='EFR', weight='Extensão (km)')
            menor_dist2 = nx.single_source_dijkstra(df, source='EFR', target=fluxos.iloc[i,5], weight='Extensão (km)')
            menor_distTOT = menor_dist1[0]+menor_dist2[0]
            fluxos.iloc[i,8] = menor_distTOT
            fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
            n_rot = menor_dist1[1]+menor_dist2[1]
            fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]

    elif abs(fluxos.iloc[i,9]) > 0.05 and l == True:
        menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='FBP', weight='Extensão (km)')
        menor_dist2 = nx.single_source_dijkstra(df, source='FBP', target=fluxos.iloc[i,5], weight='Extensão (km)')
        menor_distTOT = menor_dist1[0]+menor_dist2[0]
        fluxos.iloc[i,8] = menor_distTOT
        fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
        n_rot = menor_dist1[1]+menor_dist2[1]
        fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]        

    elif abs(fluxos.iloc[i,9]) > 0.05 and m == True:
        menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='FQC', weight='Extensão (km)')
        menor_dist2 = nx.single_source_dijkstra(df, source='FQC', target=fluxos.iloc[i,5], weight='Extensão (km)')
        menor_distTOT = menor_dist1[0]+menor_dist2[0]
        fluxos.iloc[i,8] = menor_distTOT
        fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
        n_rot = menor_dist1[1]+menor_dist2[1]
        fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]

    elif abs(fluxos.iloc[i,9]) > 0.05 and n == True:
        menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='FFB', weight='Extensão (km)')
        menor_dist2 = nx.single_source_dijkstra(df, source='FFB', target=fluxos.iloc[i,5], weight='Extensão (km)')
        menor_distTOT = menor_dist1[0]+menor_dist2[0]
        fluxos.iloc[i,8] = menor_distTOT
        fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
        n_rot = menor_dist1[1]+menor_dist2[1]
        fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]
    
    # Mateus Editou #
    elif abs(fluxos.iloc[i,9]) > 0.05 and c == True: 
        menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='FRK', weight='Extensão (km)')
        menor_dist2 = nx.single_source_dijkstra(df, source='FRK', target=fluxos.iloc[i,5], weight='Extensão (km)')
        menor_distTOT = menor_dist1[0]+menor_dist2[0]
        fluxos.iloc[i,8] = menor_distTOT
        fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
        n_rot = menor_dist1[1]+menor_dist2[1]
        fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]
        
    elif abs(fluxos.iloc[i,9]) > 0.05 and o == True:
        menor_dist1 = nx.single_source_dijkstra(df, source=fluxos.iloc[i,4], target='Z51', weight='Extensão (km)')
        menor_dist2 = nx.single_source_dijkstra(df, source='Z51', target=fluxos.iloc[i,5], weight='Extensão (km)')
        menor_distTOT = menor_dist1[0]+menor_dist2[0]
        fluxos.iloc[i,8] = menor_distTOT
        fluxos.iloc[i,9] = (fluxos.iloc[i,7]/fluxos.iloc[i,8])-1
        n_rot = menor_dist1[1]+menor_dist2[1]
        fluxos.at[i,'Roteamento'] = menor_dist1[1]+menor_dist2[1]

# Definição do número de trens pra cada fluxo de transporte
"""
trem_tipo = pd.read_excel('C:\Declaração de Rede 2020\Base de Dados - Trem Tipo.xlsx')
trem_tipo.columns
fluxos.columns

fluxos['FER_MER'] = str()
trem_tipo['FER_MER'] = str()

fluxos['FER_MER'] = fluxos['Ferrovia'] + ' - ' + fluxos['Mercadoria ANTT']
trem_tipo['FER_MER'] = trem_tipo['Ferrovia'] + ' - ' + trem_tipo['Mercadorias']

fluxos = pd.merge(fluxos, trem_tipo, on='FER_MER')
fluxos.columns

fluxos['Trens'] = float(0)
fluxos['Trens'] = fluxos['TU'] / fluxos['TU - TREM']
"""
# fluxos.to_csv('C:\\Declaração de Rede 2020\\fluxos_2015.csv', sep=';', decimal =',')

"""
fluxp = [] # fluxo
origem = []  # origem do fluxo
destino = [] # destino do
distsp = [] # distância SAFF
distdp = [] # distância DIJKSTRA
rot = []
for i in range(len(fluxos['Diferença'])):
    if abs(fluxos.iloc[i,9])>0.05:
        origem.append(fluxos.iloc[i,4])
        destino.append(fluxos.iloc[i,5])
        fluxp.append(fluxos.iloc[i,4] + ' - ' + fluxos.iloc[i,5])
        distsp.append(fluxos.iloc[i,7])
        distdp.append(fluxos.iloc[i,8])
        rot.append(fluxos.iloc[i,10])
        # print(fluxos.iloc[i,3] + ' - ' + fluxos.iloc[i,4])
problemas = pd.DataFrame(list(zip(fluxp, origem, destino, distsp, distdp, rot)), 
               columns =['Fluxo', 'Origem', 'Destino', 'Dist.SAFF', 'Dist.Dijkstra', 'Roteamento']) 
problemas = problemas.drop_duplicates(subset='Fluxo')
len(problemas)
problemas.to_csv('C:\\Declaração de Rede 2020\\Fluxos_problematicosNOVO.csv', sep=';', decimal =',')
"""

# Ajuste do DataFrame da DR
data['AB'] = float()
for i in range(0, len(data['A'])):
    data.iloc[i,6] = data.iloc[i,2] + ' - ' + data.iloc[i,3]
data['TU'] = float(0)

# Ano a Ano
anos = set(fluxos['Mês/Ano'])
dict_fluxos = {}
for i in anos:
    filtro1 = fluxos['Mês/Ano'] == i
    fluxos_filt = fluxos[filtro1]

    dict_fluxos[i] = fluxos_filt


t=2015
for ano in anos:
    fluxos = dict_fluxos[ano]
    data['TU'] = float(0)
    
    ## vetorizando as variáveis
    entrepatioDR = data['AB'].values
    tuDR = data['TU'].values
    fluxostu_ = fluxos['TU'].values

    ## registra a TU que passou em cada entre pátio no dataframe da DR
    for i in range(0, len(fluxos['TU'])): # corre cada fluxo de transporte

        for k in range(0, len(fluxos.iloc[i,10])): # construção de cada entrepátio que o fluxo percorre
            j = k + 1

            try:
                estA = fluxos.iloc[i,10][k]
                estB = fluxos.iloc[i,10][j]
                entrepat = estA + ' - ' + estB
                entrepatin = estB + ' - ' + estA

                x = np.where(entrepatioDR == entrepat) # filtro do entre pátio kj

                try: # se não tiver IndexError
                    tuDR[x[0][0]] = tuDR[x[0][0]] + fluxostu_[i]

                except IndexError: # se tiver IndexError, troca o sentido dos entre pátios kj
                    x = np.where(entrepatioDR == entrepatin)
                    tuDR[x[0][0]] = tuDR[x[0][0]] + fluxostu_[i]

            except IndexError: # passa para o próximo fluxo quando chega no último entre pátio
                continue

    data['TU'] = tuDR

    print(ano)

    data.to_csv('TU_' + str(t) + '.csv', sep=';', decimal =',')
    t+=1

TU_2019 = pd.read_csv(filepath + 'TU_2019.csv', sep=';', decimal=',')
TU_2018 = pd.read_csv(filepath + 'TU_2018.csv', sep=';', decimal=',')
TU_2017 = pd.read_csv(filepath + 'TU_2017.csv', sep=';', decimal=',')
TU_2016 = pd.read_csv(filepath + 'TU_2016.csv', sep=';', decimal=',')
TU_2015 = pd.read_csv(filepath + 'TU_2015.csv', sep=';', decimal=',')

TU_15_19 = TU_2015
TU_15_19['TU_2015'] = TU_2015['TU']
TU_15_19['TU_2016'] = TU_2016['TU']
TU_15_19['TU_2017'] = TU_2017['TU']
TU_15_19['TU_2018'] = TU_2018['TU']
TU_15_19['TU_2019'] = TU_2019['TU']

del_col = ['Unnamed: 0', 'x', 'TU']
for i in del_col:
    del TU_15_19[i]

for ano in anos:
    i = 'Dist_' + str(ano)
    TU_15_19[i] = TU_15_19['Extensão (km)']


for ano in anos:
    i = 'Dist_' + str(ano)
    j = 'TU_' + str(ano)
    TU_15_19.loc[TU_15_19[j] == 0, [i]] = 0




TU_15_19.to_csv('TU_completa.csv', sep=';', decimal =',')

