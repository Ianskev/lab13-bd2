
import json, random, datetime, uuid, os, math, itertools, textwrap

categories = [
    ("Electrónica", ["Laptops", "Smartphones", "Accesorios"]),
    ("Hogar", ["Cocina", "Electrodomésticos", "Decoración"]),
    ("Deportes", ["Fitness", "Aire Libre", "Ciclismo"]),
    ("Moda", ["Ropa", "Calzado", "Accesorios"]),
]
brands = ["HP", "Apple", "Samsung", "Sony", "LG", "Adidas", "Nike", "Xiaomi", "Lenovo", "Asus"]
features_pool = [
    "Pantalla 4K", "Procesador Intel Core i7", "16GB de RAM", "512GB SSD", "Bluetooth 5.0",
    "Batería de larga duración", "Resistente al agua", "Carga rápida", "Pantalla táctil", "WiFi 6"
]

products = []
for pid in range(1, 101):
    cat, subcats = random.choice(categories)
    subcat = random.choice(subcats)
    brand = random.choice(brands)
    name = f"{subcat[:-1]} {brand} modelo {uuid.uuid4().hex[:4].upper()}"
    price = round(random.uniform(20, 2000), 2)
    discount = random.choice([0, 5, 10, 15, 20])
    stock = random.randint(10, 100)
    dimensions = {"ancho": round(random.uniform(10, 50), 1),
                  "alto": round(random.uniform(10, 50), 1),
                  "profundidad": round(random.uniform(1, 10), 1),
                  "unidad": "cm"}
    peso = {"valor": round(random.uniform(0.2, 5.0), 2), "unidad": "kg"}
    features = random.sample(features_pool, k=random.randint(3, 5))
    calificacion = round(random.uniform(3.0, 5.0), 1)
    release_date = (datetime.date(2022,1,1) + datetime.timedelta(days=random.randint(0, 900))).isoformat()
    products.append({
        "id_producto": pid,
        "nombre": name,
        "marca": brand,
        "precio": price,
        "descuento": discount,
        "categoria": cat,
        "subcategoria": subcat,
        "stock": stock,
        "dimensiones": dimensions,
        "peso": peso,
        "caracteristicas": features,
        "calificacion": calificacion,
        "descripcion": f"{name} con características avanzadas para usuarios exigentes.",
        "fecha_lanzamiento": release_date
    })

first_names = ["Carlos", "María", "Juan", "Ana", "Luis", "Elena", "Pedro", "Sofía", "Miguel", "Lucía"]
last_names = ["Pérez", "García", "López", "Rodríguez", "Hernández", "Martínez", "González", "Torres", "Ramírez", "Flores"]
countries = ["México", "Argentina", "Perú", "Chile", "Colombia"]
clients = []
for cid in range(1, 101):
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    email = f"{fname.lower()}.{lname.lower()}{cid}@mail.com"
    phone = f"555-{random.randint(1000,9999)}"
    street = f"Calle {random.choice(['Falsa','Real','Independencia','Libertad','Los Almendros'])} {random.randint(10,999)}"
    city = random.choice(["Ciudad de México","Buenos Aires","Lima","Santiago","Bogotá"])
    country = random.choice(countries)
    postal = f"{random.randint(10000,99999)}"
    clients.append({
        "id_cliente": cid,
        "nombre": f"{fname} {lname}",
        "email": email,
        "telefono": phone,
        "direccion": {
            "calle": street,
            "ciudad": city,
            "pais": country,
            "codigo_postal": postal
        }
    })

orders = []
for oid in range(1001, 1101):
    client_id = random.randint(1, 100)
    num_items = random.randint(1, 5)
    chosen_products = random.sample(products, k=num_items)
    items = []
    total = 0
    for p in chosen_products:
        qty = random.randint(1, 3)
        items.append({
            "id_producto": p["id_producto"],
            "nombre": p["nombre"],
            "cantidad": qty,
            "precio_unitario": p["precio"]
        })
        total += p["precio"] * qty
    order_date = (datetime.date(2023,1,1) + datetime.timedelta(days=random.randint(0, 540))).isoformat()
    orders.append({
        "id_pedido": oid,
        "id_cliente": client_id,
        "productos": items,
        "total_pedido": round(total,2),
        "fecha_pedido": order_date,
        "estado": random.choice(["Pendiente","Enviado","Entregado","Cancelado"])
    })

dataset_path = "./dataset"
os.makedirs(dataset_path, exist_ok=True)
with open(os.path.join(dataset_path, "productos.json"), "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)
with open(os.path.join(dataset_path, "clientes.json"), "w", encoding="utf-8") as f:
    json.dump(clients, f, ensure_ascii=False, indent=4)
with open(os.path.join(dataset_path, "pedidos.json"), "w", encoding="utf-8") as f:
    json.dump(orders, f, ensure_ascii=False, indent=4)

print("Archivos creados:", os.listdir(dataset_path))
