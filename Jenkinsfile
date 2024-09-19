pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'snakegameacr.azurecr.io/snake-game'
        AZURE_CREDS = credentials('azure-credentials')
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
            }
        }
        
        stage('Test') {
            steps {
                // Add your test commands here
                sh 'echo "Running tests..."'
            }
        }
        
        stage('Push') {
            steps {
                sh 'az login --service-principal -u $AZURE_CREDS_CLIENT_ID -p $AZURE_CREDS_CLIENT_SECRET -t $AZURE_CREDS_TENANT_ID'
                sh 'az acr login --name snakegameacr'
                sh 'docker push $DOCKER_IMAGE:$BUILD_NUMBER'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'az aks get-credentials --resource-group snake-game-resources --name snake-game-aks'
                sh "helm upgrade --install snake-game ./helm/snake-game --set image.tag=$BUILD_NUMBER"
            }
        }
    }
    
    post {
        always {
            sh 'docker rmi $DOCKER_IMAGE:$BUILD_NUMBER'
        }
    }
}
