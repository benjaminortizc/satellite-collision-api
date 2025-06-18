# Satellite Collision Avoidance API

API para extraer y analizar datos de satélites, basura espacial y conjunciones críticas usando FastAPI.

## 🚀 Características

- **TLE Activos**: Extracción de elementos orbitales de satélites activos
- **Basura Espacial**: Identificación de objetos de desecho espacial
- **CDM Críticos**: Análisis de riesgo de colisión entre objetos
- **API REST**: Interfaz web para consultar datos
- **Documentación Automática**: Swagger UI integrado
- **Despliegue Automático**: CI/CD con Azure

## 📋 Requisitos

- Python 3.8+
- Credenciales de Space-Track.org
- FastAPI y dependencias
- Azure CLI (para despliegue)

## 🔧 Instalación Local

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd satellite-extractor-api
```

2. **Crear archivo de credenciales:**
```bash
# Copiar archivo de ejemplo
cp env.example env
# Editar con tus credenciales reales
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la API:**
```bash
python main.py
```

5. **Acceder a la documentación:**
```
http://localhost:8003/docs
```

## ☁️ Despliegue en Azure

### Opción 1: Despliegue Automático (Recomendado)

1. **Instalar Azure CLI:**
```bash
# Descargar desde: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

2. **Ejecutar script de despliegue:**
```powershell
.\deploy-to-azure.ps1
```

3. **Conectar repositorio Git:**
```bash
# Crear repositorio en GitHub/GitLab
git remote add origin <tu-repositorio-url>
git push -u origin main
```

4. **Configurar credenciales en Azure:**
   - Ve al Portal de Azure
   - App Service > Configuration > Application settings
   - Agregar variables:
     - `USERNAME`: Tu usuario de Space-Track
     - `PASSWORD`: Tu contraseña de Space-Track

### Opción 2: Despliegue Manual

1. **Crear App Service en Azure Portal:**
   - Plataforma: Linux
   - Runtime: Python 3.10+
   - Startup Command: `./startup.sh`

2. **Configurar variables de entorno:**
   - `USERNAME`: Tu usuario de Space-Track
   - `PASSWORD`: Tu contraseña de Space-Track
   - `WEBSITES_PORT`: 8000

3. **Conectar Git:**
   - App Service > Deployment Center
   - Source: GitHub/GitLab
   - Seleccionar repositorio y rama

## 📊 Estructura de Datos

### Respuesta del endpoint `/extract`:

```json
{
  "status": "success",
  "metadata": {
    "extraction_time": "2024-01-15T10:30:00",
    "total_active_tle": 27066,
    "total_debris_tle": 10346,
    "total_critical_cdm": 68,
    "total_records": 37480
  },
  "stats": {
    "high_risk": 5,
    "medium_risk": 12,
    "low_risk": 51,
    "total": 37480
  },
  "csv_output_dir": "datos_criticos_20240115_103000"
}
```

## 🔒 Seguridad

- Las credenciales se almacenan en variables de entorno
- El archivo `env` está en `.gitignore`
- La API incluye manejo de errores robusto
- Autenticación con Space-Track.org

## 📝 Archivos Generados

La extracción crea los siguientes archivos CSV:

- `tle_activos.csv`: Elementos orbitales de satélites activos
- `tle_basura_espacial.csv`: Objetos de desecho espacial
- `cdm_criticos.csv`: Conjunciones de alto riesgo
- `metadata.json`: Metadatos de la extracción

## 🌐 Endpoints Disponibles

- `GET /`: Información general
- `GET /health`: Estado del servicio
- `GET /extract`: Ejecutar extracción completa
- `GET /docs`: Documentación interactiva

## 🚀 CI/CD con GitHub Actions

El proyecto incluye configuración automática para GitHub Actions:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: satellite-collision-api
        package: .
```

## 📈 Monitoreo

- **Logs**: Disponibles en Azure Portal > App Service > Log stream
- **Métricas**: CPU, memoria, requests en Azure Portal
- **Health Check**: Endpoint `/health` para monitoreo

## 🆘 Solución de Problemas

### Error de credenciales:
- Verificar variables de entorno en Azure
- Comprobar credenciales de Space-Track.org

### Error de puerto:
- Verificar `WEBSITES_PORT=8000` en configuración
- Revisar startup command

### Error de dependencias:
- Verificar `requirements.txt`
- Revisar logs de build en Azure

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
- Revisar logs en Azure Portal
- Contactar al equipo de desarrollo

---

**Nota**: Esta API requiere credenciales válidas de Space-Track.org para funcionar correctamente. 