pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'izojuanid.azurecr.io/flask-curd-app'
        KUBERNETES_NAMESPACE = 'default'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push to ACR') {
            steps {
                script {
                    docker.withRegistry('https://izojuanid.azurecr.io', 'acr-credentials') {
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push("latest")
                    }
                }
            }
        }

        stage('Deploy to AKS') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh "helm upgrade --install flask-curd-app ./flask-app --set image.tag=${BUILD_NUMBER} --namespace ${KUBERNETES_NAMESPACE}"
                    }
                }
            }
        }
    }
}
