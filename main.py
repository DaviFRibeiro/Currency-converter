import customtkinter as ctk
import requests
from tkinter import messagebox
from dotenv import load_dotenv
import os
from typing import List

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API do arquivo .env
API_KEY = os.getenv('API_KEY')

# Função para obter a lista de moedas
def get_currency_list(api_key: str) -> List[str]:
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
    response = requests.get(url)
    data = response.json()
    print("Debug - Data received from API (codes):", data)  # Adiciona mensagem de depuração
    if data.get('result') == 'success':
        return [currency[0] for currency in data.get('supported_codes', [])]
    else:
        return []

# Função para atualizar a taxa de câmbio
def update_exchange_rate(api_key: str, base_currency: str, target_currency: str) -> float:
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    print("Debug - Data received from API (latest):", data)  # Adiciona mensagem de depuração
    if data.get('result') == 'success':
        return data['conversion_rates'].get(target_currency, 0.0)
    else:
        return 0.0

# Função chamada ao clicar no botão
def on_convert():
    base_currency = base_currency_var.get()
    target_currency = target_currency_var.get()
    amount = float(amount_entry.get())
    if base_currency and target_currency:
        rate = update_exchange_rate(API_KEY, base_currency, target_currency)
        converted_amount = amount * rate
        result_label.configure(text=f"Resultado: {converted_amount:.2f} {target_currency}")
    else:
        messagebox.showerror("Erro", "Por favor, selecione as moedas e insira o valor.")

# Criar a janela principal
app = ctk.CTk()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Definir título, tamanho e cor da janela
app.title("Conversor de Moedas")
app.geometry("500x500")
app.configure(bg='white')
# Criar variáveis para armazenar as moedas selecionadas
base_currency_var = ctk.StringVar()
target_currency_var = ctk.StringVar()

titulo = ctk.CTkLabel(app, text="Conversor de Moedas", font=("",20))

# Criar widgets
ctk.CTkLabel(app, text="Quantidade:").pack(pady=20)
amount_entry = ctk.CTkEntry(app)
amount_entry.pack(pady=10)

ctk.CTkLabel(app, text="Selecione a moeda de origem:").pack(pady=20)
base_currency_menu = ctk.CTkOptionMenu(app, values=get_currency_list(API_KEY), variable=base_currency_var)
base_currency_menu.pack(pady=10)

ctk.CTkLabel(app, text="Selecione a moeda de destino:").pack(pady=20)
target_currency_menu = ctk.CTkOptionMenu(app, values=get_currency_list(API_KEY), variable=target_currency_var)
target_currency_menu.pack(pady=10)

convert_button = ctk.CTkButton(app, text="Converter", command=on_convert)
convert_button.pack(pady=30)

def on_convert():
    print("Converter moeda")

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=10)

# Iniciar o loop principal da aplicação
app.mainloop()
