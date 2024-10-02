pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-creds')
        GIT_CREDENTIALS = credentials('git-creds')
        EC2_SSH_KEY = credentials('ec2')
        DOCKER_IMAGE = 'shubhamm033/video:latest'
        EC2_USER = 'ubuntu' // Replace with your EC2 username
        EC2_HOST = 'ec2-3-108-185-93.ap-south-1.compute.amazonaws.com'
        PROJECT_DIR = '/home/ubuntu/splitwise'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourusername/your-django-repo.git',
                    credentialsId: 'git-credentials'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image(DOCKER_IMAGE).push()
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << EOF
                            docker pull ${DOCKER_IMAGE}
                            docker stop app_container || true
                            docker rm app_container || true
                            docker run -d --name app_container -p 8000:8000 ${DOCKER_IMAGE}
                        EOF
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed.'
        }
    }
}
