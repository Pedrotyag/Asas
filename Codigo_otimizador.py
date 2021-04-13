# To do
# - Criar função que sort a lista com objetos asa em função de pontuação. Ou de outro parâmetro.
# - Ajeitar a função visualizador. Ela só ta mostrando a última geração.
# - Gerar mais de 1 filho
# - Ta mostrando só o msm indivíduo no final

from Estimação_de_massa import metodo_por_MTOW
import random as rd
'from random import uniform as random
'import os
import time
import textwrap
import math, statistics
from operator import itemgetter
from numpy import log as ln
import matplotlib.pyplot 
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import re
from subprocess import Popen, PIPE, DEVNULL


class asa():
    def __init__(self, B, cordas, offsets, alfa_stol = 13.5):

        self.envs = B
        self.B = (B[-1]*2)
        self.offsets = offsets
        self.cordas = cordas

        total = 0
        for i in range(0,len(B)):
            if (i == 0):
                total += ((cordas[i] + cordas[i+1])*B[i])/2
            else:
                total+= ((cordas[i] + cordas[i+1])*(B[i]-B[i-1]))/2

        self.S = (total*2)
        self.AR = self.B**2/self.S
        self.afil = cordas[-1]/cordas[0]
        self.mac = ( cordas[0]*(2/3)* ((1+self.afil+self.afil**2)/(1+self.afil)))
        self.alfa_stol = alfa_stol

        # Valores que não são da aeronave
        self.g = 9.81
        self.rho = 1.225
        self.mi = 0.025
        self.pista_total = 60

    def file_and_commands(self, alfa_stol = 13.5): # Não mexer nisso~

        o  = open("asa.avl", "w")
        o.write(" Urutau 2020 (2)\n" +
        "0.0                                 | Mach\n" +
        "0     0     0.0                     | iYsym  iZsym  Zsym\n"+
        "%f     %f     %f   | Sref   Cref   Bref\n" %(self.S, self.mac, self.B)+
        "0.00000     0.00000     0.00000   | Xref   Yref   Zref\n"+
        "0.00                               | CDp  (optional)\n"+
        "SURFACE                      | (keyword)\n"+
        "Main Wing\n"+
        "11        1.0\n"+
        "INDEX                        | (keyword)\n"+
        "1814                         | Lsurf\n"+
        "YDUPLICATE\n"+
        "0.0\n"+
        "SCALE\n"+
        "1.0  1.0  1.0\n"+
        "TRANSLATE\n"+
        "0.0  0.0  0.0\n"+
        "ANGLE\n"+
        "0.000                         | dAinc\n"+
        "SECTION                                              |  (keyword)\n"+
        "0.0000    0.0000    0.0000    %f   0.000    8    3   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %(self.cordas[0])+
        "AFIL 0.0 1.0\n"+
        "airfoil.dat\n"+
        "SECTION                                                     |  (keyword)\n" +
        "%f    %f    0.0000    %f   0.000    8    3   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %( self.offsets[0],  self.envs[0], self.cordas[1])+
        "AFIL 0.0 1.0\n"+
        "airfoil.dat\n"+
        "SECTION                                                     |  (keyword)\n" +
        "%f   %f    0.0000    %f   0.000   13    1   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %( self.offsets[1],  self.envs[1], self.cordas[2])+
        "AFIL 0.0 1.0\n"+
        "airfoil.dat \n" +
        "SECTION                                                     |  (keyword)\n" +
        "%f    %f    0.0000    %f   0.000   13    1   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %( self.offsets[2],  self.envs[2], self.cordas[3])+
        "AFIL 0.0 1.0\n" +
        "airfoil.dat \n")
        o.close()

        commands  = open("comandos.avl" , "w")
        commands.write("load asa.avl\n"   +
        "oper\n" +
        "a\n" +
        "a %f\n" %(alfa_stol) +
        "x\n" +
        "ft\n" +
        "resultado.txt\n" +
        "quit")
        commands.close()
        

    def coeficientes(self, angulo):

        self.file_and_commands(angulo)

        run_avl_command = 'avl.exe<' + 'comandos.avl'
        os.popen(run_avl_command).read()
    

        results = (open("resultado.txt")).readlines()
        coefficients = []
        for line in results:
            matches = re.findall(r"\d\.\d\d\d\d", line)
            for value in matches:
                coefficients.append(float(value))
        

        CD = coefficients[-7]
        CL = coefficients[-8]    
        e =  coefficients[-1]     

        self.CD = CD
        self.CL = CL
        self.e = e
        
        
        # Limpar
        dirList = os.listdir()
        arquivo = ""
        for file in dirList:
            if (file == "asa.avl") or (file == "resultado.txt") or  (file == "comandos.txt"):
                arquivo = file
                os.remove(arquivo)
        
        #return (CD_CL)
    
    def lift (self, V, rho = 1.225 ):
        return (self.rho*V**(2)*0.5*self.CL*self.S)
    
    def drag (self, V, rho = 1.225 ):
        return (self.rho*V**(2)*0.5*self.CD*self.S)

    def mtow (self, rho = 1.225, T=38.125):
        for k in range (0, 270):
            W= (k/(9)) * self.g
            V = math.sqrt((2*W)/(self.rho*self.S*self.CL)) * 1.2 * 0.7
            D = self.rho*V**(2)*0.5*self.CD*self.S
            L = self.rho*V**(2)*0.5*self.CL*self.S
            Slo = round((1.44*(W)**(2))/(self.g*self.rho*self.S*self.CL*(T-(D+self.mi*(W-L)))), 2)
            if Slo > self.pista_total:
                break    

        self.W = W
        return W
    
    def calc_massa(self):
        
        fator_corretivo = 1.09
        W = ((self.W/self.g)/fator_corretivo)
        
        massa_vazia = (11.48*((self.S)**2)) - 26.55*(self.S) + 19.44
        massa_asa = metodo_por_MTOW(W)
        massa_resto = massa_vazia - massa_asa 
        
        return (W, massa_vazia, massa_asa, massa_resto)
        
    def calc_pontuacao (self):
        
        self.MTOW = self.calc_massa()[0] # Esse é o MTOW corrigido e em Kg
        self.carga_paga = (self.MTOW - self.calc_massa()[1]) # Empirical
        self.pontuacao = 8.3 * 2.7182818 ** (self.carga_paga/6)

                
    def analisador(self, DataFrame):
        
        # Calculos para situação de stol
        self.coeficientes(self.alfa_stol)
        self.mtow()
        self.calc_pontuacao()

        # Calculos para a polar
        self.CD_lista = []
        self.CL_lista = []
        self.e_lista = []
        self.alfa_lista = []

        for i in range(-15, 20, 1):
            self.coeficientes(i)
            self.CD_lista.append(self.CD)
            self.CL_lista.append(self.CL)
            self.e_lista.append(self.e)
            self.alfa_lista.append(i)
        
        data = [[self.S, self.B, self.AR,  self.afil, self.MTOW, self.carga_paga,
                      self.pontuacao, self.alfa_lista, self.CD_lista, self.CL_lista]]
        
        asa = pd.DataFrame(data, columns=['AREA','ENVERGADURA', 'AR' , 'AFILAMENTO', 'MTOW', 'CARGA PAGA', 
                                          'PONTUAÇÃO', 'ALFA', 'CD', 'CL'], index = [DataFrame.shape[0] + 1 ])
        
        DataFrame = DataFrame.append(asa)
        
        return DataFrame
    
        #exit()
        

