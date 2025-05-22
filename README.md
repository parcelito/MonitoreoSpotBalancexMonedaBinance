# 🚀 Monitor de Criptomonedas con Análisis de Mercado

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

Aplicación gráfica para monitorear balances de criptomonedas en tiempo real con análisis de mercado simulados con IA.

## 🌟 Características principales

- 📊 **Seguimiento de precios en tiempo real** usando la API de Binance
- 💰 Cálculo del valor del portafolio
- 📈 Gráfico interactivo con histórico de precios
- 🤖 **Análisis de mercado simulando IA** (estilo DeepSeek)
- 🔍 Recomendaciones de compra/venta/mantener
- 🔄 Análisis de tendencias del mercado
- ⚡ Indicadores de volatilidad
- 🕰️ Visor completo de historial de precios

## 📋 Requisitos

- **Python 3.7 o superior**
- Paquetes necesarios:
  ```plaintext
  requests
  tkinter
  matplotlib
  pandas
  numpy
  ```
## ⚙️ Instalación
- Clona el repositorio o descarga el script:
    ```bash
    git clone https://github.com/tuusuario/monitor-cripto.git
    cd monitor-cripto
    ```
- Instala las dependencias requeridas:
    ```bash
    pip install -r requirements.txt
    ```
## 🖥️ Uso
- Ejecuta el script con el símbolo de la criptomoneda y la cantidad que posees:
    ```bash
    python MonitoreoGuiConIA.py <SÍMBOLO_CRIPTO> <CANTIDAD>
    ```
- Ejemplo:
    ```bash
    python MonitoreoGuiConIA.py BTC 0.5
    ```
- Esto monitoreará 0.5 Bitcoin y mostrará su valor actual en USDT.

## 🖼️ Descripción de la interfaz
### Secciones principales:
- 📈 Sección de datos en tiempo real: Muestra el precio actual y valor del portafolio
- 🤖 Análisis de mercado: Proporciona recomendaciones generadas por IA simulada
- 📊 Gráfico de precios: Muestra los movimientos históricos del precio
### 🎛️ Controles:
- 🔄 Actualizar Análisis - Forzar actualización inmediata del análisis
- 📅 Ver Histórico - Mostrar historial completo de precios
- 🚪 Salir - Cerrar la aplicación

## ⚙️ Detalles técnicos
- Los datos se obtienen de la API de Binance cada segundo
- El análisis de mercado se realiza cada 30 segundos
- La aplicación mantiene los últimos 100 puntos de precio

## 🔍 El análisis incluye:
- Tendencias a corto (10 periodos) y largo plazo (30 periodos)
- Cálculo de volatilidad
- Comparación de medias móviles

## ⚠️ Descargo de responsabilidad
- Importante: Este software se proporciona únicamente con fines educativos e informativos. No constituye asesoramiento financiero y no debe utilizarse como base única para tomar decisiones de inversión. Las inversiones en criptomonedas son inherentemente riesgosas y siempre debe realizar su propia investigación y consultar con un asesor financiero calificado antes de tomar cualquier decisión de inversión.
- Al utilizar este software, usted reconoce que es el único responsable de las decisiones de inversión que tome y que el desarrollador no será responsable de ninguna pérdida o daño que surja de su uso de esta herramienta.

## 📜 Licencia
- Este proyecto está licenciado bajo la Licencia MIT.

## ❓ Soporte
- Para problemas o solicitudes de características, por favor abre un issue en el repositorio de GitHub.