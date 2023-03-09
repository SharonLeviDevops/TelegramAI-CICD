pipeline {
    agent {
        docker {
            // TODO build & push your Jenkins agent image, place the URL here
            image 'public.ecr.aws/n5h8m9x0/jenkins-project-cicd:latest'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        APP_ENV = "dev"
    }

    parameters {
        string(name: 'jenkins-project-workerapp')
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
                  kubectl apply --kubeconfig ${KUBECONFIG} -f infra/k8s/worker.yaml --set env=dev
                '''
                }
            }
        }
    }
}