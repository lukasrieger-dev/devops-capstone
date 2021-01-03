pipeline {
  agent any
  
  environment {
    AWS_REGION = 'eu-central-1'
    EKS_CLUSTER_NAME = 'nnnnn'
    DOCKER_IMAGE_NAME = 'nnn'
  }

  stages {
    stage('Check system') {
      steps {
          sh 'pwd'
          sh 'ls -la'
          sh 'python3 --version'
          sh 'pip3 --version'
          sh 'which python3'
      }
    }

    stage('lint') {
      steps {
        dir("api"){
            sh """
            python3 -m venv devops
            . devops/bin/activate
            make install
            make test
            make lint
            """
        }
      }
    } 
  }

  post { 
    always { 
        echo 'Done.'
    }
  }  
}