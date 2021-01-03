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

    stage('Install dependencies') {
      steps {
        dir("app"){
            sh """
            python3 -m venv capstone
            . capstone/bin/activate
            make install
            """
        }
      }
    }

    stage('Run tests') {
      steps {
        dir('app'){
          sh 'make tests'
        }
      }
    }

    stage('Lint') {
      steps {
        dir('app') {
          sh 'make lint'
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