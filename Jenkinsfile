pipeline {
  agent any
    
  stages {
    stage('System Check') {
        steps {
            sh 'pwd'
            sh 'ls -la'
            echo 'python environment'
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
        echo '######################'              
        echo 'Building...test'       
        echo '######################'                      
      }
    }
     
    stage('Running Tests') {
      steps {
        echo '######################'              
        echo 'Running tests ...master'          
        echo '######################'               
      }
    }      
  }
  post { 
      always { 
          echo 'Done.'
      }
  }  
}