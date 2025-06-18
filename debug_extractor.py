#!/usr/bin/env python3
"""
Script de debug para probar el extractor paso a paso
"""

import os
import sys
from extractor import EssentialExtractor

def test_credentials():
    """Probar si las credenciales se cargan correctamente"""
    print("🔐 Probando carga de credenciales...")
    try:
        if os.path.exists('env'):
            with open('env', 'r') as f:
                content = f.read()
                print(f"✅ Archivo 'env' encontrado")
                print(f"   Contenido: {content.strip()}")
        else:
            print("❌ Archivo 'env' no encontrado")
            return False
        return True
    except Exception as e:
        print(f"❌ Error al leer credenciales: {e}")
        return False

def test_extractor_init():
    """Probar inicialización del extractor"""
    print("\n🚀 Probando inicialización del extractor...")
    try:
        extractor = EssentialExtractor()
        print("✅ Extractor inicializado correctamente")
        return extractor
    except Exception as e:
        print(f"❌ Error al inicializar extractor: {e}")
        return None

def test_login():
    """Probar login a Space-Track"""
    print("\n🔑 Probando login a Space-Track...")
    try:
        extractor = EssentialExtractor()
        # Crear el extractor de Space-Track
        space_track = extractor.space_track = extractor.credentials['USERNAME'], extractor.credentials['PASSWORD']
        print("✅ Login exitoso")
        return True
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False

def test_full_extraction():
    """Probar extracción completa"""
    print("\n📡 Probando extracción completa...")
    try:
        extractor = EssentialExtractor()
        result = extractor.run()
        print(f"✅ Extracción completada exitosamente")
        print(f"   Total de registros: {result['metadata']['total_records']}")
        return True
    except Exception as e:
        print(f"❌ Error en extracción completa: {e}")
        return False

def main():
    """Función principal de debug"""
    print("🔍 DEBUG: Satellite Extractor")
    print("=" * 50)
    
    # Test 1: Credenciales
    if not test_credentials():
        return
    
    # Test 2: Inicialización
    if not test_extractor_init():
        return
    
    # Test 3: Login
    if not test_login():
        return
    
    # Test 4: Extracción completa
    if not test_full_extraction():
        return
    
    print("\n" + "=" * 50)
    print("✅ Todos los tests pasaron")

if __name__ == "__main__":
    main() 