# Script de despliegue automatizado a Azure App Service
# Requiere Azure CLI instalado

Write-Host "🚀 Desplegando Satellite Collision API a Azure..." -ForegroundColor Green

# Verificar si Azure CLI está instalado
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI no encontrado. Instálalo desde: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Variables de configuración
$RESOURCE_GROUP = "satellite-api-rg"
$APP_NAME = "satellite-collision-api"
$LOCATION = "East US"
$PLAN_NAME = "satellite-api-plan"

Write-Host "📋 Configuración:" -ForegroundColor Yellow
Write-Host "   Resource Group: $RESOURCE_GROUP" -ForegroundColor White
Write-Host "   App Service: $APP_NAME" -ForegroundColor White
Write-Host "   Location: $LOCATION" -ForegroundColor White

# Crear Resource Group
Write-Host "`n🔧 Creando Resource Group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# Crear App Service Plan
Write-Host "📦 Creando App Service Plan..." -ForegroundColor Yellow
az appservice plan create --name $PLAN_NAME --resource-group $RESOURCE_GROUP --location $LOCATION --sku B1 --is-linux

# Crear App Service
Write-Host "🌐 Creando App Service..." -ForegroundColor Yellow
az webapp create --resource-group $RESOURCE_GROUP --plan $PLAN_NAME --name $APP_NAME --runtime "PYTHON|3.10"

# Configurar startup command
Write-Host "⚙️ Configurando startup command..." -ForegroundColor Yellow
az webapp config set --resource-group $RESOURCE_GROUP --name $APP_NAME --startup-file "./startup.sh"

# Configurar variables de entorno
Write-Host "🔐 Configurando variables de entorno..." -ForegroundColor Yellow
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME --settings WEBSITES_PORT=8000

Write-Host "`n✅ Despliegue completado!" -ForegroundColor Green
Write-Host "🌐 Tu API estará disponible en: https://$APP_NAME.azurewebsites.net" -ForegroundColor Cyan
Write-Host "📚 Documentación: https://$APP_NAME.azurewebsites.net/docs" -ForegroundColor Cyan

Write-Host "`n📝 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Conecta tu repositorio Git a Azure" -ForegroundColor White
Write-Host "2. Configura las credenciales de Space-Track en Azure" -ForegroundColor White
Write-Host "3. Haz push de tu código para desplegar automáticamente" -ForegroundColor White 