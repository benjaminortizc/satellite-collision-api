from fastapi import FastAPI, HTTPException
from extractor import EssentialExtractor
import uvicorn
from typing import Dict, Any
import traceback
import logging
import os

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003) 