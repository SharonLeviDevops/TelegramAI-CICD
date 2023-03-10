pipeline {
    agent {
        docker {
            // TODO build & push your Jenkins agent image, place the URL here
            image '700935310038.dkr.ecr.us-west-1.amazonaws.com/jenkins-project-cicd:latest'
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
                    aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 700935310038.dkr.ecr.us-west-1.amazonaws.com
                    docker build -t jenkins-project-worker:prod -f ./worker/Dockerfile .
                    docker tag jenkins-project-worker:prod 700935310038.dkr.ecr.us-west-1.amazonaws.com/jenkins-project-worker:prod
                    docker push 700935310038.dkr.ecr.us-west-1.amazonaws.com/jenkins-project-worker:prod
                '''
            }
        }
    }
//         stage('Trigger Deploy') {
//         steps {
//             build job: 'WorkerDeploy', wait: false, parameters: [
//                 string(name: 'BOT_IMAGE_NAME', value: "jenkins-project-workerapp:latest")
//             ]
//         }
//     }
}