pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-creds')
        GIT_CREDENTIALS = credentials('git-creds')
//         EC2_SSH_KEY = credentials('ec2')
        DOCKER_IMAGE = 'shubhamm033/video:latest'
        EC2_USER = 'ubuntu' // Replace with your EC2 username
        EC2_HOST = 'ec2-3-108-185-93.ap-south-1.compute.amazonaws.com'
        PROJECT_DIR = '/home/ubuntu/splitwise'
        CONTAINER_NAME = 'video-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/shubhamm033/video-app.git',
                    credentialsId: 'git-creds'
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
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') {
                        docker.image(DOCKER_IMAGE).push()
                    }
                }
            }
        }


        stage('Pull Docker Image') {
            steps {
                script {
                    // Pull the latest Docker image
                    sh 'docker pull ${DOCKER_IMAGE}'
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    // Stop and remove the existing container if it exists
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        # Run the new container
                        docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${DOCKER_IMAGE}
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
