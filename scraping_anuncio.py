import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import datetime

# Campos para criar o nome do arquivo que irá gerar os links, além de buscar a data do sistema. Por padrão a data vem em formato americano, utilizamos o strftime para passar para o nosso formato dia-mês-ano
nome_salvar_arquivo = input('Escolha o nome do arquivo em xlsx para salvar o novo arquivo: ')
data = datetime.date.today()
data = data.strftime('%d-%m-%Y')

# Ler o excel que contem os links "alterar o nome para o arquivo desejado", passar o df para uma LISTA, Criando uma lista para apendar os dicionários gerados pelo scrapping.
df = pd.read_excel('casas_condominio-links-27-10-2023.xlsx')
links = df['url'].tolist()
dados_finais = []
x = 0
#loop para percorrer a lista LINKS geradas no passo anterior
for link in links:
    url = link   
    param = {"method":"GET",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
                }

    # Parseando o html com o bs4, findando o "script" e pegando o texto e transformando ele em string, formatando o json gerado. 
    page = requests.get(url = url, headers = param)
    dados = BeautifulSoup(page.text,"html.parser")
    json_dados = str(dados.find("script").getText)
    json_dados = json_dados.replace('<bound method PageElement.get_text of <script>window.dataLayer = ','').replace('</script>>','')

    
    # Será feito uma tentativa para encontrar os dados, caso os dados não sendo encontrados será retornado como atribuir "".

    try:
        json_dados = json.loads(str(json_dados).strip('[]'))
        dados_complementares = json_dados.get('page').get('adDetail')
    except:
        pass


    try:
        descricao = dados.find("h1", class_="ad__sc-45jt43-0 htAiPK sc-VigVT ZEEcn").text
    except:
        descricao = ''

    try:
        data_publi = dados.find("span",class_="ad__sc-1oq8jzc-0 dWayMW sc-VigVT dHNWJq").text.split('em')[1]
    except:
        data_publi = ''
    try:
        cod = dados.find("span", class_="ad__sc-16iz3i7-0 hjLLUR sc-VigVT dHNWJq").text.split('.')[1].strip()
    except:
        cod = ''
    try:
        preco = dados.find_all("h2",class_= "ad__sc-12l420o-1 dnbBJL sc-VigVT gVrrBf")[1].text
    except:
        preco = ''
    try:
        end = dados.find("div",class_="ad__sc-10rz2dk-2 fxAfax").text.split('CEP:')[0]
    except:
        end = ''
    try:
        cep = dados.find("div",class_="ad__sc-10rz2dk-2 fxAfax").text.split('CEP:')[1]
    except:
        cep = ''
    try:    
        area_util = dados_complementares.get('size')
    except:
        area_util = ''
    try:
        quartos = dados_complementares.get('rooms')
    except:
        quartos = ''
    try:
        banheiros = dados_complementares.get('bathrooms')
    except:
        banheiros = ''
    try:    
        vagas = dados_complementares.get('garage_spaces')
    except:
        vagas = ''
    try:
        iptu = dados.find_all('span', class_= 'ad__sc-2iplj6-3 xIkHt sc-VigVT rycv')[0].text
    except:
        iptu = ''
    try:
        condominio = dados.find_all('span', class_= 'ad__sc-2iplj6-3 xIkHt sc-VigVT rycv')[1].text
    except:
        condominio = ''



    json_final = {'Data publicação':data_publi,
                    'Descrição':descricao,
                    'Código':cod,
                    'Preço':preco,
                    'Endereço':end,
                    'Cep':cep,
                    'Área Útil':area_util,
                    'Quartos':quartos,
                    'Vagas': vagas,
                    'Banheiros': banheiros,
                    'IPTU': iptu,
                    'Condomínio': condominio,
                    'Link': link,
                                    
        

                # 'Imagens': imagens
        }
    dados_finais.append(json_final)
    print(x)
    x+=1

df = pd.DataFrame(columns=['Descrição','Data publicação','Código','Preço','Área Útil','Endereço','Cep','Quartos','Vagas','Banheiros','IPTU','Condomínio','Link'])
df_dados = pd.concat([df,pd.DataFrame(dados_finais)],ignore_index=False)

#df_dados.to_csv(f'{nome_salvar_arquivo}.csv',index=False)
df_dados.to_excel(f'{nome_salvar_arquivo}-{data}.xlsx', index=False)

