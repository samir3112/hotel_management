pipeline {
  agent {
    kubernetes {
      yamlFile 'kaniko-agent.yaml'
    }
  }

  environment {
    DOCKER_IMAGE = "samir3112/hotel-management:latest"
    DOCKER_CONFIG = "/kaniko/.docker/"
  }

  stages {
    stage('Clone Repo') {
      steps {
        git credentialsId: 'GIT_TOKEN', url: 'https://github.com/samir3112/hotel_management.git', branch: 'main'
      }
    }

    stage('Build Docker Image with Kaniko') {
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor \
              --dockerfile=Dockerfile \
              --context=`pwd` \
              --destination=$DOCKER_IMAGE \
              --oci-layout-path=/kaniko/output \
              --skip-tls-verify \
              --verbosity=info
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh 'kubectl apply -f k8s/deployment.yaml'
        sh 'kubectl apply -f k8s/service.yaml'
      }
    }
  }
}
