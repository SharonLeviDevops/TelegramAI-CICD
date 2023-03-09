pipeline {
    agent {
        docker {
            // TODO build & push your Jenkins agent image, place the URL here
            image 'public.ecr.aws/n5h8m9x0/jenkins-project-cicd:latest'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Build') {
            when {
                changeset "worker/**"
            }
            steps {
                sh '''
                    aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/n5h8m9x0
                    docker build -t jenkins-project-workerapp -f ./worker/Dockerfile .
                    docker tag jenkins-project-workerapp:latest public.ecr.aws/n5h8m9x0/jenkins-project-workerapp:latest
                    docker push public.ecr.aws/n5h8m9x0/jenkins-project-workerapp:latest
                '''
            }
        }
    }
        stage('Trigger Deploy') {
        steps {
            build job: 'WorkerDeploy', wait: false, parameters: [
                string(name: 'BOT_IMAGE_NAME', value: "jenkins-project-workerapp:latest")
            ]
        }
    }
}