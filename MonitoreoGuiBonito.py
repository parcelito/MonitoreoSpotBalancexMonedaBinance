import requests
import time
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

class CryptoBalanceApp:
    def __init__(self, root, symbol, amount):
        self.root = root
        self.symbol = symbol.upper()
        self.amount = amount
        
        # Configuración de la ventana
        #self.root.title(f"Crypto Tracker: {self.symbol}")
        self.root.geometry("330x185")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#f0f0f0')
        
        # Configurar icono (opcional - necesita un archivo .ico)
        try:
            self.root.iconbitmap('crypto.ico')  # Puedes crear o descargar un icono
        except:
            pass
        
        # Fuentes personalizadas
        self.title_font = tkfont.Font(family='Helvetica', size=12, weight='bold')
        self.data_font = tkfont.Font(family='Courier New', size=12)
        self.big_font = tkfont.Font(family='Helvetica', size=14, weight='bold')
        self.small_font = tkfont.Font(family='Arial', size=8)
        
        # Estilo para los widgets
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Header.TLabel', 
                           background='#2c3e50', 
                           foreground='white', 
                           font=self.title_font,
                           padding=5)
        self.style.configure('Data.TLabel', 
                           background='#f0f0f0',
                           font=self.data_font)
        self.style.configure('Big.TLabel',
                           background='#f0f0f0',
                           foreground='#27ae60',
                           font=self.big_font)
        
        # Crear widgets
        self.create_widgets()
        
        # Iniciar actualización
        self.update_data()
    
    def create_widgets(self):
        # Frame de cabecera
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.pack(fill=tk.X)
        
        #ttk.Label(header_frame, 
                 #text=f"CRYPTO TRACKER - {self.symbol}", 
                 #style='Header.TLabel').pack(pady=5)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Información de la moneda
        ttk.Label(main_frame, 
                 text=f"Moneda:", 
                 style='Data.TLabel').grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(main_frame, 
                 text=f"{self.symbol}", 
                 style='Big.TLabel').grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(main_frame, 
                 text=f"Cantidad:", 
                 style='Data.TLabel').grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(main_frame, 
                 text=f"{self.amount:,.2f}", 
                 style='Data.TLabel').grid(row=1, column=1, sticky=tk.E)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=2, columnspan=2, sticky='ew', pady=5)
        
        # Datos en tiempo real
        ttk.Label(main_frame, 
                 text="Precio actual:", 
                 style='Data.TLabel').grid(row=3, column=0, sticky=tk.W, pady=2)
        self.price_label = ttk.Label(main_frame, 
                                    text="0.00000000 USDT", 
                                    style='Big.TLabel')
        self.price_label.grid(row=3, column=1, sticky=tk.E)
        
        ttk.Label(main_frame, 
                 text="Balance total:", 
                 style='Data.TLabel').grid(row=4, column=0, sticky=tk.W, pady=2)
        self.balance_label = ttk.Label(main_frame, 
                                      text="0.00 USDT", 
                                      style='Big.TLabel')
        self.balance_label.grid(row=4, column=1, sticky=tk.E)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=5, columnspan=2, sticky='ew', pady=5)
        
        # Actualización
        self.update_label = ttk.Label(main_frame, 
                                     text="Conectando a Binance...", 
                                     style='Data.TLabel',
                                     font=self.small_font)
        self.update_label.grid(row=6, columnspan=2, sticky=tk.W)
        
        # Botón de salida
        exit_btn = ttk.Button(main_frame, 
                             text="Salir", 
                             command=self.on_close)
        exit_btn.grid(row=7, columnspan=2, pady=5)
    
    def get_crypto_price(self):
        """Obtiene el precio actual de Binance"""
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
            
            # Cambiar color si el precio baja/sube (simulación)
            if hasattr(self, 'last_price'):
                if price > self.last_price:
                    self.price_label.config(foreground='#27ae60')  # Verde
                elif price < self.last_price:
                    self.price_label.config(foreground='#e74c3c')  # Rojo
            
            self.last_price = price
            
            # Actualizar interfaz
            self.price_label.config(text=f"{price:.8f} USDT")
            self.balance_label.config(text=f"{balance:,.2f} USDT")
            #self.update_label.config(text=f"Última actualización: {current_time} | Binance API")
            self.update_label.config(text=f"Última actualización: {current_time}")
        
        # Programar próxima actualización
        self.root.after(1000, self.update_data)
    
    def on_close(self):
        """Maneja el cierre de la ventana"""
        self.root.destroy()
        sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print("Uso: python binance_tracker.py <symbol> <amount>")
        print("Ejemplo: python binance_tracker.py pepe 1000")
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