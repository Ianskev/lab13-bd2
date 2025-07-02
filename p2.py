import requests
import json
from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self):
        self.mongo_uri = "mongodb://localhost:27017/"
        self.db_name = "utec_store"
        self.categories_name="categorias"
        self.productos_name="productos"
        self.connect_mongo()
    def connect_mongo(self):
        try:
            client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            client.server_info()
            self.db = client[self.db_name]
            print(f"Conectado a la base de datos '{self.db_name}' en MongoDB.")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")
            print("Asegúrese de que MongoDB esté en ejecución en el puerto correcto.")
            exit(1)

    def fetch_json_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Error desconocido:", err)
        return None

    def fetch_all_categories(self, base_url):
        categories = self.fetch_json_data(base_url)
        if categories:
            for category in categories:
                # Verificamos si category es un string simple o un objeto
                if isinstance(category, dict):
                    # Si es un objeto, guardamos todas sus propiedades
                    self.db[self.categories_name].update_one(
                        {"slug": category.get("slug")},
                        {"$set": category},
                        upsert=True
                    )
                else:
                    # Si es un string simple, guardamos solo el nombre
                    self.db[self.categories_name].update_one(
                        {"name": category},
                        {"$set": {"name": category, "slug": category}},
                        upsert=True
                    )
            print(f"Se cargaron {len(categories)} categorías.")
        else:
            print("No se pudieron obtener las categorías.")

    def fetch_all_products(self):
        categories = list(self.db[self.categories_name].find())
        
        if not categories:
            print("No hay categorías disponibles en la base de datos.")
            return
        
        total_products = 0
        
        for category_doc in categories:

            category_id = category_doc.get("slug", category_doc.get("name", ""))
            
            if isinstance(category_id, str) and ('{' in category_id or "'" in category_id):
                try:
                    category_id = category_id.replace("'", '"')
                    category_data = json.loads(category_id)
                    category_id = category_data.get("slug", "")
                except:
                    category_id = category_doc.get("_id", "")
            
            if not isinstance(category_id, str) or not category_id:
                print(f"Saltando categoría con ID inválido: {category_doc}")
                continue
                
            products_url = f"https://dummyjson.com/products/category/{category_id}"
            print(f"Consultando URL: {products_url}")
            products_data = self.fetch_json_data(products_url)
            
            if products_data and "products" in products_data:
                products = products_data["products"]
                
                for product in products:
                    if "category" not in product:
                        product["category"] = category_id
                    
                    self.db[self.productos_name].update_one(
                        {"id": product["id"]},
                        {"$set": product},
                        upsert=True
                    )
                    total_products += 1
                
                print(f"Se cargaron {len(products)} productos de la categoría '{category_id}'")
            else:
                print(f"No se encontraron productos para la categoría '{category_id}'")
        
        print(f"Se cargaron un total de {total_products} productos de {len(categories)} categorías.")

mongo_handler = MongoDBHandler()

# URL del JSON para las categorías y productos
categories_url = "https://dummyjson.com/products/categories"
# 1. Cargar todas las categorías
mongo_handler.fetch_all_categories(categories_url)

# 2. Cargar todos los productos de cada categoría
mongo_handler.fetch_all_products()