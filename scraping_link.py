import requests
import json
from parsel import Selector
import pandas as pd
import datetime


def buscador_olx(regiao = 'UDI', tipo = 'apartamentos'):
    """
    Args:
        regiao (str, optional): Seleciona a regiao de busca. Defaults to 'UDI'.
        tipo (str, optional): Seleciona o tipo da busca. Defaults to 'apartamentos'.
    """    
    # Campos para criar o nome do arquivo que irá gerar os links, além de buscar a data do sistema. Por padrão a data vem em formato americano, utilizamos o strftime para passar para o nosso formato dia-mês-ano
    nome_arquivo = input('Digite o nome do arquivo : ')
    data = datetime.date.today()
    data = data.strftime('%d-%m-%Y')

    # dicionários que servirão para determinar busca por região e ou tipo de produto , povoa-los de acordo com a necessidade.
    regiao_busca = {'UDI' : 'regiao-de-uberlandia-e-uberaba/triangulo-mineiro/uberlandia'}
    prefixo_busca = {'UDI': 'estado-mg/'}
    tipo_produto = {'apartamentos': '/imoveis/venda/apartamentos/', 'casas': '/imoveis/venda/casas/', 'terrenos':'/imoveis/terrenos/','casas_condominio':'/imoveis/venda/casas/casas-de-condominio/'}
    faixa_preco = ['?pe=240000&ps=0','?pe=340000&ps=240001','?pe=440000&ps=340001','?pe=540000&ps=440001','?pe=640000&ps=540001','?pe=740000&ps=640001','?pe=840000&ps=740001','?pe=940000&ps=840001','?pe=1500000&ps=940001','?pe=2100000&ps=1500001','?ps=2100000']
    
    # parametros para o requests.get()
    PARAM = {"method":"GET",
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
    link = []

    # loop que percorre a lista faixa de preço , do index 0 a -1.
    for index in faixa_preco:
        x = 1
        # X é equivalente ao número de pagina.
        # Loop que percorre a url formatada seguindo as instruções passadas nos parametros da função, assim o scraping entra na pagina X (inicialmente a página 1), e captura o link de cada anúncio e salva em formato dicionário {'chave':'valor'} e inclui no final da lista LINK = []
        while True:
            url = "https://www.olx.com.br/"+ tipo_produto[tipo]+ prefixo_busca[regiao]+ regiao_busca[regiao] + index + "&o="+ str(x)
            
            # Capura a url e parseal ela com o Selector no formato .text. Transformar a string que existe dentro do XPATH em json. Em anúncio afunilamos as tags para chegar na tag filho final "URL"
            page = requests.get(url,headers=PARAM)
            s = Selector(text=page.text)
            html = json.loads(s.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
            anuncio = html.get('props').get('pageProps').get('ads')
           
            # Se dentro do laço encontra um lista de anuncio vazia, o laço quebra e começa novamente com outro index de faixa_preco
            if anuncio == []:
                break
            # Caso contrário, ele  ir capturar cada produto dentro da lista de anuncio e apendar na lista LINK
            try:
                for produto in anuncio:
                    link.append({'url':produto.get('url')})
                    # print(produto.get('url'))
            except:
                pass
            # print(x)
            x += 1
            if x == 101:
                break
                    
    # cria um dataframe com a lista LINK, limpa as linhas vazias existentes e limpa as duplicas. Salva em excel com o nome do arquivo escolhido e a data.   
    df = pd.DataFrame(link)
    df = df.dropna()
    df = df.drop_duplicates()
    df.to_excel(f'{nome_arquivo}-links-{data}.xlsx',index=False)
   

buscador_olx(tipo='casas')