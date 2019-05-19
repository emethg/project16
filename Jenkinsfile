pipeline {
    agent { docker { image 'python:3.6.8' } }
    stages {
    stage('Git') {
      // Get some code from a GitHub repository
      steps{
          withEnv(["HOME=${env.WORKSPACE}"]) {
           git branch: 'emethsp3', url: 'https://github.com/emethg/project16.git'
      }
      }
   }

   stage('Requirements'){
          steps{
              withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip3.6 install --user -U -r requirements.txt'
              }
          }
   }

    stage('Run Django'){
          steps{
               withEnv(["HOME=${env.WORKSPACE}"]) {
               sh "python manage.py runserver &"
               }
          }
    }
    stage('Run Tests'){
          steps{
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh"""
                    cd ${WORKSPACE}
                    python manage.py test &
                    """
              }
          }
    }
    stage('Results') {
       steps{
            junit allowEmptyResults: true, testResults: '*/mysite/.xml'

       }
    }


}
}
