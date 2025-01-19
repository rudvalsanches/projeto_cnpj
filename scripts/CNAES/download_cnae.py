import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from zipfile import ZipFile

BASE_URL = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj"

def get_current_folder():
    now = datetime.now()
    return f"{now.year}-{now.strftime('%m')}"

def download_file(file_url, save_path):
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Arquivo salvo em: {save_path}")
    else:
        print(f"Erro ao baixar o arquivo: {response.status_code}")

def extract_and_rename(file_path, extract_to):
    with ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Arquivo extraído em: {extract_to}")

    # Identifica o arquivo com extensão incomum
    for root, _, files in os.walk(extract_to):
        for file in files:
            if "CNAE" in file.upper():  # Verifica se o arquivo tem "CNAE" no nome
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(extract_to, "arquivo.csv")
                os.rename(old_file_path, new_file_path)
                print(f"Arquivo renomeado para: {new_file_path}")
                return new_file_path

    print("Nenhum arquivo CNAE encontrado para renomear.")
    return None

def main():
    folder = get_current_folder()
    folder_url = f"{BASE_URL}/{folder}/"
    response = requests.get(folder_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a') if a['href'].endswith('.zip')]

    if not links:
        print("Nenhum arquivo encontrado!")
        return

    os.makedirs("../dados/CNAES", exist_ok=True)
    for link in links[:1]:  # Baixa apenas o primeiro arquivo como exemplo
        file_url = f"{folder_url}{link}"
        zip_path = f"../dados/CNAES/{link}"
        download_file(file_url, zip_path)

        # Extrair o arquivo ZIP e renomear
        extracted_file = extract_and_rename(zip_path, "../dados/CNAES")
        if extracted_file:
            print(f"Pronto para importar: {extracted_file}")
        else:
            print("Erro: Nenhum arquivo CSV adequado encontrado.")

if __name__ == "__main__":
    main()
