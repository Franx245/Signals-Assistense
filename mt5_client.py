"""
Cliente MetaTrader 5 para Trading Automatizado
=========================================

Este módulo proporciona una interfaz simplificada para interactuar con MetaTrader 5,
facilitando la ejecución y gestión de operaciones de trading.

Características Principales
-------------------------
1. Conexión y autenticación con MT5
2. Apertura y cierre de órdenes
3. Gestión de Stop Loss y Take Profit
4. Movimiento de Stop Loss a Break Even

Componentes del Sistema
---------------------

1. Conexión a MT5 (conectar)
   Establece la conexión con MetaTrader 5 y configura los símbolos de trading.

   Proceso de Conexión:
   ```python
   1. Cierra cualquier instancia existente
   2. Inicializa MT5
   3. Realiza login con credenciales
   4. Selecciona símbolos de trading
   ```

   Ejemplo de Uso:
   ```python
   try:
       conectar()
       print("Conectado a MT5")
   except Exception as e:
       print(f"Error de conexión: {e}")
   finally:
       cerrar()  # Siempre cerrar la conexión
   ```

2. Apertura de Órdenes (abrir_orden)
   Ejecuta nuevas órdenes de trading con gestión de SL/TP.

   Parámetros:
   ```python
   {
       'symbol': 'EURUSD',     # Par de divisas
       'order_type': 'BUY',    # BUY o SELL
       'lotes': 0.1,          # Tamaño de la operación
       'sl': 1.0450,         # Stop Loss (opcional)
       'tp': 1.0550,         # Take Profit (opcional)
       'entrada': 1.0500     # Precio original (opcional)
   }
   ```

   Ejemplos de Uso:
   ```python
   # Orden simple de compra
   ticket = abrir_orden("EURUSD", "BUY", 0.1)

   # Orden completa con SL/TP
   ticket = abrir_orden(
       symbol="EURUSD",
       order_type="SELL",
       lotes=0.1,
       sl=1.0550,
       tp=1.0450,
       entrada=1.0500
   )
   ```

   Características Especiales:
   - Ajuste automático de SL/TP basado en distancias
   - Manejo de desviaciones de precio
   - Comentarios personalizados en órdenes

3. Cierre de Órdenes (cerrar_orden)
   Cierra posiciones existentes por número de ticket.

   Proceso:
   ```python
   1. Busca la posición por ticket
   2. Determina tipo de orden inversa
   3. Ejecuta orden de cierre
   4. Verifica resultado
   ```

   Ejemplo de Uso:
   ```python
   if cerrar_orden(ticket):
       print(f"Orden {ticket} cerrada exitosamente")
   else:
       print(f"Error al cerrar orden {ticket}")
   ```

4. Gestión de Break Even (mover_sl_be)
   Mueve el Stop Loss al punto de entrada.

   Funcionamiento:
   ```python
   1. Localiza posición por ticket
   2. Obtiene precio de entrada
   3. Modifica SL manteniendo TP
   4. Verifica modificación
   ```

   Ejemplo de Uso:
   ```python
   if mover_sl_be(ticket):
       print("Stop Loss movido a Break Even")
   else:
       print("Error moviendo Stop Loss")
   ```

Escenarios de Uso Común
---------------------

1. Entrada con Gestión de Riesgo:
   ```python
   # Conectar a MT5
   conectar()
   
   try:
       # Abrir orden con SL/TP
       ticket = abrir_orden(
           "EURUSD",
           "BUY",
           0.1,
           sl=1.0450,
           tp=1.0550
       )
       
       if ticket:
           # Esperar y mover a break even
           time.sleep(300)  # 5 minutos
           mover_sl_be(ticket)
           
   finally:
       cerrar()
   ```

2. Gestión de Múltiples Órdenes:
   ```python
   conectar()
   
   try:
       # Abrir varias órdenes
       tickets = []
       for symbol in ["EURUSD", "GBPUSD"]:
           ticket = abrir_orden(symbol, "BUY", 0.1)
           if ticket:
               tickets.append(ticket)
               
       # Cerrar todas las órdenes
       for ticket in tickets:
           cerrar_orden(ticket)
           
   finally:
       cerrar()
   ```

3. Manejo de Errores:
   ```python
   conectar()
   
   try:
       ticket = abrir_orden("EURUSD", "BUY", 0.1)
       if not ticket:
           logger.error("Error abriendo orden")
           return
           
       if not mover_sl_be(ticket):
           logger.warning("Error moviendo SL a BE")
           # Intentar cerrar la orden
           cerrar_orden(ticket)
           
   except Exception as e:
       logger.error(f"Error crítico: {e}")
       # Implementar recuperación
       
   finally:
       cerrar()
   ```

Notas Importantes
---------------
1. Gestión de Conexión:
   - Siempre usar try/finally para cerrar conexión
   - Verificar estado de conexión antes de operaciones
   - Manejar reconexiones automáticas

2. Gestión de Órdenes:
   - Verificar resultados de operaciones
   - Mantener registro de tickets
   - Implementar timeouts apropiados

3. Seguridad:
   - Proteger credenciales
   - Validar parámetros de entrada
   - Limitar tamaño de operaciones

4. Optimización:
   - Reutilizar conexiones cuando sea posible
   - Minimizar número de llamadas a MT5
   - Implementar caché de datos cuando apropiado

Versión: 1.0.0
Autor: Fran
Última actualización: 2024-01-01
"""
import MetaTrader5 as mt5
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MT5 Configuration
MT5_LOGIN = 123
MT5_PASSWORD = ""
MT5_SERVER = "MetaQuotes-Demo"

