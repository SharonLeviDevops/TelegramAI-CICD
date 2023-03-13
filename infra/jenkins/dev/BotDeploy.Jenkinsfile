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
        IMAGE_NAME = 'jenkins-project-dev'
        IMAGE_TAG = "${BUILD_NUMBER}"
        REPO_URL = '700935310038.dkr.ecr.us-west-1.amazonaws.com'
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
                    # apply the configurations to k8s cluster..
                    kubectl delete deployment bot-deployment --ignore-not-found --grace-period=0 --namespace dev
                    sed -i "s|image:.*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|" infra/k8s/bot.yaml
                    sed -i 's|value:.*|value: "dev"|' infra/k8s/bot.yaml
                    kubectl apply --kubeconfig ${KUBECONFIG} -f infra/k8s/bot.yaml --namespace dev
                    kubectl get deployments
                    '''
                }
            }
        }
    }
}
