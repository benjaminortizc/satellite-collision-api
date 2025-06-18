# Satellite Collision Avoidance API

API para extraer y analizar datos de satélites, basura espacial y conjunciones críticas usando FastAPI.

## 🚀 Características

- **TLE Activos**: Extracción de elementos orbitales de satélites activos
- **Basura Espacial**: Identificación de objetos de desecho espacial
- **CDM Críticos**: Análisis de riesgo de colisión entre objetos
- **API REST**: Interfaz web para consultar datos
- **Documentación Automática**: Swagger UI integrado

## 📋 Requisitos

- Python 3.8+
- Credenciales de Space-Track.org
- FastAPI y dependencias

## 🔧 Instalación

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd satellite-extractor-api
```

2. **Crear archivo de credenciales:**
```bash
# Crear archivo 'env' con tus credenciales
echo "USERNAME=tu_usuario" > env
echo "PASSWORD=tu_password" >> env
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Uso Local

1. **Ejecutar la API:**
```bash
python main.py
```

2. **Acceder a la documentación:**
```
http://localhost:8000/docs
```

3. **Probar endpoints:**
- `GET /`: Información general
- `GET /health`: Estado del servicio
- `GET /extract`: Ejecutar extracción completa

## ☁️ Despliegue en Azure

### Opción 1: Azure App Service

1. **Crear App Service:**
   - Plataforma: Linux
   - Runtime: Python 3.10+
   - Startup Command: `./startup.sh`

2. **Configurar variables de entorno:**
   - `USERNAME`: Tu usuario de Space-Track
   - `PASSWORD`: Tu contraseña de Space-Track

3. **Desplegar código:**
   - Usar Azure CLI, VSCode o GitHub Actions

### Opción 2: Azure Container Instances

1. **Crear Dockerfile:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Construir y desplegar:**
```bash
az container create --resource-group myResourceGroup \
  --name satellite-api --image myregistry.azurecr.io/satellite-api:latest \
  --ports 8000 --dns-name-label satellite-api
```

## 📊 Estructura de Datos

### Respuesta del endpoint `/extract`:

```json
{
  "status": "success",
  "metadata": {
    "extraction_date": "2024-01-15T10:30:00",
    "total_tle": 5000,
    "total_debris": 25000,
    "total_cdm": 150,
    "critical_cdm": 12,
    "total_records": 30150
  },
  "stats": {
    "high_risk": 5,
    "medium_risk": 4,
    "low_risk": 3,
    "total": 30150
  },
  "csv_output_dir": "datos_criticos_20240115_103000"
}
```

## 🔒 Seguridad

- Las credenciales se almacenan en variables de entorno
- El archivo `env` está en `.gitignore`
- La API incluye manejo de errores robusto

## 📝 Archivos Generados

La extracción crea los siguientes archivos CSV:

- `tle_activos.csv`: Elementos orbitales de satélites activos
- `basura_espacial.csv`: Objetos de desecho espacial
- `cdm_completos.csv`: Todos los mensajes de conjunción
- `analisis_riesgo.csv`: Análisis de riesgo de colisión
- `cdm_criticos.csv`: Conjunciones de alto riesgo
- `resumen_extraccion.csv`: Metadatos de la extracción

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🆘 Soporte

Para problemas o preguntas:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo

---

**Nota**: Esta API requiere credenciales válidas de Space-Track.org para funcionar correctamente. 