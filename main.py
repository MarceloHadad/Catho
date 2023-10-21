import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Ler o arquivo Excel
df = pd.read_excel('Catho.xlsx')

# Função para obter o número de vagas
def obter_numero_vagas(url):
    try:
        headers = {'User-Agent': '*'}
        response = requests.request("GET", url, headers=headers)
                
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_title = soup.select("#jobTitle")[0].text
            job_title = job_title.replace(".", "")
            numero_vagas = job_title.split(' ')[0]
            return numero_vagas
        else:
            return None
    except Exception as e:
        print(f"Erro ao acessar a URL {url}: {str(e)}")
        return None

# Iterar sobre as linhas do DataFrame
for index, row in df.iterrows():
    busca = row['Busca']  # Ler o valor da coluna "Busca"

    # Formatar a busca como uma URL válida
    busca_url = quote(busca)
    
    # Construir a URL concatenando a busca com a URL base
    url = f'https://www.catho.com.br/vagas/{busca_url}/?faixa_sal_id=7&faixa_sal_id_combinar=1'
    
    # Usar a URL na função para obter o número de vagas
    numero_vagas = obter_numero_vagas(url)
    
    # Gravar a URL na coluna "URL" do Excel
    df.at[index, 'URL'] = url

    # Gravar o número de vagas na coluna "Vagas encontradas"
    df.at[index, 'Vagas encontradas'] = numero_vagas

# Salvar o DataFrame de volta no arquivo Excel original (substituir os dados existentes)
df.to_excel('Catho.xlsx', index=False)
