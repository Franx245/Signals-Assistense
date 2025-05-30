"""
Trading Assistant - Automatización de Trading con Telegram y MetaTrader 5
=====================================================================

¿Qué es?
--------
Este es un asistente automatizado que conecta Telegram con MetaTrader 5 para ejecutar 
operaciones de trading de forma automática. Funciona como un "puente inteligente" 
que monitorea señales de trading en canales de Telegram y las ejecuta automáticamente 
en tu cuenta de MetaTrader 5.

¿Por qué es útil?
----------------
1. Automatización:
   - Elimina la necesidad de estar pendiente 24/7 de las señales de trading
   - Reduce el error humano en la ejecución de operaciones
   - Asegura que no te pierdas ninguna oportunidad de trading

2. Precisión y Velocidad:
   - Ejecuta órdenes instantáneamente cuando se reciben las señales
   - Mantiene un registro detallado de todas las operaciones
   - Gestiona automáticamente stop loss y take profit

3. Gestión de Riesgo:
   - Maneja automáticamente el cierre de posiciones
   - Implementa break-even automático
   - Mantiene un registro detallado para análisis posterior

¿Cómo funciona? (Paso a Paso)
---------------------------
1. Conexión Inicial:
   - Se conecta a tu cuenta de Telegram
   - Establece conexión con MetaTrader 5
   - Permite seleccionar el canal de señales a monitorear

2. Monitoreo Continuo:
   - Escucha constantemente nuevos mensajes en el canal seleccionado
   - Detecta automáticamente señales de trading en formato específico
   - Identifica comandos de gestión (cerrar, break even, etc.)

3. Procesamiento de Señales:
   - Analiza cada mensaje para extraer:
     * Par de divisas (ej: EURUSD)
     * Tipo de orden (Compra/Venta)
     * Precio de entrada
     * Stop Loss
     * Take Profit

4. Ejecución Automática:
   - Abre órdenes cuando se alcanza el precio objetivo
   - Gestiona modificaciones de órdenes (break even, etc.)
   - Cierra posiciones según las instrucciones

5. Registro y Monitoreo:
   - Guarda todas las operaciones en logs detallados
   - Mantiene estadísticas de rendimiento
   - Permite consultar el estado actual de operaciones

Sistema de Acciones y Respuestas:
------------------------------
1. Acciones Principales:
   
   a) Entrada de Órdenes:
      - hit entry: Ejecuta orden al precio especificado
      - buy now: Compra inmediata a mercado
      - sell now: Venta inmediata a mercado
      Ejemplo:
      ```
      Señal original:
      EURUSD
      BUY @ 1.0500
      SL 1.0450
      TP 1.0600

      Respuesta: "hit entry" -> Ejecuta la orden cuando se alcanza 1.0500
      Respuesta: "buy now" -> Ejecuta compra inmediata al precio actual
      ```

   b) Gestión de Riesgo:
      - be (break even): Mueve el stop loss al punto de entrada
      - sl: Modifica el stop loss
      - tp: Registra/modifica take profit
      Ejemplo:
      ```
      Orden activa comprando EURUSD desde 1.0500
      Respuesta: "be" -> Stop loss se mueve a 1.0500
      Respuesta: "sl 1.0480" -> Modifica stop loss a 1.0480
      ```

   c) Control de Posiciones:
      - cerrar: Cierra la posición activa
      - cancel: Cancela una orden pendiente
      - round: Reactiva una señal cancelada
      Ejemplo:
      ```
      Orden pendiente de venta EURUSD
      Respuesta: "cancel" -> Cancela la orden
      Más tarde: "round" -> Reactiva la misma señal
      ```

2. Sistema de Cascada de Respuestas:
   
   El sistema sigue la cadena de respuestas en Telegram para relacionar acciones con señales:
   ```
   Señal Original -> Respuesta 1 -> Respuesta 2 -> Respuesta 3
   ```
   
   Ejemplo de cascada:
   ```
   Señal: "EURUSD BUY @ 1.0500..."
   ↳ Respuesta: "hit entry" (ejecuta orden)
   　↳ Respuesta: "be" (mueve SL a entrada)
   　　↳ Respuesta: "tp" (registra TP alcanzado)
   ```

3. Escenarios Comunes:

   a) Entrada y Gestión Básica:
   ```
   1. Señal recibida: EURUSD BUY @ 1.0500
   2. Precio alcanza 1.0500 -> Orden ejecutada
   3. Precio sube -> "be" para asegurar sin pérdidas
   4. Precio alcanza TP -> "tp" para registrar ganancia
   ```

   b) Gestión de Riesgo Activa:
   ```
   1. Señal recibida: GBPUSD SELL @ 1.2600
   2. "sell now" para entrar inmediatamente
   3. "sl 1.2620" para ajustar stop loss
   4. "cerrar" si el mercado no se comporta según lo esperado
   ```

   c) Reactivación de Señales:
   ```
   1. Señal recibida pero precio no favorable
   2. "cancel" para cancelar orden
   3. Más tarde, mejores condiciones
   4. "round" para reactivar la misma señal
   ```

4. Características Especiales:

   a) Seguimiento Automático:
      - Monitoreo continuo de precios
      - Ejecución automática cuando se alcanzan niveles
      - Registro detallado de cada acción

   b) Gestión de Estados:
      - Pendiente: Orden esperando precio
      - Activa: Orden en mercado
      - Cancelada: Orden cancelada pero recuperable
      - Cerrada: Operación finalizada

   c) Seguridad:
      - Verificación de permisos
      - Validación de órdenes
      - Protección contra duplicados
      - Reintentos automáticos

Formato de Señales:
-----------------
Las señales deben seguir este formato preciso:
```
EURUSD
SELL @ 1.0500
SL 1.0550
TP 1.0450
```

Gestión de Errores:
-----------------
- Reconexión automática si se pierde la conexión
- Reintentos automáticos en caso de fallos
- Notificaciones detalladas de errores
- Sistema de logs para diagnóstico

Beneficios Clave:
---------------
1. Ahorro de Tiempo:
   - No necesitas estar pendiente constantemente
   - Ejecución automática 24/7
   - Gestión automática de posiciones

2. Mejora de Resultados:
   - Elimina errores emocionales
   - Ejecución precisa de señales
   - Mantiene disciplina en el trading

3. Análisis y Mejora:
   - Estadísticas detalladas de operaciones
   - Registro completo para análisis
   - Facilita la optimización de estrategias

Requisitos Técnicos:
------------------
- Python 3.8 o superior
- Cuenta de Telegram con API configurada
- MetaTrader 5 instalado y configurado
- Conexión a internet estable

Para Empezar:
-----------
1. Configura tus credenciales de Telegram (API_ID y API_HASH)
2. Asegúrate de que MetaTrader 5 esté abierto y conectado
3. Ejecuta el script: python3 main.py
4. Selecciona el canal de señales a monitorear
5. ¡Listo! El sistema comenzará a operar automáticamente

Versión: 1.0.0
Última actualización: 2024-01-01
Autor: Fran
"""

# =============================================================================
# Imports
# =============================================================================

# Stdlib imports
import asyncio
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import time
from datetime import datetime

