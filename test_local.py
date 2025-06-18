#!/usr/bin/env python3
"""
Script para probar la API localmente
"""

import requests
import json
import time

def test_api():
    """Probar todos los endpoints de la API"""
    base_url = "http://localhost:8000"
    
    print("🚀 Probando Satellite Collision Avoidance API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Probando health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Health check: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Health check: Error de conexión - {e}")
    
    # Test 2: Root endpoint
    print("\n2. Probando endpoint raíz...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint: OK")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Root endpoint: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint: Error de conexión - {e}")
    
    # Test 3: Extract endpoint (puede tomar tiempo)
    print("\n3. Probando extracción de datos...")
    print("   ⚠️  Esto puede tomar varios minutos...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/extract")
        end_time = time.time()
        
        if response.status_code == 200:
            print("✅ Extracción: OK")
            data = response.json()
            print(f"   Tiempo de ejecución: {end_time - start_time:.2f} segundos")
            print(f"   Estado: {data.get('status')}")
            print(f"   Total de registros: {data.get('metadata', {}).get('total_records', 'N/A')}")
            print(f"   CDM críticos: {data.get('metadata', {}).get('critical_cdm', 'N/A')}")
            print(f"   Directorio de salida: {data.get('csv_output_dir', 'N/A')}")
        else:
            print(f"❌ Extracción: Error {response.status_code}")
            print(f"   Detalle: {response.text}")
    except Exception as e:
        print(f"❌ Extracción: Error de conexión - {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas completadas")

if __name__ == "__main__":
    test_api() 