pipeline {
    agent none

    stages {
        stage('Docker Login') {
            steps {
                script {
                    sh '''
                        aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/n5h8m9x0
                    '''
                }
            }
        }

        stage('Build and Deploy') {
            agent {
                docker {
                    // TODO build & push your Jenkins agent image, place the URL here
                    image 'public.ecr.aws/n5h8m9x0/jenkins-project-cicd:latest'
                    args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }

            steps {
                // TODO dev bot build stage
                sh '''
                    aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/n5h8m9x0
                    docker build -t jenkins-project-dev -f ./bot/Dockerfile .
                    docker tag jenkins-project-dev:latest public.ecr.aws/n5h8m9x0/jenkins-project-dev:latest
                    docker push public.ecr.aws/n5h8m9x0/jenkins-project-dev:latest
                '''

                build job: 'BotDeploy', wait: false, parameters: [
                    string(name: 'BOT_IMAGE_NAME', value: "jenkins-project-dev:latest")
                ]
            }
        }
    }
}