pipeline {
    agent {
        docker {
            // TODO build & push your Jenkins agent image, place the URL here
            image 'jenkins-project'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

 // TODO prod bot build pipeline
}