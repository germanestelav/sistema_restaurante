import requests
from collections import defaultdict

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

    for pedido in pedidos:
        print(f"\nPedido ID: {pedido['id_pedido']} | Mesa: {pedido['id_mesa']} | Estado: {pedido['estado']} | Fecha: {pedido['fecha']}")
        detalles = get_detalles_pedido(pedido['id_pedido'])
        for detalle in detalles:
            producto = get_producto(detalle['id_producto'])
            print(f"  - Producto: {producto['nombre']} | Cantidad: {detalle['cantidad']} | Precio unitario: {detalle['precio_unitario']}")
        pagos = get_pago_por_pedido(pedido['id_pedido'])
        if pagos:
            for pago in pagos:
                print(f"  >> PAGADO: {pago['monto_total']} por {pago['metodo_pago']} el {pago['fecha_pago']}")
                total_general += float(pago['monto_total'])
                totales_por_metodo[pago['metodo_pago']] += float(pago['monto_total'])
        else:
            print("  >> NO PAGADO")

    print("\n=== RESUMEN DE CAJA DEL MOZO ===")
    print(f"Total recaudado: {total_general:.2f}")
    for metodo, total in totales_por_metodo.items():
        print(f"  - {metodo}: {total:.2f}")
    print("\n=================================")
    print("=================================")
if __name__ == "__main__":
    mostrar_pedidos_completos(id_usuario=1)