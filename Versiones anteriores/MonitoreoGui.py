import requests
import time
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class CryptoBalanceApp:
    def __init__(self, root, symbol, amount):
        self.root = root
        self.symbol = symbol.upper()
        self.amount = amount
        
        # Configuración de la ventana
        self.root.title(f"Balance: {self.symbol}")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  # Siempre visible
        
        # Evitar que la ventana se minimice (pero permite cerrarla)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('Big.TLabel', font=('Arial', 14, 'bold'))
        
        # Elementos de la interfaz
        self.create_widgets()
        
        # Iniciar actualización de datos
        self.update_data()
    
    def create_widgets(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Etiquetas de información
        ttk.Label(main_frame, text=f"Moneda: {self.symbol}").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(main_frame, text=f"Cantidad: {self.amount:,}").grid(row=1, column=0, sticky=tk.W)
        
        # Precio actual
        ttk.Label(main_frame, text="Precio actual:").grid(row=2, column=0, sticky=tk.W)
        self.price_label = ttk.Label(main_frame, text="0.00000000 USDT", style='Big.TLabel')
        self.price_label.grid(row=2, column=1, sticky=tk.E)
        
        # Balance total
        ttk.Label(main_frame, text="Balance total:").grid(row=3, column=0, sticky=tk.W)
        self.balance_label = ttk.Label(main_frame, text="0.00 USDT", style='Big.TLabel')
        self.balance_label.grid(row=3, column=1, sticky=tk.E)
        
        # Última actualización
        self.update_label = ttk.Label(main_frame, text="", font=('Arial', 8))
        self.update_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)
    
    def get_crypto_price(self):
        """Obtiene el precio actual de la criptomoneda desde Binance"""
        try:
            trading_pair = f"{self.symbol}USDT"
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={trading_pair}"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return float(data['price'])
        except Exception as e:
            print(f"Error obteniendo precio: {e}")
            return None
    
    def update_data(self):
        """Actualiza los datos en la interfaz"""
        price = self.get_crypto_price()
        
        if price is not None:
            balance = price * self.amount
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Actualizar interfaz
            self.price_label.config(text=f"{price:.8f} USDT")
            self.balance_label.config(text=f"{balance:.2f} USDT")
            self.update_label.config(text=f"Última actualización: {current_time}")
        
        # Programar próxima actualización (cada segundo)
        self.root.after(1000, self.update_data)
    
    def on_close(self):
        """Maneja el cierre de la ventana"""
        self.root.destroy()
        sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print("Uso: python binance_balance_gui.py <symbol> <amount>")
        print("Ejemplo: python binance_balance_gui.py pepe 1000")
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