#@pedro

def metodo_por_MTOW(MTOW , PORCENTAGEM = 15):
    '''
    Geralmente a massa da asa é 30 porcento da carga vazia
    Geralmente a massa da asa é 9 porcento do MTOW (NEWTON POR NEWTON)
    '''
    G = 9.81 #m/s^2
    
    m = MTOW * (PORCENTAGEM / 100)
    return m


def metodo_por_constante(AREA_OBJETIVO, PESO = 0, AREA = 0, CONSTANTE = 20.3605):
    '''
    Geralmente a constante PESO DA ASA / AREA DA ASA É 15,8
    '''
    G = 9.81 #m/s^2
        
    if CONSTANTE != 0:

        PESO_OBJETIVO = CONSTANTE * AREA_OBJETIVO

        m = PESO_OBJETIVO / G
    
    else:
        
        CONSTANTE = PESO / AREA

        PESO_OBJETIVO = CONSTANTE * AREA_OBJETIVO

        m = PESO_OBJETIVO / G


    return m

