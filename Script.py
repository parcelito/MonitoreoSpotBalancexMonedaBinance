import requests
import time
import sys
from datetime import datetime

def get_crypto_price(symbol):
    """Obtiene el precio actual de la criptomoneda desde Binance"""
    try:
        # Formatear el símbolo para que coincida con el formato de Binance (ej: PEPEUSDT)
        trading_pair = f"{symbol.upper()}USDT"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={trading_pair}"
        
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Binance: {e}")
        return None
    except KeyError:
        print(f"Error: Par {trading_pair} no encontrado en Binance")
        return None
    except ValueError:
        print("Error: Respuesta no válida de Binance")
        return None

def display_balance(symbol, amount):
    """Muestra el balance en tiempo real"""
    print(f"\nMonitoreando balance de {symbol.upper()} - Cantidad: {amount}")
    print("Presiona Ctrl+C para detener...")
    print("-" * 50)
    
    try:
        while True:
            price = get_crypto_price(symbol)
            if price is not None:
                balance = price * amount
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Precio: {price:.8f} USDT | Balance: {balance:.2f} USDT", end='\r')
            time.sleep(1)  # Espera 1 segundo entre consultas
    except KeyboardInterrupt:
        print("\n\nMonitoreo detenido por el usuario.")

def main():
    if len(sys.argv) != 3:
        print("Uso: python binance_balance.py <symbol> <amount>")
        print("Ejemplo: python binance_balance.py pepe 1000")
        sys.exit(1)
    
    symbol = sys.argv[1]
    try:
        amount = float(sys.argv[2])
    except ValueError:
        print("Error: La cantidad debe ser un número válido")
        sys.exit(1)
    
    display_balance(symbol, amount)

if __name__ == "__main__":
    main()