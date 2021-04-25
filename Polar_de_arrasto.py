import pandas as pd 
import matplotlib.pyplot as plt

   
def polar(dataframe, index = [0], tipo = 5, scatter = False):
    
    '''
    Vizualização de polares de acordo com o DataFrame dado, uma lista de asas na qual
    queira vizualizar e o tipo da polar de acordo com a documentação
    
    dataframe: Um dataframe contendo as asas e o resultado das análises
    
    index: uma lista contendo o index das asas na quais queira vizualizar
    
    tipo: qual a polar você quer vizualizar
    
    Tipos
    1 - cl x cd
    2 - cd x cl
    3 - cl/cd x alfa
    4 - cd/cl x alfa
    5 - cd x alfa
    6 - cl x alfa
    '''
    
    
    plt.style.use('classic')
    plt.rcParams['figure.figsize'] = (11,7)
    
    for i in index:
        
        asa_escolhida = dataframe.loc[i]

        CD_lista = asa_escolhida["CD"]
        CL_lista = asa_escolhida["CL"]
        ALFA_lista = asa_escolhida["ALFA"]
        
        #CD_lista = [0.0008, 0.0007, 0.0011, 0.002, 0.0034, 0.0052, 0.0075, 0.0103, 0.0136, 0.0173, 0.0215, 0.0262, 0.0313, 0.0368, 0.0428, 0.0492, 0.056, 0.0632, 0.0707, 0.0786, 0.0869, 0.0955, 0.1044, 0.1135, 0.1229, 0.1326, 0.1424, 0.1524, 0.1626, 0.1729, 0.1834, 0.1939, 0.2044, 0.215, 0.2256]
        #CL_lista = [0.1007, 0.0249, 0.0509, 0.1269, 0.2029, 0.2788, 0.3547, 0.4305, 0.5061, 0.5815, 0.6566, 0.7314, 0.8059, 0.8799, 0.9535, 1.0266, 1.0991, 1.1711, 1.2424, 1.3131, 1.383, 1.4522, 1.5206, 1.5882, 1.6549, 1.7207, 1.7856, 1.8495, 1.9124, 1.9743, 2.0351, 2.0949, 2.1535, 2.211, 2.2674]
        #ALFA_lista = [-15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        CDxCL_lista = []
        CLxCD_lista = []
        for cd, cl in zip(CD_lista, CL_lista):
                CDxCL_lista.append(cd/cl)
                CLxCD_lista.append(cl/cd)
                
        if(tipo == 1):

                plt.plot(CD_lista, CL_lista)
                if(scatter):
                        plt.scatter(CD_lista, CL_lista)
                        
                plt.title('CL x CD')

                plt.xlabel('CD')
                plt.ylabel('CL')
                
        elif(tipo == 2):
                plt.plot(CL_lista, CD_lista)
                if(scatter):
                        plt.scatter(ALFA_lista, CLxCD_lista)
                        
                plt.title('CD x CL')

                plt.xlabel('CL')
                plt.ylabel('CD')

        elif(tipo == 3):
                plt.plot(ALFA_lista, CLxCD_lista)
                if(scatter):
                        plt.scatter(ALFA_lista, CLxCD_lista)
                        
                plt.title('CL/CD x ALFA')

                plt.xlabel('CL/CD')
                plt.ylabel('ALFA')

        elif(tipo == 4):
                plt.plot(ALFA_lista, CDxCL_lista)
                if(scatter):
                        plt.scatter(ALFA_lista, CDxCL_lista)
                        
                plt.title('CD/CL x ALFA')

                plt.xlabel('ALFA')
                plt.ylabel('CD/CL')

        elif(tipo == 5):
                plt.plot(ALFA_lista, CD_lista)
                if(scatter):
                        plt.scatter(ALFA_lista, CD_lista)
                        
                plt.title('CD x ALFA')

                plt.xlabel('ALFA')
                plt.ylabel('CD')

        elif(tipo == 6):
                plt.plot(ALFA_lista, CL_lista)
                if(scatter):
                        plt.scatter(ALFA_lista, CL_lista)

                plt.title('CL x ALFA')

                plt.xlabel('ALFA')
                plt.ylabel('CL')
        

    plt.grid()
    plt.show()    
    
        
#polar(dataframe = 0, index = [0], tipo = 1, scatter = True)