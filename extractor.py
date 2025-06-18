"""
Extractor Esencial para Prevención de Colisiones Satelitales
Solo extrae datos críticos: TLE activos, basura espacial crítica y CDM críticos
"""

import subprocess
import sys
import os
import requests
import json
import csv
from datetime import datetime, timedelta
import time
from collections import defaultdict

# Configurar credenciales desde archivo env o variables de entorno
def load_credentials():
    """Cargar credenciales desde archivo env o variables de entorno"""
    credentials = {}
    
    # Primero intentar leer desde variables de entorno (Azure App Service)
    username = os.getenv('SPACE_TRACK_USERNAME')
    password = os.getenv('SPACE_TRACK_PASSWORD')
    
    if username and password:
        credentials['SPACE_TRACK_USERNAME'] = username
        credentials['SPACE_TRACK_PASSWORD'] = password
        print("✅ Credenciales cargadas desde variables de entorno")
        return credentials
    
    # Si no están en variables de entorno, intentar archivo env (desarrollo local)
    try:
        with open('env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    credentials[key] = value
        print("✅ Credenciales cargadas desde archivo env")
        return credentials
    except FileNotFoundError:
        print("❌ Archivo env no encontrado y variables de entorno no configuradas")
        return {}

def install_dependencies():
    """Instalar dependencias automáticamente"""
    print("🔧 Instalando dependencias...")
    
    dependencies = ['requests']
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {dep}")
            return False
    
    return True

class SpaceTrackExtractor:
    """Extractor de Space-Track.org para datos críticos"""
    
    def __init__(self, username, password):
        self.base_url = "https://www.space-track.org"
        self.session = requests.Session()
        self.authenticated = False
        self.username = username
        self.password = password
    
    def authenticate(self):
        """Autenticar con Space-Track"""
        print("🔐 Autenticando con Space-Track.org...")
        
        try:
            login_data = {
                'identity': self.username,
                'password': self.password
            }
            
            response = self.session.post(
                f"{self.base_url}/ajaxauth/login",
                data=login_data,
                timeout=30
            )
            
            if response.status_code == 200:
                self.authenticated = True
                print("✅ Autenticación Space-Track exitosa")
                return True
            else:
                print(f"❌ Error Space-Track: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error Space-Track: {e}")
            return False
    
    def extract_active_tle(self):
        """Extraer TLE de satélites activos (últimos 7 días)"""
        print("📡 Extrayendo TLE de satélites activos...")
        
        try:
            # TLE de satélites activos, últimos 7 días
            url = f"{self.base_url}/basicspacedata/query/class/tle_latest/ORDINAL/1/EPOCH/%3Enow-7/format/json/orderby/NORAD_CAT_ID"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Filtrar solo campos esenciales
                filtered_data = []
                for item in data:
                    filtered_item = {
                        'NORAD_CAT_ID': item.get('NORAD_CAT_ID', ''),
                        'OBJECT_NAME': item.get('OBJECT_NAME', ''),
                        'EPOCH': item.get('EPOCH', ''),
                        'MEAN_MOTION': item.get('MEAN_MOTION', ''),
                        'ECCENTRICITY': item.get('ECCENTRICITY', ''),
                        'INCLINATION': item.get('INCLINATION', ''),
                        'RA_OF_ASC_NODE': item.get('RA_OF_ASC_NODE', ''),
                        'ARG_OF_PERICENTER': item.get('ARG_OF_PERICENTER', ''),
                        'MEAN_ANOMALY': item.get('MEAN_ANOMALY', ''),
                        'BSTAR': item.get('BSTAR', ''),
                        '_source': 'space_track',
                        '_type': 'active_tle'
                    }
                    filtered_data.append(filtered_item)
                
                print(f"✅ TLE activos: {len(filtered_data)} satélites")
                return filtered_data
            return []
        except Exception as e:
            print(f"❌ Error TLE activos: {e}")
            return []
    
    def extract_debris_tle(self):
        """Extraer TLE de basura espacial crítica (últimos 30 días)"""
        print("🗑️ Extrayendo TLE de basura espacial crítica...")
        
        try:
            # TLE de basura espacial, últimos 30 días
            url = f"{self.base_url}/basicspacedata/query/class/tle_latest/ORDINAL/1/EPOCH/%3Enow-30/OBJECT_TYPE/DEBRIS/format/json/orderby/NORAD_CAT_ID"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Filtrar solo campos esenciales
                filtered_data = []
                for item in data:
                    filtered_item = {
                        'NORAD_CAT_ID': item.get('NORAD_CAT_ID', ''),
                        'OBJECT_NAME': item.get('OBJECT_NAME', ''),
                        'EPOCH': item.get('EPOCH', ''),
                        'MEAN_MOTION': item.get('MEAN_MOTION', ''),
                        'ECCENTRICITY': item.get('ECCENTRICITY', ''),
                        'INCLINATION': item.get('INCLINATION', ''),
                        'RA_OF_ASC_NODE': item.get('RA_OF_ASC_NODE', ''),
                        'ARG_OF_PERICENTER': item.get('ARG_OF_PERICENTER', ''),
                        'MEAN_ANOMALY': item.get('MEAN_ANOMALY', ''),
                        'BSTAR': item.get('BSTAR', ''),
                        '_source': 'space_track',
                        '_type': 'debris_tle'
                    }
                    filtered_data.append(filtered_item)
                
                print(f"✅ TLE basura espacial: {len(filtered_data)} objetos")
                return filtered_data
            return []
        except Exception as e:
            print(f"❌ Error TLE basura espacial: {e}")
            return []
    
    def extract_critical_cdm(self):
        """Extraer CDM críticos (últimos 7 días, alta probabilidad)"""
        print("⚠️ Extrayendo CDM críticos...")
        
        try:
            # CDM de los últimos 7 días con alta probabilidad de colisión
            url = f"{self.base_url}/basicspacedata/query/class/cdm_public/TCA/%3Enow-7/PC/%3E0.001/format/json/orderby/TCA%20DESC"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Filtrar solo campos esenciales para prevención
                filtered_data = []
                for item in data:
                    filtered_item = {
                        'CDM_ID': item.get('CDM_ID', ''),
                        'TCA': item.get('TCA', ''),
                        'PC': item.get('PC', ''),
                        'PC_UNCERTAINTY': item.get('PC_UNCERTAINTY', ''),
                        'MISS_DISTANCE': item.get('MISS_DISTANCE', ''),
                        'MISS_DISTANCE_UNCERTAINTY': item.get('MISS_DISTANCE_UNCERTAINTY', ''),
                        'OBJECT1_ID': item.get('OBJECT1_ID', ''),
                        'OBJECT1_NAME': item.get('OBJECT1_NAME', ''),
                        'OBJECT2_ID': item.get('OBJECT2_ID', ''),
                        'OBJECT2_NAME': item.get('OBJECT2_NAME', ''),
                        'RELATIVE_VELOCITY': item.get('RELATIVE_VELOCITY', ''),
                        'RELATIVE_VELOCITY_UNCERTAINTY': item.get('RELATIVE_VELOCITY_UNCERTAINTY', ''),
                        '_source': 'space_track',
                        '_type': 'critical_cdm'
                    }
                    filtered_data.append(filtered_item)
                
                print(f"✅ CDM críticos: {len(filtered_data)} eventos")
                return filtered_data
            return []
        except Exception as e:
            print(f"❌ Error CDM críticos: {e}")
            return []
    
    def logout(self):
        """Cerrar sesión"""
        try:
            if self.authenticated:
                self.session.get(f"{self.base_url}/ajaxauth/logout")
                self.authenticated = False
        except:
            pass

class EssentialExtractor:
    """Extractor esencial para prevención de colisiones"""
    
    def __init__(self):
        self.credentials = load_credentials()
        self.space_track = None
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Verificar credenciales
        if not self.credentials.get('SPACE_TRACK_USERNAME') or not self.credentials.get('SPACE_TRACK_PASSWORD'):
            print("❌ ERROR: Credenciales de Space-Track no encontradas en variables de entorno")
            raise Exception("Credenciales no encontradas")
    
    def extract_all_critical_data(self):
        """Extraer todos los datos críticos"""
        print("🚀 Iniciando extracción de datos críticos para prevención de colisiones...")
        
        # Inicializar Space-Track
        self.space_track = SpaceTrackExtractor(
            self.credentials['SPACE_TRACK_USERNAME'],
            self.credentials['SPACE_TRACK_PASSWORD']
        )
        
        # Autenticar
        if not self.space_track.authenticate():
            print("❌ No se pudo autenticar con Space-Track")
            return False
        
        try:
            # Extraer datos críticos
            active_tle = self.space_track.extract_active_tle()
            debris_tle = self.space_track.extract_debris_tle()
            critical_cdm = self.space_track.extract_critical_cdm()
            
            # Combinar todos los datos
            all_data = {
                'active_tle': active_tle,
                'debris_tle': debris_tle,
                'critical_cdm': critical_cdm,
                'metadata': {
                    'extraction_time': datetime.now().isoformat(),
                    'total_active_tle': len(active_tle),
                    'total_debris_tle': len(debris_tle),
                    'total_critical_cdm': len(critical_cdm),
                    'total_records': len(active_tle) + len(debris_tle) + len(critical_cdm)
                }
            }
            
            return all_data
            
        finally:
            self.space_track.logout()
    
    def save_data(self, data):
        """Guardar datos en archivos CSV separados"""
        print("💾 Guardando datos críticos...")
        
        # Crear directorio de resultados
        output_dir = f"datos_criticos_{self.timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Guardar TLE activos
        if data['active_tle']:
            active_tle_file = f"{output_dir}/tle_activos.csv"
            with open(active_tle_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data['active_tle'][0].keys())
                writer.writeheader()
                writer.writerows(data['active_tle'])
            print(f"✅ TLE activos guardados: {active_tle_file}")
        
        # Guardar TLE basura espacial
        if data['debris_tle']:
            debris_tle_file = f"{output_dir}/tle_basura_espacial.csv"
            with open(debris_tle_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data['debris_tle'][0].keys())
                writer.writeheader()
                writer.writerows(data['debris_tle'])
            print(f"✅ TLE basura espacial guardados: {debris_tle_file}")
        
        # Guardar CDM críticos
        if data['critical_cdm']:
            cdm_file = f"{output_dir}/cdm_criticos.csv"
            with open(cdm_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data['critical_cdm'][0].keys())
                writer.writeheader()
                writer.writerows(data['critical_cdm'])
            print(f"✅ CDM críticos guardados: {cdm_file}")
        
        # Guardar metadata
        metadata_file = f"{output_dir}/metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(data['metadata'], f, indent=2, ensure_ascii=False)
        print(f"✅ Metadata guardada: {metadata_file}")
        
        return output_dir
    
    def show_stats(self, data, return_text=False):
        """Mostrar estadísticas detalladas"""
        metadata = data['metadata']
        
        # Análisis de CDM críticos
        high_risk = [cdm for cdm in data['critical_cdm'] if float(cdm.get('PC', 0)) > 0.01]
        medium_risk = [cdm for cdm in data['critical_cdm'] if 0.001 < float(cdm.get('PC', 0)) <= 0.01]
        
        if return_text:
            return {
                "high_risk": len(high_risk),
                "medium_risk": len(medium_risk),
                "low_risk": len(data['critical_cdm']) - len(high_risk) - len(medium_risk),
                "total": metadata['total_records']
            }
        
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS DE EXTRACCIÓN CRÍTICA")
        print("="*60)
        print(f"🕐 Tiempo de extracción: {metadata['extraction_time']}")
        print(f"📡 TLE Satélites Activos: {metadata['total_active_tle']:,}")
        print(f"🗑️ TLE Basura Espacial: {metadata['total_debris_tle']:,}")
        print(f"⚠️ CDM Críticos: {metadata['total_critical_cdm']:,}")
        print(f"📈 Total de Registros: {metadata['total_records']:,}")
        
        # Análisis de CDM críticos
        if data['critical_cdm']:
            print("\n🔍 ANÁLISIS DE CDM CRÍTICOS:")
            print(f"   🔴 Alto riesgo (PC > 1%): {len(high_risk)}")
            print(f"   🟡 Riesgo medio (0.1% < PC ≤ 1%): {len(medium_risk)}")
            print(f"   🟢 Riesgo bajo (PC ≤ 0.1%): {len(data['critical_cdm']) - len(high_risk) - len(medium_risk)}")
        
        print("="*60)
    
    def run(self):
        """Ejecutar extracción completa con salida estructurada"""
        data = self.extract_all_critical_data()
        if not data:
            raise Exception("Error en la extracción")
        return {
            "metadata": data["metadata"],
            "stats": self.show_stats(data, return_text=True),
            "csv_output": self.save_data(data)
        } 