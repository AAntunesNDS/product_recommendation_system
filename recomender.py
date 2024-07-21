from typing import List
from models import Product
from datetime import date
import calendar

import pandas as pd

class ProductRecommender:
    def __init__(self, csv_file):
        # Carregar os dados a partir do CSV
        self.df = pd.read_csv(csv_file)
        
        # Converter a coluna sale_date para o tipo datetime
        self.df['sale_date'] = pd.to_datetime(self.df['sale_date'])
        
        # Criar a nova coluna com o nome do dia da semana
        self.df['day_of_week'] = self.df['sale_date'].dt.day_name()
        
        # Categorizar os produtos
        self.categories = {
            "Eletrônicos de Entretenimento": ["Home Theater Sony", "Smart TV LG 55'", "Console Playstation 5"],
            "Computadores e Acessórios": ["Notebook Dell Inspiron 15", "Monitor Gamer AOC", "Tablet Samsung Galaxy Tab",
                                          "Processador Intel Core i7", "Placa de Vídeo NVIDIA GeForce", "SSD Samsung EVO",
                                          "Memória RAM Kingston"],
            "Periféricos de Computador": ["Mouse Logitech MX Master", "Teclado Mecânico Razer", "Headset Gamer HyperX"],
            "Áudio": ["Caixa de Som Bluetooth Bose", "Fone de Ouvido Bluetooth JBL"],
            "Fotografia e Filmagem": ["Câmera Digital Canon EOS", "Drone DJI Phantom", "Câmera de Segurança Intelbras"],
            "Saúde e Bem-Estar": ["Termômetro Digital G-Tech", "Oxímetro de Pulso Yonker", "Aparelho de Pressão Omron"],
            "Eletrodomésticos de Cozinha": ["Panela de Pressão Elétrica Mondial", "Cafeteira Elétrica Cadence", 
                                            "Cafeteira Nespresso", "Liquidificador Philips Walita", "Chaleira Elétrica Oster",
                                            "Grill Elétrico George Foreman", "Fritadeira Air Fryer Philips"],
            "Eletrodomésticos Gerais": ["Ar Condicionado Split LG", "Geladeira Inverse Brastemp", "Fogão 4 Bocas Electrolux",
                                        "Máquina de Lavar Roupas Brastemp", "Micro-ondas Panasonic", "Ventilador de Mesa Arno"],
            "Eletroportáteis": ["Máquina de Costura Singer", "Aspirador de Pó Robô Roomba", "Escova Secadora Philco"],
            "Itens de Casa e Cuidados Pessoais": ["Purificador de Água Consul", "Smart Lâmpada LED", "Roteador TP-Link"],
            "Dispositivos Pessoais": ["Relógio Inteligente Apple Watch", "Smartwatch Xiaomi", "Kindle Paperwhite"],
            "Esporte e Lazer": ["Bicicleta Ergométrica Kikos"],
            "Armazenamento": ["HD Externo Seagate", "Carregador Portátil Anker"],
            "Impressão e Escritório": ["Impressora Multifuncional HP", "Projetor Epson"]
        }
        
        self.df['category'] = self.df['product_title'].apply(self.categorize_product)
        
        # Agrupar os dados
        self.df_products = self.df.groupby('product_id').agg({
            'sales_per_day': 'sum',
            'category': 'first',
            'product_title': 'first',
            'product_price': 'mean',
            'product_image_url': 'first',
            'store_name': 'max',
            'store_id': 'max',
            'day_of_week': 'max',
        }).reset_index().sort_values(by='sales_per_day', ascending=False)
        
        self.df_category_sales = self.df.groupby(['day_of_week', 'category'])['sales_per_day'].sum().reset_index().sort_values(by='sales_per_day', ascending=False)
    
    def categorize_product(self, title):
        for category, products in self.categories.items():
            if title in products:
                return category
        return "Outros"
    
    def recommend_products(self, user_id):

        # Criando recomendação para usuario:
        print(f'Criando recomendação para usuario: {user_id}')

        my_date = date.today()
        current_day_of_week = calendar.day_name[my_date.weekday()]
        # Filtrar as categorias mais vendidas no dia atual
        top_categories = self.df_category_sales[self.df_category_sales['day_of_week'] == current_day_of_week].sort_values(by='sales_per_day', ascending=False)['category'].unique()
        
        # Lista para armazenar as recomendações
        recommendations = []
        
        # Buscar os produtos mais vendidos das categorias top
        for category in top_categories:
            top_products = self.df_products[self.df_products['category'] == category].sort_values(by='sales_per_day', ascending=False)
            recommendations.extend(top_products.head(5).to_dict(orient='records'))
            if len(recommendations) >= 5:
                break
        
        # Limitar a 5 recomendações
        top_products = recommendations[:5]
        
        # Garantir que cada produto está formatado corretamente
        products = []
        for product in top_products:
            # Assegura que todos os campos estão presentes e corretamente formatados
            product_data = {
                "id": product["product_id"],
                "name": product["product_title"],
                "sales_per_day": product["sales_per_day"],
                "category": product["category"],
                "product_title": product["product_title"],
                "product_price": product["product_price"],
                "product_image_url": product["product_image_url"],
                "store_name": product["store_name"],
                "store_id": product["store_id"],
                "day_of_week": product["day_of_week"]
            }
            products.append(Product(**product_data))
        
        return products
