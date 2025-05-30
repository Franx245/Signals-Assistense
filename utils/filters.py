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
