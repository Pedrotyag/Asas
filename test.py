import requests, time
from letmecrawl import letmecrawl

    
if __name__ == '__main__':
    try:
        proxies = open('proxies.txt', 'x')
        proxies.close()
    except:
        pass
    
    for proxy in letmecrawl():
        
        with open('proxies.txt', 'a') as proxies:
            proxies.write('{0}\n'.format(str(proxy)))
        print("O proxy '{0}' foi escrito".format(str(proxy)))
    