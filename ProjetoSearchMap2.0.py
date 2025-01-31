import os
import zipfile
import tempfile
import requests
from qgis.utils import iface 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QMessageBox, QCalendarWidget
from PyQt5.QtCore import Qt
from datetime import datetime
from qgis.core import QgsRasterLayer, QgsProject

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
        self.catalog_list.addItem("Amazonia - 1/WFI")  # APARECE
        self.catalog_list.addItem("CBERS - 4/MUX CLOUD")  # APARECE
        self.catalog_list.addItem("CBERS - 4/MUX Data Cube") # APARECE
        self.catalog_list.addItem("CBERS - 4/WFI CLOUD") #Não aparece
        self.catalog_list.addItem("CBERS - 4/WFI Data Cube") # não aparece
        self.catalog_list.addItem("CBERS - 4 Mosaico do brasil") # nao aparece
        self.catalog_list.addItem("CBERS - 4A/WFI CLOUD") # nao aparece imagens
        self.catalog_list.addItem("CBERS - 4A/WFI mosaico da paraíba") # nao aparece
        self.catalog_list.addItem("CBERS - 4A/WPM Multi bands") #nao aparece
        self.catalog_list.addItem("CBERS - 4/WFI Data Cube - LCF 8 Dias")
        self.catalog_list.addItem("GOES - 13 - Level 3 - VIS/IR (Binario)")
        self.catalog_list.addItem("GOES - 16 CLOUD")
        self.catalog_list.addItem("Landsat coleção 2 - Level-2")
        self.catalog_list.addItem("Landsat coleção 2 - Level-2 - Data Cube - LCF 16 dias")
        self.catalog_list.addItem("Landsat imagem mosaico do BRASIL - 6 meses")
        self.catalog_list.addItem("Landsat imagem mosaico do bioma da Amazonia - 3 meses")
        self.catalog_list.addItem("Sentinel-1 - Level-1 - Interferometric Wide Swath Ground Range Detected High Resolution")
        self.catalog_list.addItem("Sentinel-2 - Level-1C")
        self.catalog_list.addItem("Sentinel-2 - Level-2A") # APARECE
        self.catalog_list.addItem("Sentinel-2 - Level-2A - Cloud Optimized GeoTIFF") # APARECE
        self.catalog_list.addItem("Sentinel-2 image mosaico do bioma da Amazonia - 1 Meses") # APARECE
        self.catalog_list.addItem("Sentinel-2 image mosaico do bioma da Amazonia - 3 meses") # APARECE
        self.catalog_list.addItem("Sentinel-2 image mosaico do bioma da cerrado - 2 meses") # APARECE
        self.catalog_list.addItem("Sentinel-2 image mosaico do bioma da cerrado - 4 meses") # APARECE
        self.catalog_list.addItem("Sentinel-3/OLCI - Level-1B Full Resolution") # APARECE
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

        self.exit_button = QPushButton("Sair")
        self.exit_button.clicked.connect(self.exit_application)
        layout.addWidget(self.exit_button)
        
        self.setLayout(layout) 

    def get_selected_dates(self):
        start_date = self.start_calendar.selectedDate().toString("dd-MM-yyyy")
        end_date = self.end_calendar.selectedDate().toString("dd-MM-yyyy")
        return start_date, end_date
    
         
    def convert_to_iso_format(self, date_str):
        """Converte uma data no formato dd-MM-yyyy para o formato ISO yyyy-MM-dd."""
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y") 
            return date_obj.strftime("%Y-%m-%d") 
        except ValueError as e:
            print(f"Erro na conversão da data: {e}")
            return None

    def exit_application(self):
        """Fecha apenas a janela do plugin."""
        self.close()

    def load_images(self):
        """Carrega imagens do catálogo selecionado com o intervalo de datas fornecido."""
        selected_catalog = self.catalog_list.currentItem().text()
        start_date, end_date = self.get_selected_dates()

        start_date_iso = self.convert_to_iso_format(start_date)
        end_date_iso = self.convert_to_iso_format(end_date)

        if not start_date_iso or not end_date_iso:
            QMessageBox.warning(self, "Erro de data", "As datas inseridas são invalidas")
        
        if selected_catalog == "Amazonia - 1/WFI":
            self.load_amazonia1_WFI(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4/MUX CLOUD":
            self.load_cbers4a_mux_cloud_images(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4/MUX Data Cube":
            self.load_cbers4_mux_images(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4/WFI CLOUD":
            self.load_cbers4_efi_cloud_images(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4/WFI Data Cube":
            self.load_cbers4_wfi_images(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4 Mosaico do brasil":
            self.load_cbers4_wfi_mosaic_images(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4A/WFI CLOUD":
            self.load_cbers4_wfi_cloud2_images(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4A/WFI mosaico da paraíba":
            self.load_cbers4_wfi_paraiba_images(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4A/WPM Multi bands":
            self.load_cbers4_wpm_images(start_date_iso, end_date_iso)
        elif selected_catalog == "CBERS - 4/WFI Data Cube - LCF 8 Dias":
            self.load_cbers4_wfi_8d_images(start_date_iso, end_date_iso)
        elif selected_catalog == "GOES - 13 - Level 3 - VIS/IR (Binario)":
            self.load_goes_13_images(start_date_iso, end_date_iso)
        elif selected_catalog == "GOES - 16 CLOUD":
            self.load_goes_16_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Landsat coleção 2 - Level-2":
            self.load_landsat_level2_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Landsat coleção 2 - Level-2 - Data Cube - LCF 16 dias":
            self.load_landsat_level2_16d_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Landsat imagem mosaico do BRASIL - 6 meses":
            self.load_landsat_mosaic_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Landsat imagem mosaico do bioma da Amazonia - 3 meses":
            self.load_landsat_mosaic_amazonia_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-1 - Level-1 - Interferometric Wide Swath Ground Range Detected High Resolution":
            self.load_sentinel1_level1_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-2 - Level-1C":
            self.load_sentinel2_level1c_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-2 - Level-2A":
            self.load_sentinel2a_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-2 - Level-2A - Cloud Optimized GeoTIFF":
            self.load_sentinel2a_cloud_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da Amazonia - 1 Meses":
            self.load_sentinel2_mosaic_amazonia1m_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da Amazonia - 3 meses":
            self.load_sentinel2_mosaic_amazonia3m_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da cerrado - 2 meses":
            self.load_sentinel2_mosaic_cerrado2m_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da cerrado - 4 meses":
            self.load_sentinel2_mosaic_cerrado4m_images(start_date_iso, end_date_iso)
        elif selected_catalog == "Sentinel-3/OLCI - Level-1B Full Resolution":
            self.load_sentinel3_level1_images(start_date_iso, end_date_iso)


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
            
    def load_cbers4_efi_cloud_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4/WFI - Level-4-SR - Cloud Optimized GeoTIFF."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CB4-WFI-L4-SR-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        # Requisição à API
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")
    
    def load_cbers4_wfi_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4/WFI - Level-4-SR - Data Cube - LCF 16 days."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CBERS4-WFI-16D-2/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_wfi_mosaic_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4/WFI Image Mosaic of Brazil - 3 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-cbers4-brazil-3m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_wfi_cloud2_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4A/WFI - Level-4-SR - Cloud Optimized GeoTIFF."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CB4A-WFI-L4-SR-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_cbers4_wfi_paraiba_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4A/WFI Image Mosaic of Brazil Paraíba State - 3 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-cbers4a-paraiba-3m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_cbers4_wpm_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS-4A/WPM - Multispectral and Panchromatic Bands Fusioned."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CB4A-WPM-PCA-FUSED-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_cbers4_wfi_8d_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo CBERS/WFI - Level-4-SR - Data Cube - LCF 8 days."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/CBERS-WFI-8D-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_goes_13_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo GOES-13/Imager - Level-3 - VIS/IR Imagery (Binary)."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/GOES13-L3-IMAGER-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_goes_16_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo GOES-16 Cloud & Moisture Imagery."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/GOES16-L2-CMI-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_landsat_level2_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Landsat Collection 2 - Level-2."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/landsat-2/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_landsat_level2_16d_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Landsat Collection 2 - Level-2 - Data Cube - LCF 16 days."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/LANDSAT-16D-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_landsat_mosaic_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Landsat Image Mosaic of Brazil - 6 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-landsat-brazil-6m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_landsat_mosaic_amazonia_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Landsat Image Mosaic of Brazilian Amazon Biome - 3 Months."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/mosaic-landsat-amazon-3m-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")

    def load_sentinel1_level1_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Sentinel-1 - Level-1 - Interferometric Wide Swath Ground Range Detected High Resolution."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/sentinel-1-grd-bundle-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
            self.image_list.addItem(f"{image_id} | {image_date}")
            
    def load_sentinel2_level1c_images(self, start_date, end_date):
        """Função para carregar imagens do catalogo Sentinel-2 - Level-1C."""
        catalog_url = "https://data.inpe.br/bdc/stac/v1/collections/S2_L1C_BUNDLE-1/items"
        params = {'datetime': f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"}
        response = requests.get(catalog_url, params=params)
        QgsMessageLog.logMessage("Status Code: {}".format(response.status_code), 'QGIS Log')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code != 200:
            QgsMessageLog.logMessage("Erro na requisição: {}".format(response.text), 'QGIS Log')
            QMessageBox.critical(self, "Erro", "Não foi possível obter dados do catálogo.")
            return
        
        # Processar os dados retornados
        data = response.json()
        features = data.get('features', [])
        QgsMessageLog.logMessage("Quantidade de Imagens Encontradas: {}".format(len(features)), 'QGIS Log')
        
        if not features:
            QMessageBox.information(self, "Sem Imagens", "Não há imagens disponíveis para o intervalo de datas selecionado.")
            return

        self.image_list.clear()
        for feature in features:
            QgsMessageLog.logMessage("Feature: {}".format(feature), 'QGIS Log')  # Exibe cada item retornado
            image_id = feature['id']
            image_date = feature['properties']['datetime']
            QgsMessageLog.logMessage(f"ID: {image_id}, Date: {image_date}", 'QGIS Log')
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
        
        catalog_url = None

        if selected_catalog == "Amazonia - 1/WFI":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/AMZ1-WFI-L4-SR-1/items/{image_id}"
        elif selected_catalog == "CBERS - 4/MUX CLOUD":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CB4-MUX-L4-SR-1/items/{image_id}"
        elif selected_catalog == "CBERS - 4/MUX Data Cube":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CBERS4-MUX-2M-1/items{image_id}"
        elif selected_catalog == "CBERS - 4/WFI CLOUD":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CB4-WFI-L4-SR-1/items/{image_id}"
        elif selected_catalog == "CBERS - 4/WFI Data Cube":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CBERS4-WFI-16D-2/items/{image_id}"
        elif selected_catalog == "CBERS - 4 Mosaico do brasil":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/mosaic-cbers4-brazil-3m-1/items/{image_id}"
        elif selected_catalog == "CBERS - 4A/WFI CLOUD":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CB4A-WFI-L4-SR-1/items/{image_id}"
        elif selected_catalog =="CBERS - 4A/WFI mosaico da paraíba":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/mosaic-cbers4a-paraiba-3m-1/items/{image_id}"
        elif selected_catalog == "CBERS - 4A/WPM Multi bands":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CB4A-WPM-PCA-FUSED-1/items/{image_id}"
        elif selected_catalog == "CBERS - 4/WFI Data Cube - LCF 8 Dias":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/CBERS-WFI-8D-1/items/{image_id}"
        elif selected_catalog == "GOES - 13 - Level 3 - VIS/IR (Binario)":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/GOES13-L3-IMAGER-1/items/{image_id}"
        elif selected_catalog == "GOES - 16 CLOUD":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/GOES16-L2-CMI-1/items/{image_id}"
        elif selected_catalog == "Landsat coleção 2 - Level-2":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/landsat-2/items/{image_id}"
        elif selected_catalog == "Landsat coleção 2 - Level-2 - Data Cube - LCF 16 dias":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/LANDSAT-16D-1/items/{image_id}"
        elif selected_catalog == "Landsat imagem mosaico do BRASIL - 6 meses":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/mosaic-landsat-brazil-6m-1/items/{image_id}"
        elif selected_catalog == "Landsat imagem mosaico do bioma da Amazonia - 3 meses":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/mosaic-landsat-amazon-3m-1/items/{image_id}"
        elif selected_catalog == "Sentinel-1 - Level-1 - Interferometric Wide Swath Ground Range Detected High Resolution":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/sentinel-1-grd-bundle-1/items/{image_id}"
        elif selected_catalog == "Sentinel-2 - Level-1C":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/S2_L1C_BUNDLE-1/items/{image_id}"
        elif selected_catalog == "Sentinel-2 - Level-2A":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/S2_L2A_BUNDLE-1/items/{image_id}"
        elif selected_catalog == "Sentinel-2 - Level-2A - Cloud Optimized GeoTIFF":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/S2_L2A-1/items/{image_id}"
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da Amazonia - 1 Meses":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/mosaic-s2-amazon-1m-1/items/{image_id}"
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da Amazonia - 3 meses":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/mosaic-s2-amazon-3m-1/items/{image_id}"
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da cerrado - 2 meses":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/mosaic-s2-cerrado-2m-1/items/{image_id}"
        elif selected_catalog == "Sentinel-2 image mosaico do bioma da cerrado - 4 meses":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/mosaic-s2-cerrado-4m-1/items/{image_id}"
        elif selected_catalog == "Sentinel-3/OLCI - Level-1B Full Resolution":
            catalog_url = f"https://data.inpe.br/bdc/stac/v1/collections/sentinel-3-olci-l1-bundle-1/items/{image_id}"
            
        # Verifica se a URL do catálogo foi definida
        if not catalog_url:
            QMessageBox.warning(self, "Erro", "Catálogo não encontrado ou não suportado.")
            return
        
        # Faz a requisição para obter os dados da imagem
        response = requests.get(catalog_url)
        if response.status_code != 200:
            QMessageBox.warning(self, "Erro", "Não foi possível obter os dados da imagem.")
            return
        
        image_data = response.json()
        
        # Lógica original para .ZIP (funcionava antes)
        if 'assets' in image_data and 'asset' in image_data['assets']:
            image_url = image_data['assets']['asset']['href']
            
            iface.addRasterLayer(f"/vsicurl/{image_url}", "Imagem Raster")


            # Verifica se é .ZIP ou .COG
            if image_url.endswith(".zip"):
                # Abre o .ZIP como no código original
                iface.addRasterLayer(f"/vsizip/{image_url}", "Imagem Raster")
                return
            else:
                # Tenta abrir como COG
                iface.addRasterLayer(f"/vsicurl/{image_url}", "Imagem Raster")
                return
        
        # Se não tiver o asset 'asset', procura por COG ou ZIP manualmente
        for asset_name, asset_info in image_data.get('assets', {}).items():
            # Prioriza COG
            if asset_info.get('type') == 'image/tiff; application=geotiff; profile=cloud-optimized':
                cog_url = asset_info['href']
                iface.addRasterLayer(f"/vsicurl/{cog_url}", f"COG: {image_id}")
                return
            
            # Verifica ZIP genérico
            elif asset_info.get('type') == 'application/zip':
                zip_url = asset_info['href']
                iface.addRasterLayer(f"/vsizip/{zip_url}", f"ZIP: {image_id}")
                return
        
        QMessageBox.warning(self, "Erro", "Nenhum arquivo .ZIP ou .COG válido encontrado.")



# Inicialização do aplicativo PyQt5
app = QApplication([])
window = CatalogSelector()
window.show()
app.exec_()
