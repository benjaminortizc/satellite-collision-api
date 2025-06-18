# Script de despliegue automatizado a Azure App Service
# Requiere Azure CLI instalado

Write-Host "🚀 Desplegando Satellite Collision API a Azure..."

# Verificar si Azure CLI está instalado
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI encontrado"
} catch {
    Write-Host "❌ Azure CLI no encontrado. Instálalo desde: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Variables de configuración
$RESOURCE_GROUP = "satellite-api-rg"
$APP_NAME = "satellite-collision-api"
$LOCATION = "eastus"
$PLAN_NAME = "satellite-api-plan"

Write-Host "📋 Configuración:"
Write-Host "   Resource Group: $RESOURCE_GROUP"
Write-Host "   App Service: $APP_NAME"
Write-Host "   Location: $LOCATION"

# Crear Resource Group
Write-Host "`n🔧 Creando Resource Group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Crear App Service Plan
Write-Host "📦 Creando App Service Plan..."
az appservice plan create --name $PLAN_NAME --resource-group $RESOURCE_GROUP --location $LOCATION --sku B1 --is-linux

# Crear App Service (runtime correcto: PYTHON:3.10)
Write-Host "🌐 Creando App Service..."
az webapp create --resource-group $RESOURCE_GROUP --plan $PLAN_NAME --name $APP_NAME --runtime "PYTHON:3.10"

# Configurar startup command
Write-Host "⚙️ Configurando startup command..."
az webapp config set --resource-group $RESOURCE_GROUP --name $APP_NAME --startup-file "./startup.sh"

# Configurar variables de entorno
Write-Host "🔐 Configurando variables de entorno..."
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME --settings WEBSITES_PORT=8000

Write-Host "`n✅ Despliegue completado!"
Write-Host "🌐 Tu API estará disponible en: https://$APP_NAME.azurewebsites.net"
Write-Host "📚 Documentación: https://$APP_NAME.azurewebsites.net/docs"

Write-Host "`n📝 Próximos pasos:"
Write-Host "1. Conecta tu repositorio Git a Azure"
Write-Host "2. Configura las credenciales de Space-Track en Azure"
Write-Host "3. Haz push de tu código para desplegar automáticamente" 