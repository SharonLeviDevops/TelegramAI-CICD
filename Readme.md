# CI/CD with Jenkins Project


This project involves implementing a complete CI/CD process for the TelegramAI service in development and production environments using Jenkins.
The code for the project is provided in the TelegramAI-CICD repository on the main branch.
The project involves deploying a single-node Kubernetes cluster using k0s on an Amazon Linux EC2 medium instance.
The instance and Kubernetes cluster must have the appropriate permissions to access S3, SQS, and ECR registries.
The development and production environments will be running on the same Kubernetes cluster in two different namespaces.

Additionally, the project involves creating new resources for the different environments. Specifically, a new Telegram bot must be created for the production environment and stored as a secret in AWS Secrets Manager. A new SQS and S3 bucket must also be created for the new bot.
The existing Telegram token and resources will be used for the development environment.

Finally, the project involves configuring Jenkins to work with the Kubernetes cluster and creating pipelines for the development and production environments.
The pipelines will build and deploy the Bot and Worker applications using Kubernetes YAML manifests.
The pipelines will be created in the dev and prod folders, respectively.

The Dev and Prod Jenkins pipelines:

BotBuild: builds the Bot app and is triggered upon changes in bot/ directory or any other file related to the bot app.
BotDeploy: deploys the Bot app using a Kubernetes YAML manifest.
WorkerBuild: builds the Worker app and is triggered upon changes in worker/ directory or any other file related to the worker app.
WorkerDeploy: deploys the Worker app using a Kubernetes YAML manifest.
All pipelines should be implemented in the dev branch. The Docker image for all pipelines will be the same, and the Jenkins server will use a Kubernetes CLI tool called kubectl to deploy the applications.
