pipeline {
    agent any
    
    environment {
        // Docker Hub credentials configured in Jenkins
        DOCKER_CREDENTIALS_ID = 'docker-hub-creds'
        IMAGE_NAME = 'samir3112/hotel-management'
        KUBE_CONFIG_CREDENTIALS_ID = 'kubeconfig'  // your K8s config credential in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub or your repo
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${env.IMAGE_NAME}:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Use your kubeconfig credential to access K8s cluster
                withKubeConfig([credentialsId: KUBE_CONFIG_CREDENTIALS_ID]) {
                    // Apply k8s manifests from k8s/ folder
                    sh 'kubectl apply -f k8s/deployment.yaml'
                    sh 'kubectl apply -f k8s/service.yaml'
                }
            }
        }
    }
}
