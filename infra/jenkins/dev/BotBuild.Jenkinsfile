pipeline {
    agent none

    stages {
        stage('Docker login') {
            agent {
                docker {
                    image 'docker'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh 'aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/n5h8m9x0'
            }
        }
        stage('Build and Deploy') {
            agent {
                docker {
                    image 'public.ecr.aws/n5h8m9x0/jenkins-project-cicd:latest'
                    args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh 'docker build -t jenkins-project-dev -f ./bot/Dockerfile .'
                sh 'docker tag jenkins-project-dev:latest public.ecr.aws/n5h8m9x0/jenkins-project-dev:latest'
                sh 'docker push public.ecr.aws/n5h8m9x0/jenkins-project-dev:latest'
                build job: 'BotDeploy', wait: false, parameters: [string(name: 'BOT_IMAGE_NAME', value: "jenkins-project-dev:latest")]
            }
        }
    }
}