# Third-party imports
import pytz
from telethon import TelegramClient, events

# Configuración inicial de logging
logger = logging.getLogger('trading_assistant')

# Configuración de directorios y logging
DATA_DIR = "data"
LOGS_DIR = os.path.join(DATA_DIR, "logs")

# Crear directorios necesarios
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(os.path.join(LOGS_DIR, 'backup'), exist_ok=True)

# Configuración de logging
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5

# Configurar zona horaria
timezone = pytz.timezone('America/Argentina/Buenos_Aires')

class ColoredFormatter(logging.Formatter):
    """Implementación básica de formatter con colores ANSI."""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[41m',  # Red BG
    }
    RESET = '\033[0m'
    
    def format(self, record):
        if not hasattr(record, 'log_color'):
            color = self.COLORS.get(record.levelname, '')
            # Añadir el color al inicio y el reset al final del mensaje
            record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)

# Intentar importar colorlog para funcionalidad adicional
try:
    import colorlog
    ColoredFormatter = colorlog.ColoredFormatter
except ImportError:
    pass  # Usar nuestra implementación básica de ColoredFormatter

def init_logging():
    """
    Inicializa el sistema de logging con configuración mejorada.
    Esta función debe ser llamada una sola vez al inicio del programa.
    """
    global logger
    
    # Evitar inicialización múltiple
    if logger.handlers:
        return logger
    
    try:
        # Crear directorios necesarios
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(LOGS_DIR, exist_ok=True)
        os.makedirs(os.path.join(LOGS_DIR, 'backup'), exist_ok=True)

        # Configurar el logger principal
        logger.setLevel(logging.INFO)

        # Handler para la consola con formato colorizado
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt=LOG_DATE_FORMAT
        ))
        logger.addHandler(console_handler)

        # Handler para archivo general con rotación
        file_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, 'trading_assistant.log'),
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
        logger.addHandler(file_handler)

        # Handler específico para errores
        error_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, 'errors.log'),
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s\nStack trace:\n%(exc_info)s',
            datefmt=LOG_DATE_FORMAT
        ))
        logger.addHandler(error_handler)

        log_mensaje("Sistema de logging inicializado correctamente", nivel='info')
        return logger
        
    except Exception as e:
        # Si falla la inicialización del logging, configurar un handler básico
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt=LOG_DATE_FORMAT
        )
        logger.error(f"Error inicializando sistema de logging: {e}", exc_info=True)
        return logger

# Local imports
from mt5_client import (
    conectar, 
    cerrar, 
    abrir_orden, 
    cerrar_orden, 
    mover_sl_be
)
from utils.filters import (
    parse_senal,
    detectar_accion_mensaje,
    encontrar_senal_original
)

# =============================================================================
# Configuración y Constantes
# =============================================================================

# Información de versión
VERSION = "1.0.0"  # Actualizar al hacer cambios significativos
AUTHOR = "Fran"
UPDATE_DATE = "2024-01-01"  # Actualizar al hacer modificaciones

# Configuración de Telegram
API_ID = 123
API_HASH = ''

def get_timestamp():
    """
    Obtiene el timestamp actual en formato Buenos Aires.
    Returns:
        str: Fecha y hora actual en formato 'YYYY-MM-DD HH:MM:SS TZ'
    """
    return datetime.now(timezone).strftime(LOG_DATE_FORMAT + ' %Z')

def log_mensaje(mensaje, nivel='info', mostrar=True, exc_info=None):
    """
    Función unificada para logging con manejo de errores mejorado.
    
    Args:
        mensaje (str): Mensaje a registrar
        nivel (str): Nivel de log ('debug', 'info', 'warning', 'error', 'critical')
        mostrar (bool): Si se debe mostrar el mensaje en consola
        exc_info: Información de excepción para errores
    """
    log_func = getattr(logger, nivel)
    
    # Añadir contexto al mensaje
    contexto = {
        'timestamp': get_timestamp(),
        'nivel': nivel.upper(),
        'modulo': __name__
    }
    
    mensaje_formateado = f"{mensaje}"
    
    # Log con manejo de excepciones
    try:
        log_func(mensaje_formateado, exc_info=exc_info)
    except Exception as e:
        # Si falla el logging, intentar registrar el error
        print(f"Error logging message: {e}")
        try:
            with open(os.path.join(LOGS_DIR, 'logging_errors.txt'), 'a') as f:
                f.write(f"{get_timestamp()} - Error logging: {e}\nOriginal message: {mensaje}\n")
        except:
            pass

def print_banner():
    """
    Muestra el banner de inicio del sistema.
    """
    banner = f"""
╔══════════════════════════════════════╗
║     🤖 Trading Assistant v{VERSION}     ║
║        Telegram + MT5 Bridge         ║
╚══════════════════════════════════════╝
    • Autor: {AUTHOR}
    • Última actualización: {UPDATE_DATE}
    • Zona horaria: America/Argentina/Buenos_Aires
"""
    print(banner)
    log_mensaje("Trading Assistant iniciado", nivel='info')

# =============================================================================
# Estado Global y Clientes
# =============================================================================

# Cliente Telegram
client = None
CANAL_VIP = None
SESSION_NAME = 'trading_session'

# Estado de órdenes
ordenes_pendientes = {}
senales_activas = {}
mensajes_senales = {}
senales_canceladas = {}

# =============================================================================
# Sistema de Logging
# =============================================================================

def get_log_paths():
    """
    Retorna paths de logs organizados por mes con soporte para backups.
    
    Returns:
        dict: Diccionario con paths para diferentes tipos de logs:
            - procesados: Log de mensajes procesados
            - diario: Log de operaciones diarias
            - acciones: Log de acciones ejecutadas
            - backup: Directorio para backups
    """
    fecha_actual = datetime.now(timezone).strftime("%Y%m")
    
    paths = {
        'procesados': os.path.join(LOGS_DIR, f'procesados_{fecha_actual}.json'),
        'diario': os.path.join(LOGS_DIR, f'diario_{fecha_actual}.json'),
        'acciones': os.path.join(LOGS_DIR, f'acciones_{fecha_actual}.jsonl'),
        'backup': os.path.join(LOGS_DIR, 'backup'),
        'errores': os.path.join(LOGS_DIR, 'errors.log'),
        'trading': os.path.join(LOGS_DIR, 'trading_assistant.log')
    }
    
    # Crear directorios necesarios
    for path in paths.values():
        if path.endswith(('/', '\\')): # Si es un directorio
            os.makedirs(path, exist_ok=True)
        else: # Si es un archivo
            os.makedirs(os.path.dirname(path), exist_ok=True)
    
    return paths

