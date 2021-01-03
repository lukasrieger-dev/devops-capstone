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
          sh 'whoami'
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
        sh 'docker version'
      }
    }

    stage('Build docker image') {
      steps {
        dir('app') {
          sh 'docker build --tag=${DOCKER_IMAGE_NAME} .'
        }
      }
    }

    stage('Run docker container locally') {
        steps {
            sh 'docker image ls'
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

    stage('Deploy to EKS') {
      steps {
        withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
          script {
            // check if the AWS EKS cluster ARN exists
            def EKS_ARN = sh(
                script: "aws cloudformation list-exports --query \"Exports[?Name=='eksctl-${EKS_CLUSTER_NAME}-cluster::ARN'].Value\" --output text",
                returnStdout: true
            ).trim()
            // create the AWS EKS cluster using eksctl if the ARN doesn't exist
            if (EKS_ARN.isEmpty()) {
                sh """
                eksctl create cluster --name ${EKS_CLUSTER_NAME} \
                                      --version 1.17 \
                                      --nodegroup-name standard-workers \
                                      --node-type t2.medium \
                                      --nodes 2 \
                                      --nodes-min 1 \
                                      --nodes-max 2 \
                                      --node-ami auto \
                                      --region ${AWS_REGION}
                """
                sh 'sleep 2m'  // wait for creation
                // update the value of EKS_ARN after the cluster is created
                EKS_ARN = sh(
                    script: "aws cloudformation list-exports --query \"Exports[?Name=='eksctl-${EKS_CLUSTER_NAME}-cluster::ARN'].Value\" --output text",
                    returnStdout: true
                ).trim()
            }
            sh 'aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME}'
            sh "kubectl config use-context ${EKS_ARN}"
          }
          sh 'kubectl config current-context'
          sh 'kubectl apply -f deployment.yml'
          sh 'kubectl rollout restart deployments/mathsapi'
          sh 'sleep 2m'  // wait for image pulling
          sh 'kubectl get nodes'
        }
      }
    }

    stage('Smoke test') {
      steps {
        withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
          script {
              def EKS_HOSTNAME = sh(
                  script: 'kubectl get svc mathsapi -o jsonpath="{.status.loadBalancer.ingress[*].hostname}"',
                  returnStdout: true
                  ).trim()
              sh "curl ${EKS_HOSTNAME}:8080"
          }
        }
      }
    }

    stage('Check rollout') {
      steps {
        withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
            sh 'kubectl rollout status deployments/mathsapi'
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