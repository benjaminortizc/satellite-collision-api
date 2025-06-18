#!/usr/bin/env python3
"""
Script de configuración inicial para Satellite Collision Avoidance API
"""

import os
import sys
import subprocess

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def create_env_file():
    """Crear archivo de credenciales si no existe"""
    if os.path.exists('env'):
        print("✅ Archivo 'env' ya existe")
        return True
    
    print("\n📝 Configuración de credenciales")
    print("Necesitas credenciales de Space-Track.org")
    print("Regístrate en: https://www.space-track.org/auth/signup")
    
    username = input("Usuario de Space-Track: ").strip()
    password = input("Contraseña de Space-Track: ").strip()
    
    if not username or not password:
        print("❌ Credenciales no válidas")
        return False
    
    try:
        with open('env', 'w') as f:
            f.write(f"USERNAME={username}\n")
            f.write(f"PASSWORD={password}\n")
        print("✅ Archivo 'env' creado")
        return True
    except Exception as e:
        print(f"❌ Error al crear archivo 'env': {e}")
        return False

def install_dependencies():
    """Instalar dependencias de Python"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def make_startup_executable():
    """Hacer ejecutable el script de inicio"""
    try:
        os.chmod('startup.sh', 0o755)
        print("✅ Script startup.sh hecho ejecutable")
        return True
    except Exception as e:
        print(f"❌ Error al hacer ejecutable startup.sh: {e}")
        return False

def test_imports():
    """Probar importaciones de módulos"""
    print("\n🧪 Probando importaciones...")
    try:
        import fastapi
        import uvicorn
        import requests
        import pandas
        print("✅ Todas las importaciones exitosas")
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def main():
    """Función principal de configuración"""
    print("🚀 Configuración de Satellite Collision Avoidance API")
    print("=" * 60)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear archivo de credenciales
    if not create_env_file():
        print("\n💡 Puedes crear el archivo 'env' manualmente:")
        print("   USERNAME=tu_usuario")
        print("   PASSWORD=tu_password")
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Hacer ejecutable startup.sh
    make_startup_executable()
    
    # Probar importaciones
    if not test_imports():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Configuración completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Ejecutar la API: python main.py")
    print("2. Abrir en navegador: http://localhost:8000/docs")
    print("3. Probar endpoints: python test_local.py")
    print("\n🌐 Para desplegar en Azure:")
    print("1. Crear App Service en Azure Portal")
    print("2. Configurar startup command: ./startup.sh")
    print("3. Subir código via Git o Azure CLI")

if __name__ == "__main__":
    main() 