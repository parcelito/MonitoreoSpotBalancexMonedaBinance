import requests
import time
import sys
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

class CryptoBalanceApp:
    def __init__(self, root, symbol, amount):
        self.root = root
        self.symbol = symbol.upper()
        self.amount = amount
        self.history_data = []
        self.analysis_result = None
        
        # Configuración de la ventana
        self.root.geometry("420x470")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#f0f0f0')
        
        try:
            self.root.iconbitmap('crypto.ico')
        except:
            pass
        
        # Fuentes personalizadas
        self.title_font = tkfont.Font(family='Helvetica', size=12, weight='bold')
        self.data_font = tkfont.Font(family='Courier New', size=12)
        self.big_font = tkfont.Font(family='Helvetica', size=14, weight='bold')
        self.small_font = tkfont.Font(family='Arial', size=8)
        self.analysis_font = tkfont.Font(family='Arial', size=10, weight='bold')
        
        # Estilo para los widgets
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Data.TLabel', background='#f0f0f0', font=self.data_font)
        self.style.configure('Big.TLabel', background='#f0f0f0', foreground='#27ae60', font=self.big_font)
        self.style.configure('Analysis.TLabel', background='#f0f0f0', font=self.analysis_font)
        
        # Crear widgets
        self.create_widgets()
        
        # Iniciar actualización
        self.update_data()
        self.root.after(30000, self.perform_deepseek_analysis)  # Análisis cada 30 segundos
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sección de datos básicos
        data_frame = ttk.Frame(main_frame)
        data_frame.grid(row=0, column=0, sticky='nsew')
        
        ttk.Label(data_frame, text=f"Moneda:", style='Data.TLabel').grid(row=0, column=0, sticky=tk.W)
        ttk.Label(data_frame, text=f"{self.symbol}", style='Big.TLabel').grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(data_frame, text=f"Cantidad:", style='Data.TLabel').grid(row=1, column=0, sticky=tk.W)
        ttk.Label(data_frame, text=f"{self.amount:,.2f}", style='Data.TLabel').grid(row=1, column=1, sticky=tk.E)
        
        ttk.Label(data_frame, text="Precio actual:", style='Data.TLabel').grid(row=2, column=0, sticky=tk.W)
        self.price_label = ttk.Label(data_frame, text="0.00000000 USDT", style='Big.TLabel')
        self.price_label.grid(row=2, column=1, sticky=tk.E)
        
        ttk.Label(data_frame, text="Balance total:", style='Data.TLabel').grid(row=3, column=0, sticky=tk.W)
        self.balance_label = ttk.Label(data_frame, text="0.00 USDT", style='Big.TLabel')
        self.balance_label.grid(row=3, column=1, sticky=tk.E)
        
        # Sección de análisis
        analysis_frame = ttk.Frame(main_frame)
        analysis_frame.grid(row=1, column=0, sticky='nsew', pady=(10,0))
        
        ttk.Label(analysis_frame, text="Análisis de Mercado:", style='Analysis.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        self.analysis_text = tk.Text(analysis_frame, height=4, width=50, wrap=tk.WORD, 
                                    font=self.small_font, bg='#f0f0f0', relief=tk.FLAT)
        self.analysis_text.grid(row=1, column=0, sticky='nsew')
        self.analysis_text.insert(tk.END, "Recopilando datos para el primer análisis...")
        self.analysis_text.config(state=tk.DISABLED)
        
        # Sección de gráfico
        self.figure = plt.Figure(figsize=(5, 2.5), dpi=80)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky='nsew', pady=(10,0))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky='nsew', pady=(10,0))
        
        ttk.Button(button_frame, text="Actualizar Análisis", command=self.perform_deepseek_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ver Histórico", command=self.show_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salir", command=self.on_close).pack(side=tk.RIGHT, padx=5)
        
        # Actualización
        self.update_label = ttk.Label(main_frame, text="Conectando a Binance...", style='Data.TLabel', font=self.small_font)
        self.update_label.grid(row=4, column=0, sticky=tk.W)
    
    def get_crypto_price(self):
        """Obtiene el precio actual de Binance"""
        try:
            trading_pair = f"{self.symbol}USDT"
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={trading_pair}"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            price = float(data['price'])
            
            # Guardar histórico
            self.history_data.append({
                'timestamp': datetime.now(),
                'price': price
            })
            
            # Mantener solo las últimas 100 entradas
            if len(self.history_data) > 100:
                self.history_data = self.history_data[-100:]
            
            return price
        except Exception as e:
            print(f"Error obteniendo precio: {e}")
            return None
    
    def update_data(self):
        """Actualiza los datos en la interfaz"""
        price = self.get_crypto_price()
        
        if price is not None:
            balance = price * self.amount
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Cambiar color según movimiento
            if hasattr(self, 'last_price'):
                if price > self.last_price:
                    self.price_label.config(foreground='#27ae60')  # Verde
                elif price < self.last_price:
                    self.price_label.config(foreground='#e74c3c')  # Rojo
            
            self.last_price = price
            
            # Actualizar interfaz
            self.price_label.config(text=f"{price:.8f} USDT")
            self.balance_label.config(text=f"{balance:,.2f} USDT")
            self.update_label.config(text=f"Última actualización: {current_time}")
            
            # Actualizar gráfico
            self.update_chart()
        
        # Programar próxima actualización
        self.root.after(1000, self.update_data)
    
    def update_chart(self):
        """Actualiza el gráfico de precios"""
        if len(self.history_data) < 2:
            return
            
        self.ax.clear()
        
        timestamps = [x['timestamp'] for x in self.history_data]
        prices = [x['price'] for x in self.history_data]
        
        self.ax.plot(timestamps, prices, color='#3498db', linewidth=2)
        self.ax.set_title(f"Historial de precios - {self.symbol}", fontsize=10)
        self.ax.set_ylabel("Precio (USDT)", fontsize=8)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Formatear ejes
        self.ax.xaxis.set_tick_params(labelsize=7)
        self.ax.yaxis.set_tick_params(labelsize=7)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def perform_deepseek_analysis(self):
        """Realiza análisis de mercado usando lógica simulada de DeepSeek"""
        if len(self.history_data) < 10:
            self.analysis_text.config(state=tk.NORMAL)
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, "Recopilando más datos para análisis...")
            self.analysis_text.config(state=tk.DISABLED)
            self.root.after(30000, self.perform_deepseek_analysis)
            return
        
        try:
            # Simular llamada a API de DeepSeek (en realidad hacemos análisis local)
            analysis = self.simulate_deepseek_analysis()
            
            # Mostrar resultados
            self.analysis_text.config(state=tk.NORMAL)
            self.analysis_text.delete(1.0, tk.END)
            
            # Añadir recomendación
            self.analysis_text.insert(tk.END, f"Recomendación: {analysis['recommendation']}\n", 'bold')
            self.analysis_text.tag_config('bold', font=('Arial', 10, 'bold'))
            
            # Añadir razones
            self.analysis_text.insert(tk.END, "\nRazones:\n")
            for reason in analysis['reasons']:
                self.analysis_text.insert(tk.END, f"- {reason}\n")
            
            # Añadir estadísticas
            self.analysis_text.insert(tk.END, "\nEstadísticas:\n")
            for stat, value in analysis['stats'].items():
                self.analysis_text.insert(tk.END, f"- {stat}: {value}\n")
            
            self.analysis_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Error en análisis: {e}")
            self.analysis_text.config(state=tk.NORMAL)
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, f"Error en análisis: {str(e)}")
            self.analysis_text.config(state=tk.DISABLED)
        
        # Programar próximo análisis
        self.root.after(30000, self.perform_deepseek_analysis)
    
    def simulate_deepseek_analysis(self):
        """Simula el análisis de DeepSeek con los datos históricos"""
        if len(self.history_data) < 10:
            return {
                'recommendation': 'Esperar (datos insuficientes)',
                'reasons': ['Necesitamos más datos históricos para un análisis preciso'],
                'stats': {}
            }
        
        # Convertir a DataFrame para análisis
        df = pd.DataFrame(self.history_data)
        df['price_change'] = df['price'].pct_change()
        
        # Calcular métricas
        last_price = df.iloc[-1]['price']
        avg_10 = df['price'].tail(10).mean()
        avg_30 = df['price'].tail(30).mean()
        volatility = df['price_change'].std() * 100  # Volatilidad en %
        
        # Determinar tendencia
        short_trend = "alcista" if last_price > avg_10 else "bajista"
        long_trend = "alcista" if avg_10 > avg_30 else "bajista"
        
        # Generar recomendación
        recommendation = "Mantener"
        reasons = []
        
        if short_trend == "alcista" and long_trend == "alcista":
            recommendation = "Considerar comprar más"
            reasons.append("Tendencia alcista a corto y largo plazo")
        elif short_trend == "bajista" and long_trend == "bajista":
            recommendation = "Considerar vender"
            reasons.append("Tendencia bajista a corto y largo plazo")
        elif short_trend == "alcista" and long_trend == "bajista":
            recommendation = "Mantener con precaución"
            reasons.append("Recuperación a corto plazo pero tendencia bajista general")
        else:
            recommendation = "Mantener y observar"
            reasons.append("Corrección temporal en tendencia alcista")
        
        if volatility > 5:
            reasons.append(f"Alta volatilidad ({volatility:.2f}%) - Mercado inestable")
        
        # Estadísticas
        stats = {
            "Precio actual": f"{last_price:.8f} USDT",
            "Media (10 periodos)": f"{avg_10:.8f} USDT",
            "Media (30 periodos)": f"{avg_30:.8f} USDT",
            "Volatilidad": f"{volatility:.2f}%",
            "Tendencia corto plazo": short_trend,
            "Tendencia largo plazo": long_trend
        }
        
        return {
            'recommendation': recommendation,
            'reasons': reasons,
            'stats': stats
        }
    
    def show_history(self):
        """Muestra el historial completo en una nueva ventana"""
        if not self.history_data:
            messagebox.showinfo("Historial", "No hay suficientes datos históricos aún")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title(f"Historial completo - {self.symbol}")
        history_window.geometry("600x400")
        
        text = tk.Text(history_window, wrap=tk.WORD)
        scroll = ttk.Scrollbar(history_window, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(fill=tk.BOTH, expand=True)
        
        # Formatear datos históricos
        text.insert(tk.END, f"Historial de precios para {self.symbol}\n\n")
        text.insert(tk.END, "Fecha/Hora\t\tPrecio (USDT)\tCambio %\n")
        text.insert(tk.END, "-"*50 + "\n")
        
        for i in range(1, len(self.history_data)):
            current = self.history_data[i]
            prev = self.history_data[i-1]
            change_pct = ((current['price'] - prev['price']) / prev['price']) * 100
            
            text.insert(tk.END, 
                       f"{current['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\t" +
                       f"{current['price']:.8f}\t" +
                       f"{change_pct:+.2f}%\n")
        
        text.config(state=tk.DISABLED)
    
    def on_close(self):
        """Maneja el cierre de la ventana"""
        self.root.destroy()
        sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print("Uso: python crypto_analyzer.py <symbol> <amount>")
        print("Ejemplo: python crypto_analyzer.py pepe 1000")
        sys.exit(1)
    
    symbol = sys.argv[1]
    try:
        amount = float(sys.argv[2])
    except ValueError:
        print("Error: La cantidad debe ser un número válido")
        sys.exit(1)
    
    root = tk.Tk()
    app = CryptoBalanceApp(root, symbol, amount)
    root.mainloop()

if __name__ == "__main__":
    main()