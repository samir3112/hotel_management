pipeline {
  agent {
    kubernetes {
      yamlFile 'kaniko-agent.yaml'
    }
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
              --context `pwd` \
              --dockerfile Dockerfile \
              --destination=docker.io/samir3112/hotel-management:latest\
              --insecure \
              --skip-tls-verify
          '''
        }
      }
    }

    stage('Deploy to K8s') {
      steps {
        sh 'kubectl apply -f k8s/deployment.yaml'
      }
    }
  }
}
