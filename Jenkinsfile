pipeline {
  agent any
    
  stages {
        
    stage('Cloning Git Repo') {
      steps {
        git 'https://github.com/lukasrieger-dev/devops-capstone.git'
      }
    }
    stage('Install dependencies') {
      steps {
        echo '######################'              
        echo 'Building...'       
        echo '######################'                      
      }
    }
     
    stage('Running Tests') {
      steps {
        echo '######################'              
        echo 'Running tests ...'          
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