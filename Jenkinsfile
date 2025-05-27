pipeline {
    agent {
        kubernetes {
            yamlFile 'kaniko-agent.yaml'
        }
    }

    environment {
        IMAGE_NAME = "samir3112/hotel-management"
        TAG = "latest"
    }

    stages {
        stage('Clone Code') {
            steps {
                git 'https://github.com/samir3112/hotel_management.git'
            }
        }

        stage('Build & Push Image with Kaniko') {
            steps {
                container('kaniko') {
                    sh '''
                        /kaniko/executor \
                          --dockerfile=/workspace/Dockerfile \
                          --context=dir://workspace/ \
                          --destination=$IMAGE_NAME:$TAG \
                          --verbosity=info
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/flask-deployment.yaml'
                sh 'kubectl apply -f k8s/flask-service.yaml'
            }
        }
    }
}