def init_log_diario():
    """
    Inicializa o carga el log diario con estadísticas.
    
    Returns:
        dict: Estructura de log mejorada con estadísticas
    """
    paths = get_log_paths()
    if os.path.exists(paths['diario']):
        with open(paths['diario'], "r") as f:
            return json.load(f)
    
    # Crear estructura base
    log_base = {
        "estadisticas": {
            "total_operaciones": 0,
            "operaciones_activas": 0,
            "take_profits_alcanzados": 0,
            "stop_loss_alcanzados": 0,
            "win_rate": 0.0,
            "mejor_operacion": None,
            "peor_operacion": None,
            "trades_ganadores": 0,
            "trades_perdedores": 0
        },
        "operaciones": {
            "entrada": [],  # Changed from "entradas"
            "cierre": [],   # Changed from "cierres"
            "be": [],
            "tp": [],       # Changed from "take_profits"
            "sl": [],       # Changed from "perdidas"
            "cancelacion": [] # Changed from "canceladas"
        },
        "resumen_diario": {
            "fecha": datetime.now(timezone).strftime('%Y-%m-%d'),
            "balance_inicial": 10000,  # Balance inicial demo
            "balance_actual": 10000,
            "profit_loss_dia": 0,
            "mejor_trade_dia": None,
            "peor_trade_dia": None,
            "total_trades_dia": 0,
            "trades_ganadores": 0,
            "trades_perdedores": 0,
            "win_rate_dia": 0.0,
            "profit_factor": 0.0,
            "drawdown_maximo": 0.0
        }
    }
    
    # Crear directorios si no existen
    os.makedirs(os.path.dirname(paths['diario']), exist_ok=True)
    os.makedirs(os.path.dirname(paths['acciones']), exist_ok=True)
    os.makedirs(os.path.dirname(paths['procesados']), exist_ok=True)
    
    # Guardar estructura inicial
    with open(paths['diario'], 'w') as f:
        json.dump(log_base, f, indent=4, sort_keys=True)
    
    return log_base

def actualizar_estadisticas(tipo_accion, data, profit=None):
    """
    Actualiza las estadísticas del log diario con manejo de errores mejorado.
    
    Args:
        tipo_accion: Tipo de acción ('tp', 'sl', 'entrada', etc.)
        data: Datos completos de la acción incluyendo detalles de mercado
        profit: Ganancia/pérdida de la operación (opcional)
    """
    try:
        global log_diario
        stats = log_diario["estadisticas"]
        resumen = log_diario["resumen_diario"]
        
        # Asegurar que existan todos los campos necesarios
        if "drawdown_maximo" not in stats:
            stats["drawdown_maximo"] = 0.0
        if "drawdown_maximo" not in resumen:
            resumen["drawdown_maximo"] = 0.0
        
        # Actualizar estadísticas según tipo de acción
        if tipo_accion == "entrada":
            stats["total_operaciones"] = stats.get("total_operaciones", 0) + 1
            stats["operaciones_activas"] = stats.get("operaciones_activas", 0) + 1
        
        elif tipo_accion == "tp":
            stats["take_profits_alcanzados"] = stats.get("take_profits_alcanzados", 0) + 1
            stats["operaciones_activas"] = max(0, stats.get("operaciones_activas", 1) - 1)
            
            # Actualizar win rate
            total_cerradas = stats.get("take_profits_alcanzados", 0) + stats.get("stop_loss_alcanzados", 0)
            if total_cerradas > 0:
                stats["win_rate"] = (stats["take_profits_alcanzados"] / total_cerradas) * 100
                
            # Actualizar mejor operación
            if profit is not None:
                mejor_profit = stats.get("mejor_operacion", {}).get("profit", float('-inf'))
                if not stats.get("mejor_operacion") or profit > mejor_profit:
                    stats["mejor_operacion"] = {**data, "profit": profit}
        
        elif tipo_accion == "sl":
            stats["stop_loss_alcanzados"] = stats.get("stop_loss_alcanzados", 0) + 1
            stats["operaciones_activas"] = max(0, stats.get("operaciones_activas", 1) - 1)
            
            # Actualizar win rate
            total_cerradas = stats.get("take_profits_alcanzados", 0) + stats.get("stop_loss_alcanzados", 0)
            if total_cerradas > 0:
                stats["win_rate"] = (stats["take_profits_alcanzados"] / total_cerradas) * 100
                
            # Actualizar peor operación
            if profit is not None:
                peor_loss = stats.get("peor_operacion", {}).get("loss", float('inf'))
                if not stats.get("peor_operacion") or profit < peor_loss:
                    stats["peor_operacion"] = {**data, "loss": profit}
        
        # Actualizar resumen diario si hay profit/loss
        if profit is not None:
            resumen["balance_actual"] = resumen.get("balance_actual", 0) + profit
            resumen["profit_loss_dia"] = resumen.get("profit_loss_dia", 0) + profit
            
            if profit > 0:
                resumen["trades_ganadores"] = resumen.get("trades_ganadores", 0) + 1
            else:
                resumen["trades_perdedores"] = resumen.get("trades_perdedores", 0) + 1
                
            resumen["total_trades_dia"] = resumen["trades_ganadores"] + resumen["trades_perdedores"]
            
            if resumen["total_trades_dia"] > 0:
                resumen["win_rate_dia"] = (resumen["trades_ganadores"] / resumen["total_trades_dia"]) * 100
                
            # Actualizar drawdown máximo
            drawdown = resumen["balance_inicial"] - resumen["balance_actual"]
            if drawdown > resumen["drawdown_maximo"]:
                resumen["drawdown_maximo"] = drawdown
                
            # Actualizar profit factor
            if resumen["trades_perdedores"] > 0:
                resumen["profit_factor"] = abs(resumen["trades_ganadores"] / resumen["trades_perdedores"])
        
        # Guardar estadísticas actualizadas
        try:
            paths = get_log_paths()
            with open(paths['diario'], "w", encoding='utf-8') as f:
                json.dump(log_diario, f, indent=4, sort_keys=True, ensure_ascii=False)
        except Exception as e:
            log_mensaje(f"Error guardando estadísticas: {e}", nivel='error', exc_info=True)
            # Intentar guardar en archivo de respaldo
            try:
                backup_file = os.path.join(LOGS_DIR, 'estadisticas_backup.json')
                with open(backup_file, "w", encoding='utf-8') as f:
                    json.dump(log_diario, f, indent=4, sort_keys=True, ensure_ascii=False)
            except:
                pass
                
    except Exception as e:
        log_mensaje(f"Error crítico actualizando estadísticas: {e}", nivel='critical', exc_info=True)

def log_mensaje(mensaje, nivel='info', mostrar=True):
    """
    Función unificada para logging y mostrar mensajes.
    Evita duplicación de mensajes.
    
    Args:
        mensaje (str): Mensaje a registrar/mostrar
        nivel (str): Nivel de log ('info', 'warning', 'error', 'debug')
        mostrar (bool): Si se debe mostrar el mensaje en consola
    """
    log_func = getattr(logger, nivel)
    log_func(mensaje)
    if mostrar and not mensaje.startswith('\n'):  # Evitar duplicar mensajes con newlines
        print(mensaje)

