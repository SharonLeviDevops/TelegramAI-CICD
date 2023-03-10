pipeline {
    agent {
        docker {
            // TODO build & push your Jenkins agent image, place the URL here
            image '700935310038.dkr.ecr.us-west-1.amazonaws.com/jenkins-project-cicd:latest'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        APP_ENV = "dev"
    }

    parameters {
        string(name: 'BOT_IMAGE_NAME')
    }

    stages {
        stage('Bot Deploy') {
            steps {
                withCredentials([
                    file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')
                ]) {
                    sh '''
                    # apply the configurations to k8s cluster
                    cat infra/k8s/bot.yaml
                    sleep 5s
                    cat infra/k8s/bot.yaml
                    sleep 5s
                    sed -i "s|image:.*|image: 700935310038.dkr.ecr.us-west-1.amazonaws.com/jenkins-project-dev:dev|" infra/k8s/bot.yaml
                    sed -i 's|value:.*|value: "dev"|' infra/k8s/bot.yaml
                    sleep 10s
                    cat infra/k8s/bot.yaml
                    sleep 5s
                    cat infra/k8s/bot.yaml
                    sleep 5s
                    kubectl apply --kubeconfig ${KUBECONFIG} -f infra/k8s/bot.yaml
                    '''
                }
            }
        }
    }
}