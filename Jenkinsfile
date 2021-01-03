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

    stage('Install dependencies, test, lint') {
      steps {
        dir('app'){
            sh """
            python3 -m venv capstone
            . capstone/bin/activate
            make install
            make tests
            make lint
            """
        }
      }
    }

    stage('verify aws-cli v2, eksctl, kubectl') {
      steps {
        sh 'aws --version'
        sh 'eksctl version'
        sh 'kubectl version --short --client'
      }
    }

  }


  post { 
    always { 
        echo 'Done.'
    }
  }  
}