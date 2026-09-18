import asyncio
import httpx
from bs4 import BeautifulSoup
import json
import pdfplumber

base_url = 'https://arth-inacio.github.io/scod_scraping_challenge/'
caminho_data = '/home/jonathan/Área de trabalho/Desafio-scod/data/dados.json' 
boletos = '/home/jonathan/Área de trabalho/Desafio-scod/boletos'

async def buscar_page(client: httpx.AsyncClient, url: str) -> str | None:
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text
    except httpx.HTTPError as e:
        print(f"Erro ao acessar {url}: {e}")
        return None





async def main():   
    async with httpx.AsyncClient() as client:
        page = await buscar_page(client, base_url)
        if page:
            html = BeautifulSoup(page,'html.parser') #parser do html 
            tabela = html.find("table",{"id": "debitos-table"}) #procura a tabela 
            linhas = tabela.find_all("tr", class_="debito-row") #procura apenas as incidencias de dados da tabela
            debitos = []
            for linha in linhas:
                tds = linha.find_all("td")
                debito = {
                            "codigo_lancamento": linha["data-cod_lancamento"],  
                            "descricao":tds[0].get_text(strip=True),            
                            "exercicio":tds[1].get_text(strip=True),               
                            "parcela":tds[2].get_text(strip=True),                     
                            "vencimento":tds[3].get_text(strip=True),                               
                            "status":tds[5].get_text(strip=True),
                            "boleto_url":tds[6].find("a")["href"]                
                        }
                try:
                    url_pdf = base_url + debito["boleto_url"]
                    resposta = await client.get(url_pdf)
                    resposta.raise_for_status()
                    caminho_pdf = f"/home/jonathan/Área de trabalho/Desafio-scod/boletos/{debito['codigo_lancamento'] }.pdf"
                    with open(caminho_pdf,"wb") as boleto:
                        boleto.write(resposta.content)
                
                    with pdfplumber.open(caminho_pdf) as pdf:
                        pagina = pdf.pages[0]
                        texto = pagina.extract_text()
                        linhas_texto = texto.splitlines()
                        posicao = linhas_texto.index("Linha Digitável:")
                        digitavel = linhas_texto[posicao + 1]
                        for item in linhas_texto:
                            if item.startswith("Valor:"):
                                valor_pdf = item.split(": R$ ")[1].strip()       
                    debito["valor"] = valor_pdf
                    debito["linha_digitavel"] = digitavel           
                except httpx.HTTPError as e:
                    print(f"Erro ao baixar {url_pdf}: {e}")
                debitos.append(debito)
            with open(caminho_data, "w", encoding="utf-8") as dados:
                json.dump(debitos,dados,ensure_ascii=False,indent=2)
                
if __name__ == "__main__":
    asyncio.run(main())
