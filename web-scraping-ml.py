import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configuração do User-Agent para a requisição
headers = {
    'User-Agent': "put your user agent here"
}

# Solicitar o produto ao usuário e formatar para URL
produto = input('Digite o produto: ').replace(' ', '-')
url = f'https://lista.mercadolivre.com.br/{produto}'

# Inicializar a lista para armazenar os dados
dados = []

# Definir configurações de filtro
keywords = input("Digite palavras chave separadas por virgula: ").lower().split(',')  
min_price = int(input("Digite um preço minimo: R$"))  
max_price = int(input("Digite um preço maximo: R$"))

# Loop de raspagem
start = 1
while True:
    # Montar a URL para a página atual
    url_final = f'{url}{start}_NoIndex_True'
    r = requests.get(url_final, headers=headers)
    site = BeautifulSoup(r.content, 'html.parser')

    # Extrair resultados de descrição, link e preço
    descriptions = site.find_all('h2', class_='ui-search-item__group__element')
    links = site.find_all('a', class_='ui-search-link__title-card')
    precos = site.find_all('span', class_='andes-money-amount__fraction')

    # Interromper o loop se não houver itens na página
    if not descriptions:
        print('Sem itens')
        break

    # Capturar e filtrar dados
    for descricao, preco, link in zip(descriptions, precos, links):
        produto_nome = descricao.get_text().lower()
        
        # Verificar se o produto contém alguma palavra-chave e se o preço está dentro do intervalo
        if any(keyword in produto_nome for keyword in keywords):
            try:
                preco_valor = int(preco.get_text().replace('.', ''))
                if min_price <= preco_valor <= max_price:
                    produto_info = {
                        'produto': descricao.get_text(),
                        'valor': 'R$' + preco.get_text(),
                        'link': link.get('href')
                    }
                    dados.append(produto_info)
            except ValueError:
                continue

    # Passar para a próxima página
    start += 50

# Salvar dados no Excel
df = pd.DataFrame(dados)
df.to_excel(f"{produto}.xlsx", index=False)

print(f"Dados salvos em '{produto}.xlsx'")
