pipeline {
  agent {
    kubernetes {
      inheritFrom 'kaniko-template' // Defined in Jenkins UI
    }
  }

  environment {
    IMAGE_NAME = 'samir3112/hotel-management:latest'
  }

  stages {
    stage('Clone') {
      steps {
        git 'https://github.com/samir3112/hotel_management.git'
      }
    }

    stage('Build and Push with Kaniko') {
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor \
              --context=dir:///workspace \
              --dockerfile=Dockerfile \
              --destination=${IMAGE_NAME} \
              --insecure \
              --skip-tls-verify
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        container('kubectl') {
          sh 'kubectl apply -f k8s/deployment.yaml'
        }
      }
    }
  }
}
