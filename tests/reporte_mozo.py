import requests
from collections import defaultdict
import csv

BASE_URL = "http://localhost:8000"

def get_usuario(id_usuario):
    response = requests.get(f"{BASE_URL}/usuarios/{id_usuario}")
    response.raise_for_status()
    return response.json()

def get_pedidos_por_usuario(id_usuario):
    response = requests.get(f"{BASE_URL}/pedidos/")
    response.raise_for_status()
    pedidos = response.json()
    return [p for p in pedidos if p["id_usuario"] == id_usuario]

def get_detalles_pedido(id_pedido):
    response = requests.get(f"{BASE_URL}/detalle_pedidos/{id_pedido}")
    response.raise_for_status()
    return response.json()

def get_producto(id_producto):
    response = requests.get(f"{BASE_URL}/productos/{id_producto}")
    response.raise_for_status()
    return response.json()

def get_pago_por_pedido(id_pedido):
    response = requests.get(f"{BASE_URL}/pagos/")
    response.raise_for_status()
    pagos = response.json()
    return [p for p in pagos if p["id_pedido"] == id_pedido]

def mostrar_pedidos_completos(id_usuario):
    usuario = get_usuario(id_usuario)
    print(f"\nMozo: {usuario['nombre']} (ID: {usuario['id_usuario']})")
    pedidos = get_pedidos_por_usuario(id_usuario)
    if not pedidos:
        print("No hay pedidos para este mozo.")
        return

    total_general = 0
    totales_por_metodo = defaultdict(float)
    filas_csv = []

    for pedido in pedidos:
        detalles = get_detalles_pedido(pedido['id_pedido'])
        pagos = get_pago_por_pedido(pedido['id_pedido'])
        pago_escrito = False  # Para escribir el pago solo una vez por pedido
        for detalle in detalles:
            producto = get_producto(detalle['id_producto'])
            fila = {
                "Pedido ID": pedido['id_pedido'],
                "Mesa": pedido['id_mesa'],
                "Estado Pedido": pedido['estado'],
                "Fecha Pedido": pedido['fecha'],
                "Producto": producto['nombre'],
                "Cantidad": detalle['cantidad'],
                "Precio Unitario": detalle['precio_unitario'],
                "Pagado": "NO",
                "Monto Pagado": "",
                "Metodo Pago": "",
                "Fecha Pago": ""
            }
            if pagos and not pago_escrito:
                for pago in pagos:
                    fila_pagada = fila.copy()
                    fila_pagada["Pagado"] = "SI"
                    fila_pagada["Monto Pagado"] = pago['monto_total']
                    fila_pagada["Metodo Pago"] = pago['metodo_pago']
                    fila_pagada["Fecha Pago"] = pago['fecha_pago']
                    filas_csv.append(fila_pagada)
                    pago_escrito = True
            else:
                filas_csv.append(fila)
            # Sumar pagos solo una vez por cada pago del pedido
            if pagos:
                for pago in pagos:
                    total_general += float(pago['monto_total'])
                    totales_por_metodo[pago['metodo_pago']] += float(pago['monto_total'])
        
    # Guardar en CSV
    with open("reporte_mozo.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Pedido ID", "Mesa", "Estado Pedido", "Fecha Pedido",
            "Producto", "Cantidad", "Precio Unitario",
            "Pagado", "Monto Pagado", "Metodo Pago", "Fecha Pago"
        ])
        writer.writeheader()
        writer.writerows(filas_csv)

    print("\n=== RESUMEN DE CAJA DEL MOZO ===")
    print(f"Total recaudado: {total_general:.2f}")
    for metodo, total in totales_por_metodo.items():
        print(f"  - {metodo}: {total:.2f}")
    print("\nReporte guardado en 'reporte_mozo.csv'.")

    print("=================================")
    print("=================================")

if __name__ == "__main__":
    mostrar_pedidos_completos(id_usuario=1)