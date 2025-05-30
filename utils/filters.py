"""
Módulo de Filtros y Procesamiento de Señales
==========================================

Este módulo se encarga del procesamiento y análisis de mensajes de trading,
incluyendo la detección de señales, acciones y el seguimiento de mensajes relacionados.

Funcionalidades Principales
-------------------------
1. Parsing de señales de trading
2. Detección de acciones en mensajes
3. Seguimiento de cadenas de respuestas
4. Extracción de información adicional de trading

Componentes del Sistema
---------------------

1. Parser de Señales (parse_senal)
   Analiza y extrae información estructurada de señales de trading.

   Ejemplo de señal:
   ```
   EURUSD
   BUY ZONE 1.0500-1.0520
   SL: 1.0450
   TP: 1.0550-1.0600-1.0650
   ```

   Proceso de parsing:
   a) Extrae el símbolo (ej: EURUSD)
   b) Identifica tipo (BUY/SELL) y zona de entrada
   c) Calcula precio de entrada óptimo:
      - Para SELL: mínimo de zona + 0.5
      - Para BUY: máximo de zona - 1
   d) Extrae Stop Loss y Take Profit

   Retorna:
   ```python
   {
       'simbolo': 'EURUSD',
       'tipo': 'BUY',
       'entrada': 1.0519,  # Calculado automáticamente
       'sl': 1.0450,
       'tp': 1.0600       # Primer TP de la serie
   }
   ```

2. Detector de Acciones (detectar_accion_mensaje)
   Identifica comandos y acciones en mensajes de respuesta.

   Acciones Soportadas:
   ```
   a) Ejecución:
      - "hit entry" -> 'hit_entry'
      - "buy now" -> 'buy_now'
      - "sell now" -> 'sell_now'

   b) Gestión:
      - "close/exit" -> 'cerrar'
      - "break even" -> 'be'
      - "cancel" -> 'cancel'
      - "round" -> 'round'

   c) Resultados:
      - "tp hit" -> 'tp'
      - "sl hit" -> 'perdida'
   ```

   Ejemplos de Uso:
   ```python
   >>> detectar_accion_mensaje("Hit entry now!")
   'hit_entry'
   
   >>> detectar_accion_mensaje("Move to break even")
   'be'
   
   >>> detectar_accion_mensaje("TP1 hit")
   'tp1'
   ```

3. Buscador de Señales (encontrar_senal_original)
   Rastrea la cadena de respuestas para encontrar la señal original.

   Funcionamiento:
   ```
   Señal Original
        ↳ Respuesta 1
             ↳ Respuesta 2 (acción)
                  ↳ Respuesta 3
   ```

   Estados de Señal:
   - "pendiente": Orden esperando ejecución
   - "activa": Orden en mercado
   - "cancelada": Orden cancelada
   - "no_encontrada": No se halló la señal

   Ejemplo de Uso:
   ```python
   msg_id, estado, texto = await encontrar_senal_original(
       mensaje_actual,
       client,
       mensajes_senales,
       ordenes_pendientes,
       senales_activas,
       senales_canceladas
   )
   ```

4. Extractor de Info Adicional (extract_trade_info)
   Obtiene detalles complementarios de trading.

   Información Extraída:
   ```python
   {
       'lotes': 0.1,      # Tamaño de la operación
       'riesgo': 2.0,     # Porcentaje de riesgo
       'ronda': 1         # Número de intento/ronda
   }
   ```

   Ejemplos de Entrada:
   ```
   "Entry with lot size 0.1"
   "Risk 2% on this trade"
   "Round 2 for EURUSD"
   ```

Flujo de Procesamiento
--------------------
1. Recepción de mensaje
2. Intento de parsing como señal
3. Si no es señal, detección de acción
4. Si es acción, búsqueda de señal original
5. Extracción de información adicional

Ejemplos de Uso Completo
----------------------
1. Procesamiento de Nueva Señal:
   ```python
   texto = '''
   EURUSD
   BUY ZONE 1.0500-1.0520
   SL: 1.0450
   TP: 1.0550-1.0600
   Lot size: 0.1
   '''
   
   # Parsear señal
   senal = parse_senal(texto)
   if senal:
       info_adicional = extract_trade_info(texto)
       # Combinar información
       senal.update(info_adicional or {})
   ```

2. Procesamiento de Acción:
   ```python
   texto_respuesta = "Move to break even now"
   accion = detectar_accion_mensaje(texto_respuesta)
   if accion == 'be':
       # Buscar señal original
       id_original, estado, texto = await encontrar_senal_original(...)
   ```

Notas Importantes
---------------
- Las señales deben seguir el formato especificado
- Las acciones son case-insensitive
- El sistema maneja múltiples variantes de cada comando
- Se implementa protección contra loops infinitos
- Logging detallado para debugging

Versión: 1.0.0
Autor: Fran
Última actualización: 2024-01-01
"""

