import os
import tempfile
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QMessageBox, QCalendarWidget
from PyQt5.QtCore import Qt

class CatalogSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catálogo de Imagens INPE")
        self.setGeometry(200, 100, 700, 900)
        
        layout = QVBoxLayout()

        # Caixa de entrada para o intervalo de datas (calendário para data inicial e final)
        self.date_label = QLabel("Selecione o intervalo de datas:")
        layout.addWidget(self.date_label)

        # Calendários para selecionar datas
        self.start_calendar = QCalendarWidget()
        self.end_calendar = QCalendarWidget()
        layout.addWidget(QLabel("Data inicial:"))
        layout.addWidget(self.start_calendar)
        layout.addWidget(QLabel("Data final:"))
        layout.addWidget(self.end_calendar)

        # Lista de catálogos específicos
        self.catalog_label = QLabel("Selecione um Catálogo:")
        layout.addWidget(self.catalog_label)
        
        # Lista de opções de catálogos específicos (exemplo)
        self.catalog_list = QListWidget()
        self.catalog_list.addItem("Amazonia - 1/WFI")  #  catálogo
        self.catalog_list.addItem("CBERS - 4/MUX CLOUD")  # catalogo
        self.catalog_list.addItem("CBERS - 4/MUX Data Cube")
        self.catalog_list.addItem("CBERS - 4/WFI CLOUD")
        self.catalog_list.addItem("CBERS - 4/WFI Data Cube")
        self.catalog_list.addItem("CBERS - 4 Mosaico do brasil")
        self.catalog_list.addItem("CBERS - 4A/WFI CLOUD")
        layout.addWidget(self.catalog_list)
        
        # Botão para carregar imagens de acordo com o catálogo escolhido
        self.load_images_button = QPushButton("Carregar Imagens do Catálogo")
        self.load_images_button.clicked.connect(self.load_images)
        layout.addWidget(self.load_images_button)
        
        # Lista de imagens
        self.image_label = QLabel("Escolha uma Imagem:")
        layout.addWidget(self.image_label)
        
        self.image_list = QListWidget()
        layout.addWidget(self.image_list)

        # Botão de exibir imagem
        self.show_image_button = QPushButton("Mostrar Imagem no QGIS")
        self.show_image_button.clicked.connect(self.show_image)
        layout.addWidget(self.show_image_button)
        
        self.setLayout(layout)
    
    def get_selected_dates(self):
        start_date = self.start_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_calendar.selectedDate().toString("yyyy-MM-dd")
        return start_date, end_date
    
    def load_images(self):
        """Carrega imagens do catálogo selecionado com o intervalo de datas fornecido."""
        selected_catalog = self.catalog_list.currentItem().text()
        start_date, end_date = self.get_selected_dates()
        
        if selected_catalog == "Amazonia - 1/WFI":
            self.load_amazonia1_WFI(start_date, end_date)
        elif selected_catalog == "CBERS - 4/MUX CLOUD":
            self.load_cbers4a_mux_cloud_images(start_date, end_date)
        elif selected_catalog == "CBERS - 4/MUX Data Cube":
            self.load_cbers4_mux_images(start_date, end_date)
        elif selected_catalog == "CBERS - 4/WFI CLOUD":
            self.load_cbers4_efi_cloud_images(start_date, end_date)
        elif selected_catalog == "CBERS - 4/WFI Data Cube":
            self.load_cbers4_wfi_images(start_date, end_date)
        elif selected_catalog == "CBERS - 4 Mosaico do brasil":
            self.load_cbers4_wfi_mosaic_images(start_date, end_date)
        elif selected_catalog == "CBERS - 4A/WFI CLOUD":
            self.load_cbers4_wfi_cloud2_images(start_date, end_date)
        elif selected_catalog == "CBERS - 4A/WFI mosaico da paraíba":
            self.load_cbers4_wfi_paraiba_images(start_date, end_date)
        elif selected_catalog == "CBERS - 4A/WPM Multi bands":
            self.load_cbers4_wpm_images(start_date, end_date)
        elif selected_catalog == "CBERS - 4/WFI Data Cube - LCF 8 Dias":
            self.load_cbers4_wfi_8d_images(start_date, end_date)
        elif selected_catalog == "GOES - 13 - Level 3 - VIS/IR (Binario)":
            self.load_goes_13_images(start_date, end_date)
        elif selected_catalog == "GOES - 16 CLOUD":
            self.load_goes_16_images(start_date, end_date)
        elif selected_catalog == "Landsat coleção 2 - Level-2":
            self.load_landsat_level2_images(start_date, end_date)
        elif selected_catalog == "Landsat coleção 2 - Level-2 - Data Cube - LCF 16 dias":
            self.load_landsat_level2_16d_images(start_date, end_date)
        elif selected_catalog == "Landsat imagem mosaico do BRASIL - 6 meses":
            self.load_landsat_mosaic_images(start_date, end_date)
        elif selected_catalog == "Landsat imagem mosaico do bioma da Amazonia - 3 meses":
            self.load_landsat_mosaic_amazonia_images(start_date, end_date)
        elif selected_catalog == "Sentinel-1 - Level-1 - Interferometric Wide Swath Ground Range Detected High Resolution":
            self.load_sentinel1_level1_images(start_date, end_date)
        elif selected_catalog == "Sentinel-2 - Level-1C":
            self.load_sentinel2_level1c_images(start_date, end_date)
        elif selected_catalog == "Sentinel-2 - Level-2A":
            self.load_sentinel2a_images(start_date, end_date)
        elif selected_catalog == "Sentinel-2 - Level-2A - Cloud Optimized GeoTIFF":
            self.load_sentinel2a_cloud_images(start_date, end_date)
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da Amazonia - 1 Meses":
            self.load_sentinel2_mosaic_amazonia1m_images(start_date, end_date)
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da Amazonia - 3 meses":
            self.load_sentinel2_mosaic_amazonia3m_images(start_date, end_date)
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da cerrado - 2 meses":
            self.load_sentinel2_mosaic_cerrado2m_images(start_date, end_date)
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da cerrado - 4 meses":
            self.load_sentinel2_mosaic_cerrado4m_images(start_date, end_date)
        elif selected_catalog == "Sentinel-3/OLCI - Level-1B Full Resolution":
            self.load_sentinel3_level1_images(start_date, end_date)
            
    def load_amazonia1_WFI(self, start_date, end_date):
        """Função para carregar imagens do catálogo AMAZONIA-1/WFI - Level-4-SR - Cloud Optimized GeoTIFF"""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/AMZ1-WFI-L4-SR-1/items" #Adicionar URL 
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features',[]):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
                
    
    def load_cbers4a_mux_cloud_images(self, start_date, end_date):
        """Função para carregar imagens do catálogo CBERS-4/MUX - Level-4-SR - Cloud Optimized GeoTIFF."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CB4-MUX-L4-SR-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_mux_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4/MUX - Level-4-SR - Data Cube - LCF 2 months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CBERS4-MUX-2M-1/items"
        params = {'datatime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_wfi_cloud_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4/WFI - Level-4-SR - Cloud Optimized GeoTIFF."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CB4-WFI-L4-SR-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_wfi_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4/WFI - Level-4-SR - Data Cube - LCF 16 days."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CBERS4-WFI-16D-2/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_wfi_mosaic_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4/WFI Image Mosaic of Brazil - 3 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-cbers4-brazil-3m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_wfi_cloud2_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4A/WFI - Level-4-SR - Cloud Optimized GeoTIFF."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CB4A-WFI-L4-SR-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_wfi_paraiba_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4A/WFI Image Mosaic of Brazil Paraíba State - 3 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-cbers4a-paraiba-3m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_cbers4_wpm_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4A/WPM - Multispectral and Panchromatic Bands Fusioned."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CB4A-WPM-PCA-FUSED-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_cbers4_wfi_8d_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS/WFI - Level-4-SR - Data Cube - LCF 8 days."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CBERS-WFI-8D-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_goes_13_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo GOES-13/Imager - Level-3 - VIS/IR Imagery (Binary)."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/GOES13-L3-IMAGER-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_goes_16_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo GOES-16 Cloud & Moisture Imagery."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/GOES16-L2-CMI-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_landsat_level2_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Landsat Collection 2 - Level-2."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/landsat-2/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_landsat_level2_16d_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Landsat Collection 2 - Level-2 - Data Cube - LCF 16 days."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/LANDSAT-16D-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_landsat_mosaic_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Landsat Image Mosaic of Brazil - 6 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-landsat-brazil-6m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_landsat_mosaic_amazonia_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Landsat Image Mosaic of Brazilian Amazon Biome - 3 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-landsat-amazon-3m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_sentinel1_level1_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Sentinel-1 - Level-1 - Interferometric Wide Swath Ground Range Detected High Resolution."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/sentinel-1-grd-bundle-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_sentinel2_level1c_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Sentinel-2 - Level-1C."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/S2_L1C_BUNDLE-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('feature', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_sentinel2a_images(self, start_date, end_date):
        """Função para carregar imagens do catálogo Sentinel-2 - Level-2A."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/S2_L2A_BUNDLE-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_sentinel2a_cloud_images(self, start_date, end_date):
        """Função para carregar imagens do catálogo Sentinel-2 - Level-2A - Cloud Optimized GeoTIFF."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/S2_L2A-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_sentinel2_mosaic_amazonia1m_images(self, start_date, end_date):
        """Função para carregar imagens do catálogo Sentinel-2 image Mosaic of Brazilian Amazon Biome - 1 Month."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-s2-amazon-1m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_sentinel2_mosaic_amazonia3m_images(self, start_date, end_date):
        """Função para carregar imagens do catálogo Sentinel-2 image Mosaic of Brazilian Amazon Biome - 3 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-s2-amazon-3m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_sentinel2_mosaic_cerrado2m_images(self, start_date, end_date):
        """Função para carregar imagens do catálogo Sentinel-2 Image Mosaic of Brazilian Cerrado Biome - 2 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-s2-cerrado-2m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_sentinel2_mosaic_cerrado4m_images(self, start_date, end_date):
        """Função para carregar imagens do catálogo Sentinel-2 image Mosaic of Brazilian Cerrado Biome - 4 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-s2-cerrado-4m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_sentinel3_level1_images(self, start_date, end_date):
        """Função para carregar imagens do catálogo Sentinel-3/OLCI - Level-1B Full Resolution."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/sentinel-3-olci-l1-bundle-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        data = response.json()
        
        self.image_list.clear()
        
        for feature in data.get('features', []):
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            self.image_list.addItem(f"{image_id} | {image_date}")

    def show_image(self):
        """Exibe o arquivo .zip completo dentro do QGIS."""
        selected_item = self.image_list.currentItem()
        
        if not selected_item:
            QMessageBox.warning(self, "Seleção de Imagem", "Por favor, selecione uma imagem.")
            return
        
        image_id = selected_item.text().split(" | ")[0]
        selected_catalog = self.catalog_list.currentItem().text()
        
        if selected_catalog == "Amazonia - 1/WFI":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/AMZ1-WFI-L4-SR-1/items/{image_id}"
        elif selected_catalog == "CBERS - 4/MUX CLOUD":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CB4-MUX-L4-SR-1/items/{image_id}"
        elif selected_catalog == "CBERS - 4/MUX Data Cube":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CBERS4-MUX-2M-1/items{image_id}"
        
        response = requests.get(catalog_url)
        image_data = response.json()
        
        if 'assets' in image_data and 'asset' in image_data['assets']:
            image_url = image_data['assets']['asset']['href']
            zip_data = requests.get(image_url).content
            
            # Salva o arquivo zip temporariamente em uma pasta temporária
            temp_dir = tempfile.gettempdir()  # Diretório temporário
            zip_path = os.path.join(temp_dir, "temp_image.zip")
            with open(zip_path, 'wb') as zip_file:
                zip_file.write(zip_data)
            
            # Carrega o arquivo .zip inteiro como camada raster no QGIS
            zip_layer = QgsRasterLayer(f"zip://{zip_path}", "Imagem ZIP")

            if zip_layer.isValid():
                QgsProject.instance().addMapLayer(zip_layer)
            else:
                QMessageBox.critical(self, "Erro ao Carregar", "O arquivo ZIP não é válido ou não contém imagens geotiff.")
        else:
            QMessageBox.warning(self, "Imagem Indisponível", "Esta imagem não possui um arquivo ZIP disponível.")

# Inicialização do aplicativo PyQt5
app = QApplication([])
window = CatalogSelector()
window.show()
app.exec_()
