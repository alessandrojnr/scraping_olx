
# WebScraping OLX

Projeto criado para capturar dados do olx, a princípio imóveis, e armazena-los em arquivos csv ou xlsx, além de guardar fotos em pastas nominais.

## Step-by-Step

-  **1 - pip install -r requirements.txt:**

    Antes de começar a rodar o  código, verique no txt todas as bibliotecas utilizadas no projeto. Utilizando o comando acima , fará o download de todas as bibliotecas.

- **2 - scraping_link:**

    O primeiro arquivo a ser rodado é este. Esse scripts coleta todos os links de cada anúncio. Em uma página, geralmente tem 50 anuncios e algumas propagandas. Em alguns casos elas tem o mesmo nome de class no html. Se for o caso o script irá coletar informação " ". No final do script antes de salvar, o script irá fazer uma limpeza nos dados coletados. Caso haja linhas vazias ou repetidas, as mesmas serão apagadas. Ao termino do script, e esperado retornar um csv com uma única coluna ('url'), com todos os links.

    O script está como uma função, para futuras manutenções ou modificações. Nessa versão , a função vem com parametro padrão região = 'UDI' e tipo = 'apartamento', verificar no código os conjuntos disponíveis para chamar a função desejada.

    Obs.: Na produção do script , foi verificada que o OLX continha 20k de anúncios, porém limitava em 5k de anúncios. Para raspar todos os anúncios, foi criado uma métrica de busca por range de valor e página.

- **3 - scraping_anuncio:**

    Após coletar todos os links com o script anterior, e esperado um csv. Ao abrir esse script, iremos selecionar o nome do csv que contém os links. Aqui o scraping vai percorrer todos links e fazer uma coleta de todos os itens requeridos pelo cliente e guarda-los em formato json. Ao finalizar o scraping é esperado um arquivo com linhas que serão representadas por cada anúncio, e por colunas (essas terão os nomes de cada item requerido). Foi feito um tratamento para retornar valores '' para preencher os dados vazio nas colunas de itens , e não quebrar o código.

- **4 - scraping_fotos:**

    O último passo, é coletar as fotos de cada anuncio e salva-las em um diretório. É esperado que nesse script, o script percorra a lista de links, e faça o download de todas as fotos. Irá criar uma pasta com o ID do produto e salvar as fotos como "fotos_0_{id}" e irá incrementar +1 para cada foto salvá.
    
