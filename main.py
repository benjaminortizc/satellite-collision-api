from fastapi import FastAPI, HTTPException
from extractor import EssentialExtractor
import uvicorn
from typing import Dict, Any
import traceback
import logging
import os
import glob
from fastapi.responses import FileResponse

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Satellite Collision Avoidance API",
    description="API para extraer TLE activos, basura espacial y CDM críticos.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "API para prevención de colisiones satelitales"}

@app.get("/extract")
def extract_data():
    try:
        logger.info("Iniciando extracción de datos...")
        extractor = EssentialExtractor()
        logger.info("Extractor inicializado correctamente")
        
        result = extractor.run()
        logger.info("Extracción completada exitosamente")
        
        return {
            "status": "success",
            "metadata": result["metadata"],
            "stats": result["stats"],
            "csv_output_dir": result["csv_output"]
        }
    except Exception as e:
        logger.error(f"Error en extracción: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error en extracción: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "satellite-extractor-api"}

@app.get("/env-debug")
def env_debug():
    return {
        "SPACE_TRACK_USERNAME": os.getenv("SPACE_TRACK_USERNAME"),
        "SPACE_TRACK_PASSWORD": os.getenv("SPACE_TRACK_PASSWORD")
    }

@app.get("/files")
def list_files():
    """Listar archivos CSV disponibles"""
    try:
        # Buscar directorios de datos críticos
        data_dirs = glob.glob("datos_criticos_*")
        if not data_dirs:
            return {"message": "No hay archivos de datos disponibles", "files": []}
        
        # Obtener el directorio más reciente
        latest_dir = max(data_dirs, key=os.path.getctime)
        
        # Listar archivos en el directorio
        files = []
        for file_path in glob.glob(f"{latest_dir}/*"):
            if os.path.isfile(file_path):
                files.append({
                    "name": os.path.basename(file_path),
                    "size": os.path.getsize(file_path),
                    "path": file_path
                })
        
        return {
            "directory": latest_dir,
            "files": files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando archivos: {str(e)}")

@app.get("/download/{filename}")
def download_file(filename: str):
    """Descargar archivo específico"""
    try:
        # Buscar el archivo en el directorio más reciente
        data_dirs = glob.glob("datos_criticos_*")
        if not data_dirs:
            raise HTTPException(status_code=404, detail="No hay archivos disponibles")
        
        latest_dir = max(data_dirs, key=os.path.getctime)
        file_path = os.path.join(latest_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Archivo {filename} no encontrado")
        
        return FileResponse(file_path, filename=filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error descargando archivo: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003) 