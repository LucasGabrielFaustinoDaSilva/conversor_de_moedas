from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

# Criando a aplicação FastAPI
app = FastAPI()

# Configuração CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aceita requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sua chave de API
ACCESS_KEY = "e56017cf8da0b72a063cc08873f9004d"

# Rota inicial de teste
@app.get("/")
def root():
    return {"message": "API de conversão de moedas funcionando!"}

# Rota para listar moedas válidas (lista fixa)
@app.get("/moedas")
def listar_moedas():
    """
    Retorna um dicionário fixo de moedas válidas para garantir que o frontend funcione.
    """
    return {
        "USD": {"description":"United States Dollar","code":"USD"},
        "BRL": {"description":"Brazilian Real","code":"BRL"},
        "EUR": {"description":"Euro","code":"EUR"},
        "JPY": {"description":"Japanese Yen","code":"JPY"},
        "GBP": {"description":"British Pound","code":"GBP"},
        "AUD": {"description":"Australian Dollar","code":"AUD"},
        "CAD": {"description":"Canadian Dollar","code":"CAD"},
        "CHF": {"description":"Swiss Franc","code":"CHF"},
        "CNY": {"description":"Chinese Yuan","code":"CNY"},
        "INR": {"description":"Indian Rupee","code":"INR"}
    }

# Rota de conversão
@app.get("/converter")
def converter(
    de: str = Query(..., description="Moeda de origem, ex: USD"),
    para: str = Query(..., description="Moeda de destino, ex: BRL"),
    valor: float = Query(..., description="Valor a ser convertido")
):
    print("=== Dados recebidos do frontend ===")
    print("Moeda de origem:", de)
    print("Moeda de destino:", para)
    print("Valor:", valor)

    try:
        url = f"https://api.exchangerate.host/convert?from={de}&to={para}&amount={valor}&access_key={ACCESS_KEY}"
        print("URL que será chamada:", url)

        response = requests.get(url, timeout=10)
        data = response.json()

        print("=== Resposta da API ===")
        print(data)

        if "result" in data and data["result"] is not None:
            return {"valor_convertido": data["result"]}
        else:
            return {"error": "Não foi possível converter. Verifique os códigos das moedas."}

    except requests.exceptions.RequestException as e:
        print("=== Erro ao conectar na API ===")
        print(e)
        return {"error": f"Erro ao conectar na API: {str(e)}"}