def guardar_logs():
    """
    Guarda todos los logs en archivos separados con formato mejorado y manejo de errores.
    """
    try:
        fecha_actual = datetime.now().strftime("%Y%m")
        
        # Preparar rutas de archivos
        paths = {
            'diario': os.path.join(LOGS_DIR, f'diario_{fecha_actual}.json'),
            'procesados': os.path.join(LOGS_DIR, f'procesados_{fecha_actual}.json'),
            'backup': os.path.join(LOGS_DIR, 'backup')
        }
        
        # Crear directorio de backup si no existe
        os.makedirs(paths['backup'], exist_ok=True)
        
        # Función auxiliar para guardar archivo con backup
        def guardar_archivo_seguro(ruta, datos):
            try:
                # Si el archivo existe y excede el tamaño máximo, hacer backup
                if os.path.exists(ruta) and os.path.getsize(ruta) > MAX_LOG_SIZE:
                    backup_name = f"{os.path.basename(ruta)}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
                    backup_path = os.path.join(paths['backup'], backup_name)
                    os.rename(ruta, backup_path)
                
                # Guardar nuevo archivo
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, sort_keys=True, ensure_ascii=False)
                
                return True
            except Exception as e:
                log_mensaje(f"Error guardando {ruta}: {e}", nivel='error', exc_info=True)
                try:
                    # Intentar guardar en archivo de respaldo
                    backup_path = f"{ruta}.backup"
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        json.dump(datos, f, indent=4, sort_keys=True, ensure_ascii=False)
                    log_mensaje(f"Datos guardados en backup: {backup_path}", nivel='warning')
                except Exception as backup_error:
                    log_mensaje(f"Error guardando backup: {backup_error}", nivel='critical', exc_info=True)
                return False
        
        # Guardar estadísticas y resumen diario
        datos_diario = {
            "estadisticas": log_diario.get('estadisticas', {}),
            "resumen_diario": log_diario.get('resumen_diario', {})
        }
        guardar_archivo_seguro(paths['diario'], datos_diario)
        
        # Guardar operaciones
        datos_operaciones = {
            "activas": log_diario.get('operaciones', {}).get('entrada', []),
            "cerradas": {
                "take_profits": log_diario.get('operaciones', {}).get('tp', []),
                "perdidas": log_diario.get('operaciones', {}).get('sl', []),
                "break_even": log_diario.get('operaciones', {}).get('be', [])
            },
            "canceladas": log_diario.get('operaciones', {}).get('cancelacion', [])
        }
        guardar_archivo_seguro(paths['procesados'], datos_operaciones)
        
        # Limpiar logs antiguos (más de 30 días)
        try:
            for archivo in os.listdir(LOGS_DIR):
                if archivo.endswith('.json') or archivo.endswith('.jsonl'):
                    ruta_archivo = os.path.join(LOGS_DIR, archivo)
                    tiempo_archivo = datetime.fromtimestamp(os.path.getctime(ruta_archivo))
                    if (datetime.now() - tiempo_archivo).days > 30:
                        backup_path = os.path.join(paths['backup'], f"old_{archivo}")
                        os.rename(ruta_archivo, backup_path)
        except Exception as e:
            log_mensaje(f"Error limpiando logs antiguos: {e}", nivel='warning')
            
    except Exception as e:
        log_mensaje(f"Error crítico guardando logs: {e}", nivel='critical', exc_info=True)