# def mutation():

def crossover(l, q): 
    l,q = int(str(l)[2:8]), int(str(q)[2:8]) # Corta a parte decimal

    # Ve se tem menos de 6 digitos e ajeita
    while (len(str(l))< 6):
        l = l*10
    while (len(str(q))< 6):
        q = q*10

    l,q = bin(l)[2:], bin(q)[2:] # Corta o "0b"
    #l,q = str(l).zfill(22), str(q).zfill(22) # Deixa no mesmo tamanho

    l = list(l) 
    q = list(q) 

    ponto_corte = rd.randint(5, 17) 
    # Combinando a partir do ponto de corte
    l[ponto_corte:], q[ponto_corte:] = q[ponto_corte:], l[ponto_corte:] 

    # Volta pra string
    filho_1 = ''.join(l) 
    filho_2 = ''.join(q) 

    filho_1 = int(filho_1, 2)/1000000
    filho_2 = int(filho_2, 2)/1000000

    return filho_1

def criar_asas ():
    # Wingspans
    env_1 = random(0.33,0.52)
    env_2 = random(0.33,0.52) + env_1
    env_3 = random(0.33,0.52) + env_2
    envs = [env_1, env_2, env_3]

    # Chords
    chord_1 = random(0.3, 0.4)
    chord_2 = random(chord_1-0.05, chord_1)
    chord_3 = random(chord_2 - 0.05, chord_2)
    chord_4 = random(chord_3 - 0.05, chord_3)
    cordas = [chord_1, chord_2, chord_3, chord_4]

    # Offsets 
    offset_1 = random(0.01, 0.03)
    offset_2 = random(0.01, 0.03) + offset_1
    offset_3 = random(0.01, 0.03) + offset_2
    offsets = [offset_1, offset_2, offset_3]

    Asa = asa(envs,cordas, offsets)

    return Asa