import re
import logging

logger = logging.getLogger(__name__)

def parse_senal(texto):
    """
    Extrae información de una señal de trading y devuelve:
    símbolo, tipo, entrada, sl, y solo el primer tp.
    """
    texto = texto.upper()

    # Extraer símbolo (ej: XAUUSD)
    simbolo_match = re.search(r'\b(XAUUSD|EURUSD|GBPUSD|USDJPY)\b', texto)
    simbolo = simbolo_match.group(1) if simbolo_match else "XAUUSD"

    # Extraer tipo y rango (BUY/SELL ZONE min-max)
    orden = re.search(r'\b(BUY|SELL)\b.*?ZONE\s*(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', texto)
    if not orden:
        return None

    tipo = orden.group(1)
    rango_min = float(orden.group(2))
    rango_max = float(orden.group(3))

    # Entrada modificada según tipo
    if tipo == "SELL":
        entrada = rango_min + 0.5
    else:  # BUY
        entrada = rango_max - 1

    # Extraer SL
    sl_match = re.search(r'SL[:\s]+(\d+\.?\d*)', texto)
    sl = float(sl_match.group(1)) if sl_match else None

    # Extraer TPs separados por guiones
    tp_match = re.search(r'TP[:\s]+([\d\-.]+)', texto)
    primer_tp = None
    if tp_match:
        tps = [float(x) for x in tp_match.group(1).split('-') if x]
        if tps:
            primer_tp = tps[1]

    return {
        'simbolo': simbolo,
        'tipo': tipo,
        'entrada': entrada,
        'sl': sl,
        'tp': primer_tp
    }

def detectar_accion_mensaje(texto):
    """
    Detecta el tipo de acción en el mensaje.
    Retorna: 'cerrar', 'be', 'cancel', 'hit_entry', 'round', 'tp', 'perdida', 'buy_now', 'sell_now' o None
    """
    texto = texto.lower().strip()
    
    # Primero verificar si contiene palabras que invalidan Round
    palabras_invalidas = ["don't", "dont", "sl", "tp", "vip"]
    if any(palabra in texto for palabra in palabras_invalidas) and "round" in texto:
        return None
        
    # Verificar comandos de ejecución inmediata
    if "buy now" in texto:
        return "buy_now"
    if "sell now" in texto:
        return "sell_now"
        
    # Verificar Round antes que otras acciones
    if "round" in texto or "ronda" in texto:
        return "round"
    
    # Acciones básicas con múltiples variantes
    acciones = {
        'cerrar': [
            'close', 'closing', 'closed', 'exit now', 'exit trade'
        ],
        'be': [
            'break even', 'move to be', 'move stop', 'stop to entry',
            'stop loss to entry', 'set breakeven now move', 'locked'
        ],
        'cancel': ['cancel', 'cancelar', 'cancelled'],
        'perdida': ['hit risk', 'stop hit', 'sl hit'],
        'hit_entry': [
            'hit entry', 'entry now', 'enter now', 'execute now', 
            'take entry', 'NOW:'
        ]
    }

    # Revisar acciones básicas
    for accion, palabras_clave in acciones.items():
        for palabra in palabras_clave:
            if palabra in texto:
                return accion

    # Revisar TP específicamente
    if texto.startswith('tp'):
        return texto  # Retorna el texto completo del TP

    return None

