pipeline {
  agent { docker { image 'python:3.7.2' } }
  environment {HOME = '/tmp'}
  stages {
    // First stage , get files from your GitHub repository.
    stage('Git'){
        steps{
            checkout scm
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