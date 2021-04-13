import Codigo_otimizador_copy as ot 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import Polar_de_arrasto as polar

env = (3, 4.2)
chord = (0.3, 0.5)
offset = (0.01, 0.05)

geometria = [env, chord, offset]

asas_populacao_inicial = ot.criar_asas(geometria, limite_populacional = 3)

#for asa in asas_populacao_inicial:
    #asa.analisador()
    
ot.analisador(asas_populacao_inicial)

#asas_populacao_inicial = sorted(asas_populacao_inicial, key = lambda x: x.pontuacao, reverse=True)

#asas_finais = ot.combinador(asas_populacao_inicial)
asas_finais = ot.genetico(asas_populacao_inicial)

asas_finais = sorted(asas_finais, key = lambda x: x.pontuacao, reverse=True)

ot.criar_df(asas_finais)

df_asas.to_excel("testesdeplot.xlsx")


'''
#Criação do DataFrame
try:
    arquivo = pd.read_excel("output.xlsx")
    asa = pd.DataFrame(arquivo)
    asa = asa.drop(columns=['Unnamed: 0'])
        
except:    
    asa = pd.DataFrame()
'''
      
polar.polar(df_asas, index = list(df_asas.index), tipo = 5)