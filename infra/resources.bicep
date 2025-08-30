@description('Name of the environment')
param suffixName string

@description('Azure region for resources')
param location string = resourceGroup().location

@secure()
param apiKey string

@secure()
param apiEndpoint string

@description('Docker image for the frontend app service')
param frontendDockerImage string

@description('Docker image for the backend app service')
param backendDockerImage string

@description('Tags to apply to all resources')
param tags object

// App Service Plan using Azure Verified Module
module appServicePlan 'br/public:avm/res/web/serverfarm:0.3.0' = {
  name: 'appServicePlan'
  params: {
    name: 'asp-index-${suffixName}'
    location: location
    skuName: 'B1'
    kind: 'Linux'
    tags: tags
  }
}

module backendAppService 'br/public:avm/res/web/site:0.11.0' = {
  name: 'backendAppService'
  params: {
    name: 'app-index-backend-${suffixName}'
    location: location
    kind: 'app,linux,container'
    serverFarmResourceId: appServicePlan.outputs.resourceId
    siteConfig: {
      alwaysOn: false
      linuxFxVersion: 'DOCKER|${backendDockerImage}'
      appSettings: [
        {
          name: 'API_KEY'
          value: apiKey
        }
        {
          name: 'API_ENDPOINT'
          value: apiEndpoint
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
      ]
    }
    httpsOnly: true
    tags: tags
  }
}

// App Service with sidecar using Azure Verified Module
module frontendAppService 'br/public:avm/res/web/site:0.11.0' = {
  name: 'frontendAppService'
  params: {
    name: 'app-index-frontend-${suffixName}'
    location: location
    kind: 'app,linux,container'
    serverFarmResourceId: appServicePlan.outputs.resourceId
    siteConfig: {
      alwaysOn: false
      linuxFxVersion: 'DOCKER|${frontendDockerImage}'
      appSettings: [
        {
          name: 'VITE_API_BASE_URL'
          value: 'https://${backendAppService.outputs.defaultHostname}'
        }
        {
          name: 'WEBSITES_PORT'
          value: '5000'
        }
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
      ]
    }
    httpsOnly: true
    tags: tags
  }
}

// Outputs
output frontendAppServiceUrl string = 'https://${frontendAppService.outputs.defaultHostname}'
output frontendAppServiceName string = frontendAppService.outputs.name
output backendAppServiceUrl string = 'https://${backendAppService.outputs.defaultHostname}'
output backendAppServiceName string = backendAppService.outputs.name
