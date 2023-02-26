pipeline {
    agent {
        docker {
            // TODO build & push your Jenkins agent image, place the URL here
            image '<jenkins-agent-image>'
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
                    # replace placeholders in YAML k8s files
                    sed -i "s%{{APP_ENV}}%$APP_ENV%g" infra/k8s/bot.yaml
                    sed -i "s%{{BOT_IMAGE}}%$BOT_IMAGE_NAME%g" infra/k8s/bot.yaml

                    # apply the configurations to k8s cluster
                    kubectl apply --kubeconfig ${KUBECONFIG} -f infra/k8s/bot.yaml
                    '''
                }
            }
        }
    }
}