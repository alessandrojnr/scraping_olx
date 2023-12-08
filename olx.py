import json
import pandas as pd
import requests
import lxml.html
from lxml.html import etree
from lxml.html import tostring
from datetime import datetime, timezone, timedelta


class Olx:
    def __init__(self):
        self.regiao = '/regiao-de-uberlandia-e-uberaba/triangulo-mineiro/uberlandia'
        self.prefixo = 'estado-mg'
        self.tipo = {
            'apartamentos': 'imoveis/venda/apartamentos/', 
            'casas': 'imoveis/venda/casas/', 
            'terrenos':'imoveis/terrenos/',
            'casas_condominio':'imoveis/venda/casas/casas-de-condominio/'
        }

        self.precos = [ 
            '?pe=240000&ps=0',
            '?pe=340000&ps=240001',
            '?pe=440000&ps=340001',
            '?pe=540000&ps=440001',
            '?pe=640000&ps=540001',
            '?pe=740000&ps=640001',
            '?pe=840000&ps=740001',
            '?pe=940000&ps=840001',
            '?pe=1500000&ps=940001',
            '?pe=2100000&ps=1500001',
            '?ps=2100001']
    
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}

        self.url_anuncios = []
        self.json_data_list = []

    def scrap_anuncios(self,type):
        x = 1
        for preco in self.precos:
            for i in range(1,101):
                url = "https://www.olx.com.br/"+self.tipo[type]+self.prefixo+self.regiao + preco + "&o="+ str(i)
                #print(url)
                r = requests.get(url, headers= self.headers)

                if 'Ops! Nenhum anúncio foi encontrado.' in r.text:
                    break
                else:
                    html= lxml.html.fromstring(r.text)
                    data = html.xpath('//script[@id="__NEXT_DATA__"]/text()')
                    json_data = json.loads(data[0])
                    anuncios = json_data.get('props').get('pageProps').get('ads')
                    try:
                        for anuncio in anuncios:
                            url_anuncio = anuncio.get('url')
                            if url_anuncio and url_anuncio not in self.url_anuncios:
                                self.url_anuncios.append(url_anuncio)
                                self.scrap_dados_anuncios(url_anuncio)
                                print(url_anuncio)
                                print(x)   
                                x += 1      
                    except Exception as e:
                        print(e)
                       


    def scrap_dados_anuncios(self, url):
        r = requests.get(url, headers= self.headers)
        print(r.status_code)
        if r.status_code == 200:
            html = lxml.html.fromstring(r.text)
            meta = self.scrap_meta_script(html)
            initial = self.scrap_initial_script(html)
            taxa_condominio = ''
            iptu = ''
            print(taxa_condominio, iptu)
            if 'properties' in initial['ad']:
                for property in initial['ad']['properties']:
                    if 'name' in property:
                        if property['name'] == 'condominio':
                            taxa_condominio = property['value']

                        if property['name'] == 'iptu':
                            iptu = property['value']

            try:
                data = {
                    'id_ambiente': meta[0]['page']['detail']['list_id'],
                    'tipo_imovel': meta[0]['page']['adDetail']['subCategory'],
                    'titulo': meta[0]['page']['adDetail']['subject'],
                    'rua' : initial['ad']['location']['address'],
                    'bairro': initial['ad']['location']['neighbourhood'],
                    'cidade': initial['ad']['location']['municipality'],
                    'estado': initial['ad']['location']['uf'],
                    'cep': initial['ad']['location']['zipcode'],
                    'preco': meta[0]['page']['adDetail']['price'],
                    'area_privativa': meta[0]['page']['adDetail']['size'],
                    'quartos': meta[0]['page']['adDetail']['rooms'],
                    'banheiros': meta[0]['page']['adDetail']['bathrooms'],
                    'garagens': meta[0]['page']['adDetail']['garage_spaces'],
                    'iptu': iptu,
                    'taxa_condominio': taxa_condominio,
                    'caracteristicas_imovel': meta[0]['page']['adDetail']['re_features'] if 're_features' in meta[0]['page']['adDetail'] else '',
                    'caracteristicas_condominio': meta[0]['page']['adDetail']['re_complex_features'] if 're_complex_features' in meta[0]['page']['adDetail'] else '',
                    'descricao': initial['ad']['body'],
                    'data_anuncio': self.formatar_data(initial['ad']['listTime']),
                    'anunciante': meta[0]['page']['adDetail']['sellerName'],
                    'professional': initial['ad']['professionalAd'],
                    'url': url,
                }
            except:
                pass

            self.data_json(data)
            #
            print(data)          
        return None

    def formatar_data(self, data_str, formato="%d/%m/%Y %H:%M", fuso_horario=timezone(timedelta(hours=-3))):
        # Converter a string para um objeto datetime
        data_objeto = datetime.fromisoformat(data_str[:-1]).replace(tzinfo=timezone.utc)
        # Adicionar o deslocamento de tempo para o fuso horário especificado
        data_formatada = data_objeto.astimezone(fuso_horario).strftime(formato)
        
        return data_formatada
    
    def scrap_meta_script(self, html):
        heads = html.xpath('/html/head')[0]
        for head in heads:
            script_data = etree.tostring(head, encoding='unicode', method='html', pretty_print=True)
            script = script_data.split('>')[1].split('<')[0]
            if 'window.dataLayer' in script:
                data = script.replace('window.dataLayer = ', '')
                data = data.split('}})')[0]
                if 'pageType' in data:
                    return json.loads(data)                   
        return None

    def scrap_initial_script(self, html):
        scripts = html.xpath('//*[@id="initial-data"]')
        script_data = etree.tostring(scripts[0], encoding='unicode', method='html', pretty_print=True)
        script_data = script_data.split("data-json='")[1].split("'></script>")[0]
        return json.loads(script_data)
    
    def data_json(self,data):
        self.json_data_list.append(data)

    def get_json_data(self):
        return json.dumps(self.json_data_list)

    def save_to_excel(self, file_path = 'output.xlsx'):
        df = pd.DataFrame(self.json_data_list)
        df.to_excel(file_path, index = False)
        df2 = pd.DataFrame(self.url_anuncios)
        df2.to_excel('teste.xlsx')



olx = Olx()
olx.scrap_anuncios('casas_condominio')
olx.save_to_excel('output.xlsx')