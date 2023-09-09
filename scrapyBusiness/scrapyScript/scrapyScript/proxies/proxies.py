import requests
from bs4 import BeautifulSoup as bs

#Definir funcion
def get_proxies():
    res = requests.get('https://free-proxy-list.net/')
    content = bs(res.text, 'lxml')
    table = content.find('table')
    rows = table.find_all('tr')
    cols = [[col.text for col in row.find_all('td')] for row in rows]

    proxies = set()

    for col in cols:
        try:
            if col[4]=='elite proxy' and col[6]=='yes':
                proxy = ('https://' + col[0] + ':' + col[1])
                proxies.add(proxy)
        except:
            pass
    print(proxies)
    return proxies