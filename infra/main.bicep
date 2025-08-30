targetScope = 'subscription'

@description('suffix for environment name, e.g. dev, prod')
param suffixName string

@description('Azure region for resources')
param location string = 'Australia East'

@description('Docker image for the frontend app service')
param frontendDockerImage string = 'koudaiii/indexfrontend:latest'

@description('Docker image for the backend app service')
param backendDockerImage string = 'koudaiii/indexbackend:latest'

@secure()
@description('api key for the app service')
param apiKey string

@secure()
@description('api endpoint for the app service')
param apiEndpoint string

@description('Tags to apply to all resources')
param tags object = {
  project: 'index'
  managed_by: 'bicep'
}

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'rg-index-${suffixName}'
  location: location
  tags: tags
}

// Deploy resources in the resource group
module resources 'resources.bicep' = {
  scope: rg
  name: 'resources'
  params: {
    suffixName: suffixName
    location: location
    frontendDockerImage: frontendDockerImage
    backendDockerImage: backendDockerImage
    tags: tags
    apiKey: apiKey
    apiEndpoint: apiEndpoint
  }
}

// Outputs
output frontendAppServiceUrl string = resources.outputs.frontendAppServiceUrl
output frontendAppServiceName string = resources.outputs.frontendAppServiceName
output backendAppServiceUrl string = resources.outputs.backendAppServiceUrl
output backendAppServiceName string = resources.outputs.backendAppServiceName
output resourceGroupName string = rg.name
