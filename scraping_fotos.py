import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from time import sleep

# Ler o excel que contem os links e os codigos para gerar as pastas FOTOS com o nome CÓDIGO.
df = pd.read_excel('casas_condominio-27-10-2023.xlsx')
links = df['Link'].tolist()
cod = df['Código'].copy()
dados_finais = []


for x in range(0, len(links)):
    try: 
        url = links[x]
        param = {"method":"GET",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
                }
        
        page = requests.get(url = url, headers = param)
        dados = BeautifulSoup(page.text,"html.parser")
        link_foto = dados.find_all('meta', attrs= {'property':'og:image'})
        diretorio = Path.home()/'Desktop'/f'{int(cod[x])}'
        diretorio.mkdir()

        for indice, link in enumerate(link_foto):
            foto = ((link).get('content'))
            download_foto = requests.get(str(foto))
            with open(f'{diretorio}/{int(cod[x])}foto{indice}.jpg','wb') as f:
                f.write(download_foto.content)
    except:
        pass