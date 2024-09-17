import customtkinter as ctk
import requests
from tkinter import messagebox
from dotenv import load_dotenv
import os
import platform  # Import necessário para detectar o sistema operacional
from typing import List
import threading  # Para evitar que a interface trave durante a requisição
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

# Função para limpar o terminal
def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Função para criar a interface gráfica
def create_gui():
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

    # Função para obter os dados históricos de câmbio do mês atual
    def get_historical_data(base_currency: str, target_currency: str) -> List[dict]:
        today = datetime.date.today()
        start_date = today.replace(day=1)  # Começa no primeiro dia do mês
        url = f"https://economia.awesomeapi.com.br/json/daily/{base_currency}-{target_currency}/30"
        response = requests.get(url)
        data = response.json()
        historical_data = [
            {
                'date': datetime.datetime.fromtimestamp(int(item['timestamp'])).date(),
                'high': float(item['high']),
                'low': float(item['low'])
            }
            for item in data if datetime.datetime.fromtimestamp(int(item['timestamp'])).date() >= start_date
        ]
        return historical_data

    # Função para desenhar o gráfico dos dados históricos
    def draw_graph(historical_data: List[dict], base_currency: str, target_currency: str):
        dates = [item['date'] for item in historical_data]
        highs = [item['high'] for item in historical_data]
        lows = [item['low'] for item in historical_data]

        fig, ax = plt.subplots()
        ax.plot(dates, highs, label='Alta', color='green')
        ax.plot(dates, lows, label='Baixa', color='red')

        ax.set_title(f'Variação de {base_currency} para {target_currency} - Mês Atual')
        ax.set_xlabel('Data')
        ax.set_ylabel('Taxa de Câmbio')
        ax.legend()

        return fig

    # Função para processar a conversão e exibir o resultado
    def process_conversion():
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
                
                # Obter dados históricos e desenhar gráfico
                historical_data = get_historical_data(base_currency, target_currency)
                fig = draw_graph(historical_data, base_currency, target_currency)
                
                # Remover o gráfico anterior (se existir)
                global canvas
                if canvas:
                    canvas.get_tk_widget().destroy()
                
                # Exibir novo gráfico na interface
                canvas = FigureCanvasTkAgg(fig, master=app)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=20)

            else:
                result_label.configure(text="Erro: Dados não encontrados.")
        else:
            messagebox.showerror("Erro", "Por favor, selecione as moedas e insira o valor.")

    # Função chamada ao clicar no botão (executa em uma nova thread)
    def on_convert():
        threading.Thread(target=process_conversion).start()

    # Criar a janela principal
    app = ctk.CTk()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Definir título, tamanho e cor da janela
    app.title("Conversor de Moedas")
    app.geometry("600x800")  # Aumentado para comportar o gráfico
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

    # Variável global para armazenar o canvas do gráfico
    global canvas
    canvas = None

    # Iniciar o loop principal da aplicação
    app.mainloop()

# Verificar se o script está sendo executado diretamente
if __name__ == "__main__":
    clear_terminal()  # Limpar o terminal
    create_gui()      # Criar a interface gráfica
