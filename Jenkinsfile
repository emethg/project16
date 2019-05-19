pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    // First stage , get files from your GitHub repository.
    stage('Git'){
        steps{
            checkout scm
        }
    }
    stage('Requirements'){
        steps{
            withEnv(["HOME=${env.WORKSPACE}"]) {
                sh 'pip3 install --user -r requirements.txt'
            }
        }
    }
    stage('Run Tests') {
      steps {
        sh 'python manage.py test'
      }
      post {
        always {
          junit 'test-reports/*.xml'
        }
      }
    }
  }
}