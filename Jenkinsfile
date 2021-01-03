pipeline {
  agent any
  
  environment {
    AWS_REGION = 'eu-central-1'
    EKS_CLUSTER_NAME = 'nnnnn'
    DOCKER_IMAGE_NAME = 'udacity-capstone-math-api'
    DOCKER_USER = 'lukasriegerdev'
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

    stage('Check awscli, eksctl, kubectl, docker') {
      steps {
        sh 'aws --version'
        sh 'eksctl version'
        sh 'kubectl version --short --client'
        sh 'sudo docker version'
      }
    }

    stage('Build docker image') {
      steps {
        dir('app') {
          sh 'sudo docker build --tag=${DOCKER_IMAGE_NAME} .'
        }
      }
    }

    stage('Test docker container') {
        steps {
            sh 'sudo docker image ls'
            sh 'docker container ls'
            sh 'docker run -d -p 8000:80 ${DOCKER_IMAGE_NAME}'
            sh 'sleep 2s'
            sh 'curl http://localhost:8000'
            sh 'docker stop $(docker ps -a -q)'
            sh 'docker rm -f $(docker ps -a -q)'
            sh 'docker container ls'
        }
    }

    stage('Push to dockerhub') {
        steps {
            // As documented: https://devops4solutions.com/publish-docker-image-to-dockerhub-using-jenkins-pipeline/
            withDockerRegistry([credentialsId: "dockerhub", url: ""]) {
                sh 'docker tag ${DOCKER_IMAGE_NAME} ${DOCKER_USER}/${DOCKER_IMAGE_NAME}'
                sh 'docker push ${DOCKER_USER}/${DOCKER_IMAGE_NAME}'
            }
            sh 'docker rmi -f $(docker images -q)'
            sh 'docker image ls'
        }
    }

  }


  post { 
    always { 
        echo 'Done.'
    }
  }  
}