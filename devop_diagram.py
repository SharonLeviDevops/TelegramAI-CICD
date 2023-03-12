from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.generic.os import Linux
from diagrams.k8s.clusterconfig import RBAC
from diagrams.k8s.compute import Deployment, Pod
from diagrams.k8s.network import Service
from diagrams.programming.language import Python
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker

with Diagram("CI/CD with Jenkins Project", show=False):
    with Cluster("Development Environment"):
        jenkins_dev = Jenkins("Jenkins")
        kubernetes_dev = EC2("Kubernetes\nCluster\n(dev)")
        bot_dev = Python("Bot\nApplication\n(dev)")
        worker_dev = Python("Worker\nApplication\n(dev)")
        docker_dev = Docker("Docker\nImage\n(dev)")
        rbac_dev = RBAC("Kubernetes\nRBAC\n(dev)")

        jenkins_dev >> docker_dev
        docker_dev >> bot_dev
        docker_dev >> worker_dev
        bot_dev >> Deployment("Bot\nDeployment\n(dev)")
        worker_dev >> Deployment("Worker\nDeployment\n(dev)")
        Deployment("Bot\nDeployment\n(dev)") - Service("Bot\nService\n(dev)")
        Deployment("Worker\nDeployment\n(dev)") - Service("Worker\nService\n(dev)")

        kubernetes_dev - rbac_dev
        rbac_dev >> Deployment("Bot\nDeployment\n(dev)")
        rbac_dev >> Deployment("Worker\nDeployment\n(dev)")

    with Cluster("Production Environment"):
        jenkins_prod = Jenkins("Jenkins")
        kubernetes_prod = EC2("Kubernetes\nCluster\n(prod)")
        bot_prod = Python("Bot\nApplication\n(prod)")
        worker_prod = Python("Worker\nApplication\n(prod)")
        docker_prod = Docker("Docker\nImage\n(prod)")
        rbac_prod = RBAC("Kubernetes\nRBAC\n(prod)")
        telegram_bot = Linux("Telegram\nBot")
        sqs = S3("SQS\nQueue")
        s3 = S3("S3\nBucket")
        db = RDS("Database")

        jenkins_prod >> docker_prod
        docker_prod >> bot_prod
        docker_prod >> worker_prod
        bot_prod >> Deployment("Bot\nDeployment\n(prod)")
        worker_prod >> Deployment("Worker\nDeployment\n(prod)")
        Deployment("Bot\nDeployment\n(prod)") - Service("Bot\nService\n(prod)")
        Deployment("Worker\nDeployment\n(prod)") - Service("Worker\nService\n(prod)")

        kubernetes_prod - rbac_prod
        rbac_prod >> Deployment("Bot\nDeployment\n(prod)")
        rbac_prod >> Deployment("Worker\nDeployment\n(prod)")
        bot_prod >> s3
        bot_prod >> sqs
        telegram_bot >> s3
        telegram_bot >> sqs
        sqs >> worker_prod
        db >> worker_prod
        bot_prod >> db

    jenkins_dev - ELB("Elastic\nLoad\nBalancer") >> kubernetes_dev
    jenkins_prod - ELB("Elastic\nLoad\nBalancer") >> kubernetes_prod