def conectar():
    """Initialize and connect to MT5"""
    try:
        # Shutdown any existing instance
        mt5.shutdown()
        
        # Initialize MT5
        if not mt5.initialize():
            raise Exception(f"Failed to initialize MT5: {mt5.last_error()}")
        
        # Login to MT5
        authorized = mt5.login(
            login=MT5_LOGIN,
            password=MT5_PASSWORD,
            server=MT5_SERVER
        )
        
        if not authorized:
            raise Exception(f"Failed to login to MT5: {mt5.last_error()}")
            
        # Initialize symbols we'll be trading
        symbols = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
        for symbol in symbols:
            if not mt5.symbol_select(symbol, True):
                logger.warning(f"Failed to select symbol {symbol}")
        
        logger.info("MT5 connected successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error connecting to MT5: {e}")
        mt5.shutdown()
        raise

def cerrar():
    """Shutdown MT5 connection"""
    mt5.shutdown()

def abrir_orden(symbol: str, order_type: str, lotes: float, sl: float = None, tp: float = None, entrada: float = None) -> int:
    """
    Open a new order in MT5
    Returns ticket number if successful
    
    Args:
        symbol: Trading symbol
        order_type: "BUY" or "SELL"
        lotes: Volume to trade
        sl: Stop Loss price or None
        tp: Take Profit price or None
        entrada: Original entry price (used to calculate SL/TP distances) or None
    """
    try:
        point = mt5.symbol_info(symbol).point
        current_price = mt5.symbol_info_tick(symbol).ask if order_type == "BUY" else mt5.symbol_info_tick(symbol).bid
        
        # If we have an original entry price, calculate SL/TP based on distances
        if entrada is not None and sl is not None and tp is not None:
            sl_distance = abs(sl - entrada)
            tp_distance = abs(tp - entrada)
            
            # Adjust SL and TP based on current price
            if order_type == "BUY":
                sl = current_price - sl_distance
                tp = current_price + tp_distance
            else:  # SELL
                sl = current_price + sl_distance
                tp = current_price - tp_distance
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lotes,
            "type": mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL,
            "price": current_price,
            "deviation": 0,
            "magic": 234000,
            "comment": f"{order_type} order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        if sl is not None:
            request["sl"] = sl
        if tp is not None:
            request["tp"] = tp
            
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise Exception(f"Order failed: {result.comment}")
            
        return result.order
        
    except Exception as e:
        logger.error(f"Error opening order: {str(e)}")
        return None

def cerrar_orden(ticket: int) -> bool:
    """
    Close an existing order by ticket number
    Returns True if successful
    """
    try:
        position = mt5.positions_get(ticket=ticket)
        if not position:
            logger.error(f"Position {ticket} not found")
            return False
            
        position = position[0]
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(position.symbol).bid if position.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(position.symbol).ask,
            "deviation": 20,
            "magic": 234000,
            "comment": "Close position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Failed to close position: {result.comment}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error closing position: {str(e)}")
        return False

def mover_sl_be(ticket: int) -> bool:
    """
    Move stop loss to break even for given ticket
    Returns True if successful
    """
    try:
        position = mt5.positions_get(ticket=ticket)
        if not position:
            logger.error(f"Position {ticket} not found")
            return False
            
        position = position[0]
        
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": position.symbol,
            "sl": position.price_open,  # Move SL to entry price
            "tp": position.tp  # Keep existing TP
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Failed to modify SL: {result.comment}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error moving SL to BE: {str(e)}")
        return False
