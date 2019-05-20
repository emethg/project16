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


    stage('PEP8 style check') {
            steps {
                echo "PEP8 style check"
                sh  ''' source activate ${BUILD_TAG}
                        pylint --disable=C irisvmpy || true
                    '''
            }
        }

    stage('Code Coverage') {
            steps {
                echo "Code Coverage"
                sh  ''' source activate ${BUILD_TAG}
                        coverage run irisvmpy/iris.py 1 1 2 3
                        python -m coverage xml -o ./reports/coverage.xml
                    '''
            }
            post{
                always{
                    step([$class: 'CoberturaPublisher',
                                   autoUpdateHealth: false,
                                   autoUpdateStability: false,
                                   coberturaReportFile: 'reports/coverage.xml',
                                   failNoReports: false,
                                   failUnhealthy: false,
                                   failUnstable: false,
                                   maxNumberOfBuilds: 10,
                                   onlyStable: false,
                                   sourceEncoding: 'ASCII',
                                   zoomCoverageChart: false])
                }
            }
        }

}
}