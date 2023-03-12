pipeline {
    agent {
        docker {
            // TODO build & push your Jenkins agent image, place the URL here
            image '700935310038.dkr.ecr.us-west-1.amazonaws.com/jenkins-project-cicd:latest'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        APP_ENV = "prod"
    }

    parameters {
        string(name: 'jenkins-project-worker')
    }

    // TODO dev worker deploy stages here
    stages {
    stage('Bot Deploy') {
        steps {
            withCredentials([
                file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')
            ]) {
                sh '''
                # apply the configurations to k8s cluster
                    kubectl delete deployment worker-deployment --ignore-not-found --grace-period=0 --namespace prod
                    sed -i "s|image:.*|image: 700935310038.dkr.ecr.us-west-1.amazonaws.com/jenkins-project-worker:prod|" infra/k8s/worker.yaml
                    sed -i 's|value:.*|value: "dev"|' infra/k8s/worker.yaml
                    kubectl apply --kubeconfig ${KUBECONFIG} -f infra/k8s/worker.yaml --namespace=prod
                  '''
                }
            }
        }
    }
}