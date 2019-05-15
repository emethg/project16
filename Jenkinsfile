pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
  stage('Git') { // Get some code from a GitHub repository
      steps{
        withEnv(["HOME=${env.WORKSPACE}"]) {
          git 'https://github.com/emethg/project16'
        }
      }
  }
   
  stage('Requirements'){
    steps{
      withEnv(["HOME=${env.WORKSPACE}"]) {
        sh 'pip3.7 install --user -U -r requirements.txt'
      }
    }
  }
    
  stage('Run Django'){
    steps{
      withEnv(["HOME=${env.WORKSPACE}"]) {
        sh "python3.7 manage.py runserver &"
      }
    }
  }
  stage('Run Tests'){
    steps{
      withEnv(["HOME=${env.WORKSPACE}"]) {
        sh"""
        cd ${WORKSPACE}
        python manage.py test
        """
              }
          }
  }
  stage('Results') {
    steps{
      junit allowEmptyResults: true, testResults: '**/StartEasy/*.xml'  
    }
  }    
  }
}