async def encontrar_senal_original(mensaje_actual, client, mensajes_senales, ordenes_pendientes, senales_activas, senales_canceladas):
    """
    Busca recursivamente la señal original siguiendo la cadena de respuestas.
    Sin límite de profundidad para asegurar encontrar la señal original.
    
    Args:
        mensaje_actual: Mensaje actual de Telegram
        client: Cliente de Telegram
        mensajes_senales: Diccionario de señales
        ordenes_pendientes: Diccionario de órdenes pendientes
        senales_activas: Diccionario de señales activas
        senales_canceladas: Diccionario de señales canceladas
    
    Returns:
        tuple: (mensaje_id, estado, texto_senal)
            mensaje_id: ID del mensaje de la señal original
            estado: Estado de la señal ("pendiente", "activa", "cancelada", "no_encontrada")
            texto_senal: Texto de la señal original
    """
    mensaje_id = getattr(mensaje_actual, 'reply_to_msg_id', None)
    chat_id = getattr(mensaje_actual, 'chat_id', None)
    visited_msgs = set()  # Para evitar loops infinitos
    depth = 0
    
    logger.info(f"🔍 Iniciando búsqueda desde mensaje {mensaje_id}")
    
    while mensaje_id and chat_id and mensaje_id not in visited_msgs:
        depth += 1
        visited_msgs.add(mensaje_id)
        logger.info(f"📍 Profundidad {depth}: Revisando mensaje {mensaje_id}")
        
        # Verificar si este mensaje_id corresponde a una señal
        if mensaje_id in ordenes_pendientes:
            logger.info(f"✅ Encontrada señal pendiente: {mensaje_id}")
            return mensaje_id, "pendiente", mensajes_senales.get(mensaje_id)
            
        if mensaje_id in senales_activas:
            logger.info(f"✅ Encontrada señal activa: {mensaje_id}")
            return mensaje_id, "activa", mensajes_senales.get(mensaje_id)
            
        if mensaje_id in senales_canceladas:
            logger.info(f"✅ Encontrada señal cancelada: {mensaje_id}")
            return mensaje_id, "cancelada", mensajes_senales.get(mensaje_id)
            
        if mensaje_id in mensajes_senales:
            logger.info(f"📝 Mensaje {mensaje_id} está en mensajes_senales")
            
        try:
            # Obtener el mensaje al que responde
            mensaje = await client.get_messages(chat_id, ids=mensaje_id)
            if mensaje and mensaje.reply_to_msg_id:
                logger.info(f"↩️ Mensaje {mensaje_id} responde a {mensaje.reply_to_msg_id}")
                mensaje_id = mensaje.reply_to_msg_id
                continue
            else:
                logger.info(f"❌ Mensaje {mensaje_id} no tiene reply_to_msg_id")
                break
        except Exception as e:
            logger.error(f"❌ Error buscando señal original en {mensaje_id}: {e}")
            break
    
    logger.info(f"🔍 Búsqueda terminada después de {depth} niveles")
    return None, "no_encontrada", None

def extract_trade_info(texto):
    """
    Función auxiliar para extraer información adicional de trading
    """
    info = {}
    
    # Extraer información de lotes si existe
    lotes_match = re.search(r'(?:lot|size)[:\s]+(\d*\.?\d+)', texto.lower())
    if lotes_match:
        info['lotes'] = float(lotes_match.group(1))

    # Extraer información de riesgo si existe
    riesgo_match = re.search(r'(?:risk|r)[:\s]+(\d*\.?\d+)%?', texto.lower())
    if riesgo_match:
        info['riesgo'] = float(riesgo_match.group(1))

    # Extraer número de ronda si existe
    round_match = re.search(r'round\s*(\d+)', texto.lower())
    if round_match:
        info['ronda'] = int(round_match.group(1))

    return info if info else None
