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

    stage('Cloning Git Repo') {
      steps {
        git 'https://github.com/lukasrieger-dev/devops-capstone.git'
      }
    }

    stage('Install dependencies') {
      steps {
        dir('api') {
          sh 'make setup'
          sh 'make install'
        }                       
      }
    }
     
    stage('Run tests') {
      steps {
        dir('test') {
          make test
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