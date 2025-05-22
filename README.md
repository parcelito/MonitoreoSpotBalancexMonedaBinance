# 🚀 Monitor de Criptomonedas con Análisis de Mercado

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)

[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

Aplicación gráfica para monitorear balances de criptomonedas en tiempo real con análisis de mercado simulados con IA.

![Demo de la aplicación](https://via.placeholder.com/800x400?text=Demo+Monitor+Cripto+GUI)  
*(Imagen ilustrativa)*

---

## 🌟 Características principales

- 📊 **Seguimiento de precios en tiempo real** usando la API de Binance
- 💰 Cálculo automático del valor del portafolio
- 📈 Gráfico interactivo con histórico de precios
- 🤖 **Análisis de mercado con IA simulada** (estilo DeepSeek)
- 🔍 Recomendaciones inteligentes de compra/venta/mantener
- 🔄 Análisis de tendencias del mercado en múltiples timeframe
- ⚡ Indicadores de volatilidad en tiempo real
- 🕰️ Visor completo de historial de precios

---

## 📋 Requisitos del sistema

### Requisitos mínimos:
- **Python 3.7 o superior**
- **Sistema operativo**: Windows 10+/macOS 10.15+/Linux

### Dependencias:
```plaintext
requests >= 2.28.0
tkinter >= 8.6
matplotlib >= 3.6.0
pandas >= 1.5.0
numpy >= 1.23.0```



```bash
git clone https://github.com/tuusuario/monitor-cripto.git
cd monitor-cripto```
Instala las dependencias:

bash
pip install -r requirements.txt
Método alternativo (instalación manual):
bash
pip install requests matplotlib pandas numpy
Configuración inicial:
Edita el archivo config.ini para personalizar:

Intervalo de actualización

Umbrales de alerta

Parámetros de análisis

🖥️ Uso básico
Sintaxis:
bash
python MonitoreoGuiConIA.py [CRYPTO_SYMBOL] [AMOUNT]
Ejemplos:
bash

##  🛠️ Instalación y Configuración
### Método recomendado (clonación del repositorio):
Clona el repositorio:

# Monitorear 0.5 Bitcoin
python MonitoreoGuiConIA.py BTC 0.5

# Monitorear 10 Ethereum
python MonitoreoGuiConIA.py ETH 10
🖼️ Interfaz gráfica
Panel principal:
📊 Dashboard en tiempo real:

Precio actual (USD)

Valor de portafolio

Cambio porcentual (24h)

📈 Gráfico interactivo:

Visualización de tendencias

Zoom y paneo

Múltiples timeframe

🤖 Panel de IA:

Recomendaciones automáticas

Análisis de sentimiento

Predicciones de volatilidad

❓ Soporte técnico
Para reportar problemas o sugerencias: