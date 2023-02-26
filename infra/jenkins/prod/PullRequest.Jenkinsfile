pipeline {
    agent any

    stages {
        stage('Linting test') {
            steps {
              sh '''
                pip3 install pylint
                python3 -m pylint **/*.py
              '''
            }
        }
    }
}