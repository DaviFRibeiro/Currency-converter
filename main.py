import customtkinter as ctk
import requests
from tkinter import messagebox
from dotenv import load_dotenv
import os
from typing import List

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Lista pré-definida de moedas suportadas
SUPPORTED_CURRENCIES = [
    'USD', 'EUR', 'BRL', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'INR'
]

# Função para obter a lista de moedas (usando uma lista fixa)
def get_currency_list() -> List[str]:
    return SUPPORTED_CURRENCIES

# Função para atualizar a taxa de câmbio e retornar os dados
def update_exchange_rate(base_currency: str, target_currency: str) -> dict:
    url = f"https://economia.awesomeapi.com.br/json/last/{base_currency}-{target_currency}"
    response = requests.get(url)
    data = response.json()
    print("Debug - Data received from API:", data)  # Adiciona mensagem de depuração
    return data

# Função chamada ao clicar no botão
def on_convert():
    base_currency = base_currency_var.get()
    target_currency = target_currency_var.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        return
    
    if base_currency and target_currency:
        data = update_exchange_rate(base_currency, target_currency)
        if data and f"{base_currency}{target_currency}" in data:
            rate = data[f"{base_currency}{target_currency}"]['bid']
            converted_amount = amount * float(rate)
            result_label.configure(text=f"Resultado: {converted_amount:.2f} {target_currency}")
        else:
            result_label.configure(text="Erro: Dados não encontrados.")
    else:
        messagebox.showerror("Erro", "Por favor, selecione as moedas e insira o valor.")

# Criar a janela principal
app = ctk.CTk()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Definir título, tamanho e cor da janela
app.title("Conversor de Moedas")
app.geometry("600x600")
app.configure(bg='black')  # Alterado para preto

# Criar variáveis para armazenar as moedas selecionadas
base_currency_var = ctk.StringVar()
target_currency_var = ctk.StringVar()

titulo = ctk.CTkLabel(app, text="Conversor de Moedas", font=("",20))
titulo.pack(pady=20)

# Criar widgets
ctk.CTkLabel(app, text="Quantidade:").pack(pady=20)
amount_entry = ctk.CTkEntry(app)
amount_entry.pack(pady=10)

ctk.CTkLabel(app, text="Selecione a moeda de origem:").pack(pady=20)
base_currency_menu = ctk.CTkOptionMenu(app, values=get_currency_list(), variable=base_currency_var)
base_currency_menu.pack(pady=10)

ctk.CTkLabel(app, text="Selecione a moeda de destino:").pack(pady=20)
target_currency_menu = ctk.CTkOptionMenu(app, values=get_currency_list(), variable=target_currency_var)
target_currency_menu.pack(pady=10)

convert_button = ctk.CTkButton(app, text="Converter", command=on_convert)
convert_button.pack(pady=30)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=10)

api_data_label = ctk.CTkLabel(app, text="")
api_data_label.pack(pady=10)

# Iniciar o loop principal da aplicação
app.mainloop()
