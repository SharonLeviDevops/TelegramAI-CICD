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
        string(name: 'WORKER_IMAGE_NAME')
    }

    // TODO dev worker deploy stages here
}