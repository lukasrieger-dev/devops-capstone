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
            // wait 2 seconds for the container to be ready, before we call it
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
        // In order to be able to connect to AWS use the Jenkins Plugins:
        // https://support.cloudbees.com/hc/en-us/articles/360027893492-How-To-Authenticate-to-AWS-with-the-Pipeline-AWS-Plugin
        withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
          script {
            // check if the AWS EKS cluster ARN exists
            def EKS_ARN = sh(
                script: "aws cloudformation list-exports --query \"Exports[?Name=='eksctl-${EKS_CLUSTER_NAME}-cluster::ARN'].Value\" --output text",
                returnStdout: true
            ).trim()
            // create the AWS EKS cluster using eksctl if the ARN doesn't exist
            if (EKS_ARN.isEmpty()) {
                // https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html
                sh """
                eksctl create cluster --name ${EKS_CLUSTER_NAME} --version 1.18 --nodegroup-name workers --node-type t2.medium \
                                      --nodes 2 --nodes-min 2 --nodes-max 3 --node-ami auto --region ${AWS_REGION}
                """
                // wait 1 minutes because cluster creation takes some time
                sh 'sleep 1m'
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
          sh 'kubectl get pods'
          sh 'kubectl apply -f deployment.yml'
          //sh 'kubectl rollout restart deployments/mathsapi'
          sh 'sleep 1m'
          sh 'kubectl get pods'
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
              sh "echo ${EKS_HOSTNAME}"
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
        echo 'Done. Pipeline finished successfully.'
    }
  }  
}