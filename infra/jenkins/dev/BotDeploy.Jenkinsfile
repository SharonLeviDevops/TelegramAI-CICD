pipeline {
    agent {
        docker {
            // TODO build & push your Jenkins agent image, place the URL here
            image '700935310038.dkr.ecr.us-west-1.amazonaws.com/jenkins-project-cicd:latest'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    parameters {
        string(name: 'BOT_IMAGE_NAME', defaultValue: '', description: 'image sent from build')

    }

    environment {
        APP_ENV = "dev"
    }


    stages {
        stage('Bot Deploy') {
            steps {
                withCredentials([
                    file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')
                ]) {
                    sh '''
                    # apply the configurations to k8s cluster..
                    echo ${BOT_IMAGE_NAME}
                    sed -i "s|image:.*|image: jenkins-project-dev:$BOT_IMAGE_NAME|" infra/k8s/bot.yaml
                    kubectl apply --kubeconfig ${KUBECONFIG} -f infra/k8s/bot.yaml --namespace dev
                    sed -i 's|value:.*|value: "dev"|' infra/k8s/bot.yaml
                    kubectl apply --kubeconfig ${KUBECONFIG} -f infra/k8s/bot.yaml --namespace dev
                    kubectl get deployments
                    '''
                }
            }
        }
    }
}