def log_accion(tipo, accion, senal_original, detalles=None):
    """
    Registra una acción en el log con manejo de errores mejorado y formato optimizado.
    
    Args:
        tipo (str): Tipo de acción ('entrada', 'actualizacion', 'cancelacion', etc.)
        accion (str): Acción específica ('hit_entry', 'be', 'cerrar', etc.)
        senal_original (str): Texto de la señal original que generó la acción
        detalles (dict, optional): Información adicional sobre la acción
    
    Returns:
        dict: Datos de la acción registrada
    """
    try:
        timestamp = get_timestamp()
        
        # Crear estructura base del log
        data = {
            "tipo": tipo,
            "accion": accion,
            "timestamp": timestamp,
            "senal_original": senal_original,
            "detalles": detalles or {}
        }
        
        # Añadir información de mercado si está disponible
        if detalles and "simbolo" in detalles:
            data["mercado"] = {
                "simbolo": detalles["simbolo"],
                "tipo_orden": detalles.get("tipo", ""),
                "precio_entrada": detalles.get("entrada"),
                "precio_salida": detalles.get("precio_salida"),
                "sl": detalles.get("sl"),
                "tp": detalles.get("tp"),
                "ticket": detalles.get("ticket")
            }
        
        # Actualizar estadísticas según el tipo de acción
        try:
            if tipo == "entrada":
                actualizar_estadisticas("entrada", data)
            elif accion.startswith("tp"):
                actualizar_estadisticas("tp", data, profit=detalles.get("profit", 0))
            elif accion in ["hit risk", "stop hit", "sl hit"]:
                actualizar_estadisticas("sl", data, profit=detalles.get("loss", 0))
        except Exception as e:
            log_mensaje(f"Error actualizando estadísticas: {e}", nivel='error', exc_info=True)
        
        # Actualizar operaciones en el log diario de forma segura
        try:
            if tipo in log_diario["operaciones"]:
                log_diario["operaciones"][tipo].append(data)
        except Exception as e:
            log_mensaje(f"Error actualizando log diario: {e}", nivel='error', exc_info=True)
        
        # Guardar acción en el log de acciones con rotación
        try:
            log_file = os.path.join(LOGS_DIR, f'acciones_{datetime.now().strftime("%Y%m")}.jsonl')
            
            # Rotar archivo si excede el tamaño máximo
            if os.path.exists(log_file) and os.path.getsize(log_file) > MAX_LOG_SIZE:
                backup_file = f"{log_file}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
                os.rename(log_file, backup_file)
            
            # Guardar la acción en formato JSONL
            with open(log_file, "a", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
                f.write("\n")
            
            # Actualizar logs consolidados
            guardar_logs()
            
        except Exception as e:
            log_mensaje(f"Error guardando log de acciones: {e}", nivel='error', exc_info=True)
            # Intentar guardar en archivo de respaldo
            try:
                backup_file = os.path.join(LOGS_DIR, 'acciones_backup.jsonl')
                with open(backup_file, "a", encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                    f.write("\n")
            except:
                pass
        
        return data
        
    except Exception as e:
        log_mensaje(f"Error crítico en log_accion: {e}", nivel='critical', exc_info=True)
        return None


def setup_logging():
    """
    Configura el sistema de logging con rotación de archivos y manejo de errores mejorado.
    """
    return init_logging()

def init_log_diario():
    """
    Inicializa o carga el log diario con estadísticas.
    
    Returns:
        dict: Estructura de log mejorada con estadísticas
    """
    global log_diario
    
    # Estructura base del log
    log_diario = {
        "estadisticas": {
            "total_operaciones": 0,
            "operaciones_activas": 0,
            "take_profits_alcanzados": 0,
            "stop_loss_alcanzados": 0,
            "win_rate": 0.0,
            "mejor_operacion": None,
            "peor_operacion": None,
            "trades_ganadores": 0,
            "trades_perdedores": 0
        },
        "operaciones": {
            "entrada": [],
            "cierre": [],
            "be": [],
            "tp": [],
            "sl": [],
            "cancelacion": []
        },
        "resumen_diario": {
            "fecha": datetime.now(timezone).strftime('%Y-%m-%d'),
            "balance_inicial": 10000,
            "balance_actual": 10000,
            "profit_loss_dia": 0,
            "mejor_trade_dia": None,
            "peor_trade_dia": None,
            "total_trades_dia": 0,
            "trades_ganadores": 0,
            "trades_perdedores": 0,
            "win_rate_dia": 0.0,
            "profit_factor": 0.0,
            "drawdown_maximo": 0.0
        }
    }
    
    paths = get_log_paths()
    if os.path.exists(paths['diario']):
        with open(paths['diario'], "r") as f:
            log_diario.update(json.load(f))
    else:
        # Crear directorios si no existen
        os.makedirs(os.path.dirname(paths['diario']), exist_ok=True)
        os.makedirs(os.path.dirname(paths['acciones']), exist_ok=True)
        os.makedirs(os.path.dirname(paths['procesados']), exist_ok=True)
        
        # Guardar estructura inicial
        with open(paths['diario'], 'w') as f:
            json.dump(log_diario, f, indent=4, sort_keys=True)
    
    return log_diario

# =============================================================================
# Funciones de Utilidad
# =============================================================================

def print_banner():
    banner = f"""
{'=' * 50}

╔══════════════════════════════════════╗
║     🤖 Trading Assistant v{VERSION}     ║
║        Telegram + MT5 Bridge         ║
╚══════════════════════════════════════╝

    • Autor: {AUTHOR}
    • Última actualización: {UPDATE_DATE}
    • Zona horaria: America/Argentina/Buenos_Aires

{'=' * 50}
"""
    print(banner)
    logger.info("\n🚀 Trading Assistant iniciado\n")

# Inicializar logging y log diario después de que todas las funciones estén definidas
logger = init_logging()
log_diario = init_log_diario()

# =============================================================================
# Operaciones de Trading
# =============================================================================

async def ejecutar_orden_mercado(datos_senal, senal_original):
    """
    Ejecuta una orden a mercado en MT5.
    
    Args:
        datos_senal (dict): Datos de la orden a ejecutar:
            - simbolo: Símbolo a operar
            - tipo: Tipo de orden ('BUY' o 'SELL')
            - sl: Stop loss
            - tp: Take profit
            - entrada: Precio de entrada original
        senal_original (str): Texto de la señal que generó la orden
    
    Returns:
        int: Ticket de la orden si fue exitosa, None en caso contrario
    """
    try:
        conectar()
        
        # Execute order at current market price with original SL/TP distances
        ticket = abrir_orden(
            symbol=datos_senal['simbolo'],
            order_type=datos_senal['tipo'],
            lotes=0.1,
            sl=datos_senal['sl'],
            tp=datos_senal['tp'],
            entrada=datos_senal['entrada']  # Pass original entry price
        )
        
        if ticket:
            mensaje = f"✅ Orden ejecutada a mercado: {ticket}"
            logger.info(mensaje)
            print(mensaje)
            log_accion("entrada", "hit_entry", senal_original, {
                "ticket": ticket,
                "detalles": datos_senal
            })
            return ticket
        else:
            mensaje = "❌ Error ejecutando orden a mercado"
            logger.error(mensaje)
            print(mensaje)
            return None
            
    except Exception as e:
        mensaje = f"❌ Error en MT5: {e}"
        logger.error(mensaje)
        print(mensaje)
        return None
    finally:
        cerrar()

async def cerrar_orden_con_reintentos(ticket, max_intentos=3):
    """
    Intenta cerrar una orden varias veces si falla.
    
    Args:
        ticket (int): Ticket de la orden a cerrar
        max_intentos (int): Número máximo de intentos de cierre (default: 3)
    
    Returns:
        bool: True si la orden se cerró exitosamente, False en caso contrario
    """
    for intento in range(max_intentos):
        try:
            conectar()
            if cerrar_orden(ticket):
                logger.info(f"✅ Orden {ticket} cerrada correctamente en intento {intento + 1}")
                return True
            else:
                logger.error(f"❌ Intento {intento + 1}/{max_intentos}: Error al cerrar orden {ticket}")
                if intento < max_intentos - 1:
                    await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"❌ Intento {intento + 1}/{max_intentos}: Error cerrando orden {ticket}: {e}")
            if intento < max_intentos - 1:
                await asyncio.sleep(0.1)
        finally:
            cerrar()
    return False

def test_mt5():
    """
    Prueba la conexión con MetaTrader 5.
    
    Intenta establecer y cerrar una conexión con MT5 para verificar
    que el sistema está disponible y funcionando correctamente.
    
    Returns:
        bool: True si la conexión fue exitosa, False en caso contrario
    """
    try:
        conectar()
        cerrar()
        log_mensaje("✅ Conexión a MT5 exitosa.")
        return True
    except Exception as e:
        log_mensaje(f"❌ Error conectando a MT5: {e}", nivel='error')
        return False

# =============================================================================
# Handlers de Telegram
# =============================================================================

async def handler(event):
    """
    Manejador principal de eventos de Telegram.
    
    Filtra los mensajes para procesar solo los del canal VIP configurado.
    
    Args:
        event (events.NewMessage.Event): Evento de nuevo mensaje de Telegram
    """
    global CANAL_VIP
    if CANAL_VIP is None or event.chat_id != CANAL_VIP:
        return

    await procesar_mensaje(event)

def register_handlers(client):
    """
    Registra los manejadores de eventos de Telegram.
    
    Args:
        client (TelegramClient): Cliente de Telegram inicializado
    """
    client.on(events.NewMessage())(handler)

async def procesar_mensaje(event):
    """
    Procesa un mensaje de Telegram para detectar señales y acciones.
    
    Analiza el contenido del mensaje para:
    1. Detectar nuevas señales de trading
    2. Detectar acciones sobre señales existentes
    3. Ejecutar las acciones correspondientes
    4. Manejar señales canceladas para re-entrada
    
    Args:
        event (events.NewMessage.Event): Evento de mensaje a procesar
    """
    msg = event.message
    texto = getattr(msg, 'text', None) or getattr(msg, 'message', None) or getattr(msg, 'caption', None)
    if not texto:
        return

    texto = texto.strip()
    resultado = parse_senal(texto)

    if resultado:
        mensaje = f"\n══════════════════════════════════════\n📡 [SEÑAL DETECTADA] ➤ {resultado}\n══════════════════════════════════════"
        logger.info(mensaje)
        print(mensaje)
        
        ordenes_pendientes[event.id] = resultado
        mensajes_senales[event.id] = texto
        
        mensaje = f"\n🔍 Esperando precio {resultado['entrada']} para {resultado['tipo']}\n"
        logger.info(mensaje)
        print(mensaje)
        
        # Registrar nueva señal en el log
        data = {
            "mensaje_id": event.id,
            "detalles": resultado
        }
        
        # Actualizar operaciones
        log_diario["operaciones"]["entrada"].append({
            "tipo": "entrada",
            "accion": "nueva_senal",
            "timestamp": get_timestamp(),
            "senal_original": texto,
            "detalles": data
        })
        
        # Guardar logs
        guardar_logs()
        return

    accion = detectar_accion_mensaje(texto)
    if not accion:
        return

    mensaje = f"\n══════════════════════════════════════\n📥 [ACCIÓN DETECTADA] ➤ {accion.upper()}\n══════════════════════════════════════"
    logger.info(mensaje)
    print(mensaje)
    
    # Buscar señal original siguiendo la cadena de respuestas
    senal_id, estado, senal_original = await encontrar_senal_original(
        msg, client, mensajes_senales, ordenes_pendientes, senales_activas, senales_canceladas
    )
    
    if not senal_id:
        mensaje = "\n❌ No se encontró la señal original\n"
        logger.warning(mensaje)
        print(mensaje)
        return
        
    mensaje = f"\n📝 Señal original encontrada ({estado}):\n{'-' * 40}\n{senal_original}\n{'-' * 40}"
    logger.info(mensaje)
    print(mensaje)

    # Manejar HIT ENTRY, BUY NOW, SELL NOW
    if accion in ["hit_entry", "buy_now", "sell_now"]:
        datos_senal = None
        if estado == "pendiente":
            datos_senal = ordenes_pendientes[senal_id]
        elif estado == "cancelada":
            datos_senal = senales_canceladas[senal_id]
        
        if datos_senal:
            # Si es BUY NOW o SELL NOW, forzar el tipo de orden
            if accion == "buy_now":
                datos_senal['tipo'] = 'BUY'
            elif accion == "sell_now":
                datos_senal['tipo'] = 'SELL'
                
            # Ejecutar orden inmediatamente a mercado
            ticket = await ejecutar_orden_mercado(datos_senal, senal_original)
            if ticket:
                senales_activas[senal_id] = {**datos_senal, 'ticket': ticket}
                
                # Remove from appropriate dictionary
                if estado == "pendiente":
                    del ordenes_pendientes[senal_id]
                elif estado == "cancelada":
                    del senales_canceladas[senal_id]
                    
                mensaje = f"\n✅ Orden ejecutada inmediatamente a mercado (acción: {accion})\n"
                logger.info(mensaje)
                print(mensaje)
                
                # Log the action
                log_accion("entrada", accion, senal_original, {
                    "ticket": ticket,
                    "detalles": datos_senal,
                    "tipo_ejecucion": "mercado"
                })
            else:
                mensaje = f"\n❌ Error al ejecutar la orden a mercado (acción: {accion})\n"
                logger.error(mensaje)
                print(mensaje)
        else:
            mensaje = f"\n❌ No se puede ejecutar {accion.upper()} en señal {estado}\n"
            logger.warning(mensaje)
            print(mensaje)
        return

    # Manejar ROUND
    if accion == "round":
        # Buscar la señal original en la cadena de respuestas
        senal_id_original = senal_id
        senal_encontrada = False
        
        # Primero buscar en el mensaje actual
        if senal_id in ordenes_pendientes or senal_id in senales_activas or senal_id in senales_canceladas:
            senal_id_original = senal_id
            senal_encontrada = True
        
        # Si no se encuentra, buscar en la cadena de respuestas
        if not senal_encontrada:
            while True:
                msg = await client.get_messages(event.chat_id, ids=senal_id_original)
                if not msg or not msg.reply_to_msg_id:
                    break
                senal_id_original = msg.reply_to_msg_id
                
                # Verificar si encontramos la señal original
                if (senal_id_original in ordenes_pendientes or 
                    senal_id_original in senales_activas or 
                    senal_id_original in senales_canceladas):
                    senal_id = senal_id_original
                    senal_encontrada = True
                    break

        # Obtener los datos de la señal según su estado
        datos_senal = None
        estado_senal = None
        
        # Intentar obtener la señal de cualquier estado
        if senal_id in ordenes_pendientes:
            datos_senal = ordenes_pendientes[senal_id]
            estado_senal = "pendiente"
        elif senal_id in senales_canceladas:
            datos_senal = senales_canceladas[senal_id]
            estado_senal = "cancelada"
        elif senal_id in senales_activas:
            datos_senal = senales_activas[senal_id]
            estado_senal = "activa"
        
        if datos_senal:
            mensaje = f"\n🔄 Reactivando señal {senal_id} (estado anterior: {estado_senal})"
            logger.info(mensaje)
            print(mensaje)
            
            # Mover la señal a ordenes_pendientes
            ordenes_pendientes[senal_id] = datos_senal
            
            # Eliminar de su estado anterior
            if estado_senal == "cancelada":
                del senales_canceladas[senal_id]
            elif estado_senal == "activa":
                del senales_activas[senal_id]
            
            mensaje = f"\n✅ Señal reactivada exitosamente\n"
            logger.info(mensaje)
            print(mensaje)
            
            # Log the action
            log_accion("reactivacion", "round", senal_original, {
                "senal_id": senal_id,
                "estado_anterior": estado_senal,
                "detalles": datos_senal
            })
            
            await listar_senales()
        else:
            mensaje = f"\n❌ No se encontró la señal original para reactivar\n"
            logger.warning(mensaje)
            print(mensaje)
        return

    # Manejar acciones de cancelación y pérdida
    if accion in ["cancel", "hit risk", "perdida"]:
        # Buscar la señal original en la cadena de respuestas
        senal_id_original = senal_id
        while True:
            msg = await client.get_messages(event.chat_id, ids=senal_id_original)
            if not msg or not msg.reply_to_msg_id:
                break
            senal_id_original = msg.reply_to_msg_id
            
            # Verificar si encontramos la señal original
            if senal_id_original in ordenes_pendientes or senal_id_original in senales_activas:
                senal_id = senal_id_original
                break
        
        if senal_id in ordenes_pendientes:
            # Guardar la señal cancelada antes de eliminarla
            senales_canceladas[senal_id] = ordenes_pendientes[senal_id]
            del ordenes_pendientes[senal_id]
            mensaje = f"\n✅ Orden pendiente {senal_id} cancelada\n"
            logger.info(mensaje)
            print(mensaje)
            log_accion("cancelacion", accion, senal_original, {
                "referencia": senal_id,
                "motivo": accion
            })
            return

        if senal_id in senales_activas:
            # Guardar la señal cancelada antes de eliminarla
            senales_canceladas[senal_id] = senales_activas[senal_id]
            original = senales_activas.pop(senal_id)
            ticket = original.get("ticket")
            if ticket:
                exito = await cerrar_orden_con_reintentos(ticket)
                mensaje = "✅ Orden cerrada exitosamente" if exito else "❌ Error al cerrar la orden"
                logger.info(mensaje) if exito else logger.error(mensaje)
                print(mensaje)

            log_accion("cancelacion", accion, senal_original, {
                "referencia": senal_id,
                "motivo": accion,
                "detalles_orden": original
            })
            await listar_senales()
            return

    if accion and accion.startswith("tp"):
        mensaje = "✅ Take profit registrado"
        logger.info(mensaje)
        print(mensaje)
        log_accion("tp", accion, senal_original, {
            "mensaje": texto
        })
        return

    # Manejar acciones de cerrar y break even
    if accion in ["cerrar", "be"]:
        # Buscar la señal original en la cadena de respuestas
        senal_id_original = senal_id
        while True:
            msg = await client.get_messages(event.chat_id, ids=senal_id_original)
            if not msg or not msg.reply_to_msg_id:
                break
            senal_id_original = msg.reply_to_msg_id
            
            # Verificar si encontramos la señal original
            if senal_id_original in senales_activas:
                senal_id = senal_id_original
                break

        if senal_id in senales_activas:
            original = senales_activas[senal_id]
            ticket = original.get("ticket")
            if not ticket:
                mensaje = "❌ No se encontró ticket"
                logger.error(mensaje)
                print(mensaje)
                return
                
            try:
                if accion == "cerrar":
                    exito = await cerrar_orden_con_reintentos(ticket)
                    if exito:
                        mensaje = "\n✅ Orden cerrada exitosamente\n"
                        logger.info(mensaje)
                        print(mensaje)
                        del senales_activas[senal_id]
                else:  # be
                    conectar()
                    exito = mover_sl_be(ticket)
                    cerrar()
                    if exito:
                        mensaje = "✅ Break even ejecutado exitosamente"
                        logger.info(mensaje)
                        print(mensaje)
                    
                if not exito:
                    mensaje = "❌ Error al ejecutar la acción"
                    logger.error(mensaje)
                    print(mensaje)
                    
            except Exception as e:
                mensaje = f"❌ Error en MT5: {e}"
                logger.error(mensaje)
                print(mensaje)

            log_accion("actualizacion", accion, senal_original, {
                "referencia": senal_id,
                "detalles_orden": original
            })
            await listar_senales()
            return

    if accion == "list":
        await listar_senales()
        return

    if accion == "perdida":
        log_accion("perdida", accion, senal_original, {
            "mensaje": texto
        })
        await listar_senales()
        return

# =============================================================================
# Gestión de Canales
# =============================================================================

async def listar_y_elegir_canal():
    """
    Muestra y permite seleccionar un canal de Telegram.
    
    Lista todos los canales disponibles y permite al usuario
    seleccionar uno para monitorear señales.
    
    Returns:
        int: ID del canal seleccionado, None si no se seleccionó ninguno
    """
    log_mensaje("🔍 Buscando canales y supergrupos...")
    
    dialogs = await client.get_dialogs()
    canales = [d for d in dialogs if d.is_channel]
    if not canales:
        log_mensaje("⚠️ No se encontraron canales.", nivel='warning')
        return None

    # Print channel list without logging
    print("\n📋 Canales encontrados:")
    for i, canal in enumerate(canales, 1):
        print(f"{i}. {canal.title} (ID: {canal.id})")

    while True:
        opcion = input("\nElegí el número del canal: ").strip()
        try:
            i = int(opcion)
            if 1 <= i <= len(canales):
                seleccionado = canales[i - 1]
                log_mensaje(f"✅ Canal seleccionado: {seleccionado.title}")
                return seleccionado.id
        except ValueError:
            log_mensaje("❌ Entrada inválida.", nivel='warning')

async def imprimir_ultimo_mensaje_y_procesar(canal_id):
    """
    Muestra y procesa el último mensaje del canal seleccionado.
    
    Obtiene el último mensaje del canal y lo procesa como si fuera
    un mensaje nuevo para mantener el estado actualizado.
    
    Args:
        canal_id (int): ID del canal de Telegram a procesar
    """
    mensajes = await client.get_messages(canal_id, limit=1)
    if mensajes:
        ultimo = mensajes[0]
        texto = getattr(ultimo, 'text', None) or getattr(ultimo, 'message', None) or "<Mensaje multimedia>"
        log_mensaje(f"\n📢 Último mensaje del canal:\nFecha: {ultimo.date}\nMensaje: {texto}\n")

        class EventoSimulado:
            def __init__(self, message):
                self.message = message
                self.id = message.id
                self.chat_id = canal_id

        evento_simulado = EventoSimulado(ultimo)
        await procesar_mensaje(evento_simulado)
    else:
        log_mensaje("\n⚠️ No hay mensajes todavía.\n", nivel='warning')

# Variable global para el canal VIP
CANAL_VIP = None

# =============================================================================
# Funciones Principales
# =============================================================================

async def listar_senales():
    """
    Lista todas las señales activas y pendientes.
    
    Muestra un resumen del estado actual del sistema:
    - Órdenes pendientes de ejecución
    - Órdenes activas en el mercado
    - Detalles de cada orden (ID, señal original, ticket MT5)
    
    El listado se muestra tanto en consola como en el log.
    """
    mensaje = f"\n{'=' * 50}\n📊 ESTADO DE SEÑALES ({get_timestamp()})\n{'=' * 50}"
    logger.info(mensaje)
    print(mensaje)
    
    if ordenes_pendientes:
        mensaje = "\n📍 ÓRDENES PENDIENTES:\n{'-' * 30}"
        logger.info(mensaje)
        print(mensaje)
        for msg_id, datos in ordenes_pendientes.items():
            senal = mensajes_senales.get(msg_id, "Señal sin detalle")
            detalle = f"\nID: {msg_id}\n{'-' * 20}\nSeñal:\n{senal}\n{'-' * 20}\nDetalles:\n{json.dumps(datos, indent=2)}\n"
            logger.info(detalle)
            print(detalle)
    
    if senales_activas:
        mensaje = "\n🎯 ÓRDENES ACTIVAS:\n{'-' * 30}"
        logger.info(mensaje)
        print(mensaje)
        for msg_id, datos in senales_activas.items():
            senal = mensajes_senales.get(msg_id, "Señal sin detalle")
            detalle = f"\nID: {msg_id}\n{'-' * 20}\nSeñal:\n{senal}\n{'-' * 20}\nTicket: {datos.get('ticket')}\nDetalles:\n{json.dumps(datos, indent=2)}\n"
            logger.info(detalle)
            print(detalle)
    
    if not ordenes_pendientes and not senales_activas:
        mensaje = "\n📭 No hay señales activas ni pendientes\n"
        logger.info(mensaje)
        print(mensaje)
    
    print('=' * 50)

class MonitorTask:
    """
    Gestiona el monitoreo de precios y ejecución de órdenes pendientes.
    
    Attributes:
        running (bool): Indica si el monitor está activo
        task (asyncio.Task): Tarea asíncrona del monitor
        interval (int): Intervalo en segundos entre mensajes de estado
        last_check (float): Timestamp del último chequeo
    """
    
    def __init__(self, interval=300):  # Changed from 20 to 300 seconds (5 minutes)
        """
        Inicializa el monitor de precios.
        
        Args:
            interval (int): Intervalo en segundos entre mensajes de estado (default: 300)
        """
        self.running = True
        self.task = None
        self.interval = interval
        self.last_check = 0
        self.silent_mode = False  # New flag to control message visibility

    async def start(self):
        """
        Inicia la tarea de monitoreo.
        Crea una nueva tarea asíncrona para ejecutar el monitor.
        """
        self.task = asyncio.create_task(self.run())
        mensaje = "\n✅ Monitor de precios iniciado\n"
        logger.info(mensaje)
        print(mensaje)

    async def stop(self):
        """
        Detiene la tarea de monitoreo.
        Cancela la tarea asíncrona y espera a que termine.
        """
        if self.task:
            self.running = False
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                mensaje = "✅ Monitor de precios detenido"
                logger.info(mensaje)
                print(mensaje)

    async def check_prices(self):
        """
        Verifica los precios actuales y ejecuta órdenes pendientes.
        
        Verifica cada orden pendiente y la ejecuta si se alcanza el precio objetivo.
        Maneja la conexión a MT5 y el logging de eventos.
        """
        current_time = time.time()
        if current_time - self.last_check >= self.interval and not self.silent_mode:
            mensaje = f"\n{'=' * 50}\n⏰ {get_timestamp()}\nMonitor activo, verificando {len(ordenes_pendientes)} órdenes pendientes...\n{'=' * 50}"
            logger.info(mensaje)
            print(mensaje)
            self.last_check = current_time

        if ordenes_pendientes:
            try:
                conectar()
                for msg_id, datos in list(ordenes_pendientes.items()):
                    try:
                        symbol = datos['simbolo']
                        # En modo mock, simulamos el precio actual
                        precio_actual = datos['entrada']  # Para testing

                        if datos['tipo'] == 'SELL' and precio_actual >= datos['entrada']:
                            log_mensaje(f"🎯 Precio alcanzado para SELL: {precio_actual} >= {datos['entrada']}")
                            ticket = abrir_orden(
                                symbol=datos['simbolo'],
                                order_type='SELL',
                                lotes=0.1,
                                sl=datos.get('sl'),
                                tp=datos.get('tp')
                            )
                            if ticket:
                                log_mensaje(f"✅ Orden ejecutada en precio objetivo: {datos['entrada']}")
                                senales_activas[msg_id] = {**datos, 'ticket': ticket}
                                del ordenes_pendientes[msg_id]

                        elif datos['tipo'] == 'BUY' and precio_actual <= datos['entrada']:
                            log_mensaje(f"🎯 Precio alcanzado para BUY: {precio_actual} <= {datos['entrada']}")
                            ticket = abrir_orden(
                                symbol=datos['simbolo'],
                                order_type='BUY',
                                lotes=0.1,
                                sl=datos.get('sl'),
                                tp=datos.get('tp')
                            )
                            if ticket:
                                mensaje = f"✅ Orden ejecutada en precio objetivo: {datos['entrada']}"
                                logger.info(mensaje)
                                print(mensaje)
                                senales_activas[msg_id] = {**datos, 'ticket': ticket}
                                del ordenes_pendientes[msg_id]

                    except Exception as e:
                        log_mensaje(f"Error procesando orden {msg_id}: {e}", nivel='error')
            except Exception as e:
                log_mensaje(f"Error en MT5: {e}", nivel='error')
            finally:
                cerrar()

    async def run(self):
        """
        Ejecuta el bucle principal de monitoreo.
        
        Ejecuta check_prices() continuamente mientras el monitor esté activo.
        Maneja errores y reintentos automáticamente.
        """
        while self.running:
            try:
                await self.check_prices()
                await asyncio.sleep(1)  # Esperar 1 segundo entre verificaciones
            except asyncio.CancelledError:
                break
            except Exception as e:
                if self.running:
                    mensaje = f"❌ Error en monitor de precios: {e}"
                    logger.error(mensaje)
                    print(mensaje)
                    await asyncio.sleep(5)  # Esperar antes de reintentar

# =============================================================================
# Inicialización y Cleanup
# =============================================================================

async def cleanup(monitor=None):
    """
    Limpia recursos y cierra conexiones.
    
    Realiza una limpieza ordenada de los recursos del sistema:
    1. Detiene el monitor de precios si está activo
    2. Cierra la conexión con MT5
    3. Cierra la conexión con Telegram
    4. Cancela todas las tareas pendientes
    
    Args:
        monitor (MonitorTask, optional): Instancia del monitor de precios a detener
    """
    log_mensaje(f"\n{'=' * 50}\n🔄 CERRANDO CONEXIONES...\n{'=' * 50}")
    
    # Cancelar todas las tareas pendientes excepto la actual
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                log_mensaje(f"\n❌ ERROR CANCELANDO TAREA:\n{'-' * 30}\n{str(e)}\n{'-' * 30}", nivel='error')
    
    if monitor:
        try:
            await monitor.stop()
            log_mensaje("\n✅ Monitor detenido correctamente\n")
        except Exception as e:
            log_mensaje(f"❌ Error deteniendo monitor: {e}", nivel='error')
    try:
        # Cerrar MT5
        cerrar()
        log_mensaje("✅ Conexión MT5 cerrada")
    except Exception as e:
        log_mensaje(f"❌ Error cerrando MT5: {e}", nivel='error')
    
    try:
        # Cerrar Telegram
        if client and client.is_connected():
            await client.disconnect()
            log_mensaje("✅ Conexión Telegram cerrada")
    except Exception as e:
        log_mensaje(f"❌ Error cerrando Telegram: {e}", nivel='error')
    
    log_mensaje("👋 Trading Assistant finalizado")

# =============================================================================
# Inicialización y Ejecución Principal
# =============================================================================

async def main():
    """
    Función principal del Trading Assistant.
    
    Realiza la inicialización y ejecución del sistema:
    1. Muestra el banner de inicio
    2. Inicializa el monitor de precios
    3. Conecta con MT5
    4. Conecta con Telegram
    5. Configura el canal de señales
    6. Ejecuta el bucle principal de eventos
    
    Maneja el cierre ordenado del sistema en caso de error o interrupción.
    """
    global client
    
    print_banner()
    
    log_mensaje(f"\n{'=' * 50}\n🔌 Iniciando servicios...\n⏰ Hora actual: {get_timestamp()}\n{'=' * 50}")
    
    # Crear monitor de precios
    monitor = MonitorTask()
    
    if not test_mt5():
        log_mensaje("🚫 Terminando por error de MT5.", nivel='error')
        await cleanup(monitor)
        return

    try:
        # Inicializar cliente Telegram con cuenta personal
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        await client.start()
        
        # Registrar manejadores de eventos
        register_handlers(client)
        
        me = await client.get_me()
        log_mensaje(f"✅ Telegram conectado como {me.first_name} (@{me.username})")

        global CANAL_VIP
        CANAL_VIP = await listar_y_elegir_canal()
        if CANAL_VIP is None:
            log_mensaje("❌ No se eligió canal. Terminando.", nivel='error')
            await cleanup(monitor)
            return

        # Iniciar monitor después de configurar todo
        await monitor.start()
        
        await imprimir_ultimo_mensaje_y_procesar(CANAL_VIP)

        log_mensaje(f"📡 Escuchando mensajes del canal ID: {CANAL_VIP}")
        
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        log_mensaje("\n⚠️ Interrupción detectada, cerrando...", nivel='warning')
    except Exception as e:
        log_mensaje(f"❌ Error general: {e}", nivel='error')
    finally:
        await cleanup(monitor)


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == '__main__':
    """
    Punto de entrada principal del Trading Assistant.
    Inicia el sistema y maneja la interrupción por teclado.
    """
    asyncio.run(main())
