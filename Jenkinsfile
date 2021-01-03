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
        sh 'make setup'
        sh 'make install'             
      }
    }
     
    stage('Run tests') {
      steps {
        sh 'make tests'      
      }
    }

    stage('Run lint') {
      steps {
        sh 'make lint'               
      }
    }  
  }

  post { 
      always { 
          echo 'Done.'
      }
  }  
}