def combinador(asa1, asa2):
    cordas = []
    for i in range (0,len(asa1.cordas)):
        corda = crossover(asa1.cordas[i],asa2.cordas[i])
        cordas.append(corda)
    cordas = sorted(cordas)

    # # Reduzir pro limite de 0,37
    # if (cordas[0] > 0.37):
    #     while (cordas[0] > 0.37):
    #         cordas[0] = cordas[0]*0.991
    #         cordas = sorted(cordas)

    # # Ajeitar o afilamento
    # if (cordas[-1]/cordas[0] >= 0.4):
    #     while (cordas[-1]/cordas[0] >= 0.4):
    #         cordas[-1] = cordas[-1]*0.991
    # else:
    #     while (cordas[-1]/cordas[0] < 0.3):
    #         cordas[-1] = cordas[-1]*1.05
    # cordas = sorted(cordas)   

    # Envergaduras
    envs = []
    for i in range (0, len(asa1.envs)):
        if (i == 0):
            env = crossover(asa1.envs[i],asa2.envs[i])
        else:
            env = crossover(asa1.envs[i] - asa1.envs[i-1], asa2.envs[i] - asa2.envs[i-1])
        envs.append(env)
    
    for i in range(0, len(envs)):
        if (i != 0):
            envs[i] = envs[i] + envs[i-1]

    # Add esse limite de envergadura
    # if (env[-1]>= limite_envergadura):

    # Offset calculations: Botar só uma mutação
    offsets = asa1.offsets

    filho = asa(envs, cordas, offsets)

    return filho

def visualizador (lista):
    pontuacoes = []
    geracoes = [*range(1, len(lista) +1)]
    size = []

    # Ele vai adicionando sempre a melhor pontuação. Só adiciona se for melhor que a geração anterior
    for i in range (0, len(lista)):
        size.append(lista[i].B)
        if (i==0):
            pontuacoes.append(lista[i].pontuacao)
        else:
            if (lista[i].pontuacao > lista[i-1].pontuacao):
                pontuacoes.append(lista[i].pontuacao)

            else:
                pontuacoes.append(lista[i-1].pontuacao)

    # Criar o gráfico
    plt.style.use('seaborn')
    plt.scatter(geracoes,pontuacoes, s=60, c = size, cmap = 'Greens', edgecolor= "black", linewidth = 1, alpha = 1)
    cbar = plt.colorbar()
    cbar.set_label ('Envergadura')
    plt.title ("Asas")
    plt.xlabel("Geração")
    plt.ylabel("Pontuação")
    plt.tight_layout()
    plt.show()

def main():
    #limite_populacional = int(input("Quantas gerações: "))
    limite_populacional = 5
    populacao = []
    melhores = []
    
    #Criação do DataFrame
    try:
        arquivo = pd.read_excel("output.xlsx")
        asa = pd.DataFrame(arquivo)
        asa = asa.drop(columns=['Unnamed: 0'])
        
    except:    
        asa = pd.DataFrame()
    
    # Criacao da populacao inicial
    for i in range (0,limite_populacional):
        Asa = criar_asas()
        Asa.analisador(asa)
        populacao.append(Asa)                                                                                   

    populacao = sorted(populacao, key = lambda x: x.pontuacao, reverse=True)

    # Combinações
    ciclos = (int(round(limite_populacional/2)))
    tamanho = len(populacao) - 1

    for i in range (0, limite_populacional): # Combina todos os indivíduos n=limite_populacional vezes
        for j in range (0, ciclos):
            filho1 = combinador(populacao[i], populacao[tamanho-i])
            #filho2 = combinador(populacao[tamanho-i], populacao[i])

            asa = filho1.analisador(asa)
            #asa = filho2.analisador(asa)
            
            populacao.append(filho1)
            #populacao.append(filho2)

        populacao = sorted(populacao, key=lambda x: x.pontuacao, reverse=True)
        
        #Criando arquivo .xlsx
        asa.to_excel("output.xlsx") 
        
        # Deletar os extras acima do limite populacional
        if len(populacao) > limite_populacional:
            for i in range (limite_populacional, len(populacao)-1):
                del populacao[limite_populacional]

        
        melhores.append(populacao[0])
    # Ta errado isso. Ele só plota a última geração.

    # visualizador (melhores)

#main()






