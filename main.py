import customtkinter as ctk
import requests
from tkinter import messagebox
from dotenv import load_dotenv
import os
from typing import List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

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

# Função para obter histórico de taxas de câmbio
def get_exchange_rate_history(base_currency: str, target_currency: str) -> List[dict]:
    url = f"https://economia.awesomeapi.com.br/json/daily/{base_currency}-{target_currency}/30"
    response = requests.get(url)
    data = response.json()
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
            
            # Atualizar a data e hora da consulta
            api_date = data[f"{base_currency}{target_currency}"]['create_date']
            api_data_label.configure(text=f"Data da consulta: {api_date}")
            
            # Obter e plotar o histórico da taxa de câmbio
            history_data = get_exchange_rate_history(base_currency, target_currency)
            plot_exchange_rate_history(history_data)
        else:
            result_label.configure(text="Erro: Dados não encontrados.")
            api_data_label.configure(text="")
    else:
        messagebox.showerror("Erro", "Por favor, selecione as moedas e insira o valor.")

# Função para plotar o histórico da taxa de câmbio
def plot_exchange_rate_history(history_data):
    dates = []
    rates = []
    for item in history_data:
        try:
            timestamp = int(item['timestamp'])
            date = datetime.datetime.fromtimestamp(timestamp)
            rate = float(item['bid'])
            dates.append(date)
            rates.append(rate)
        except (ValueError, KeyError) as e:
            print(f"Erro ao processar dados de histórico: {e}")
            continue
    
    if dates and rates:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(dates, rates, marker='o')
        ax.set_title('Histórico da Taxa de Câmbio')
        ax.set_xlabel('Data')
        ax.set_ylabel('Taxa de Câmbio')
        
        canvas = FigureCanvasTkAgg(fig, master=app)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=5)
        
        ax.xaxis.set_major_formatter(plt.FixedFormatter(dates))
        plt.gcf().autofmt_xdate()

# Criar a janela principal
app = ctk.CTk()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Definir título, tamanho e cor da janela
app.title("Conversor de Moedas")
app.geometry("800x900")
app.configure(bg='black')  # Alterado para preto

# Criar variáveis para armazenar as moedas selecionadas
base_currency_var = ctk.StringVar()
target_currency_var = ctk.StringVar()

titulo = ctk.CTkLabel(app, text="Conversor de Moedas", font=("", 20))
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
