pipeline {
  agent any
  
  environment {
    AWS_REGION = 'eu-central-1'
    EKS_CLUSTER_NAME = 'udacity-cloud-devops-capstone'
    DOCKER_IMAGE_NAME = 'udacity-cloud-devops-capstone'
  }

  stages {
    stage('System Check') {
        steps {
            sh 'pwd'
            sh 'ls -la'
            sh 'python3 --version'
            sh 'pip3 --version'
            withEnv(["HOME=${env.WORKSPACE}"]) {
                sh 'printenv'
            }
        }
    }

    stage('Clone Git Repo') {
      steps {
        git 'https://github.com/lukasrieger-dev/devops-capstone.git'
      }
    }

    stage('Install dependencies') {
      steps {
        sh 'make setup'
        sh 'make install'
        sh 'pip3 list'
        sh 'make test'
        sh 'make lint'              
      }
    }
     
    stage('Run tests') {
      steps {
        sh 'make test'      
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