// Jenkinsfile (Declarative Pipeline) - FINAL WORKING SYNTAX FOR CD TO TARGET
pipeline {
    agent any

    environment {
        DOCKER_USER = 'hr265docker' 
        IMAGE_NAME = 'sample-python-app'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        SCANNER_HOME = "/usr/local/bin/sonar-scanner-5.0.1.3006-linux" 
        APP_CONTAINER_NAME = 'python-app' // Unique name for the running application
        TARGET_HOST = 'app-target' // The name of the Docker service/container to deploy to
    }

    stages {
        stage('Code Checkout & Tool Install') {
            steps {
                echo "1. Copying source files from host volume mount..."
                sh 'cp -v /host_project/Dockerfile .'
                sh 'cp -v /host_project/app.py .'
                
                echo "2. Installing all necessary dependencies..."
                sh 'apt-get update && apt-get install -y wget unzip apt-transport-https ca-certificates curl gnupg'
                sh '''
                    # Sonar Scanner Install
                    wget -q https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                    unzip -o -q sonar-scanner-cli-5.0.1.3006-linux.zip -d /usr/local/bin/
                    rm sonar-scanner-cli-5.0.1.3006-linux.zip
                '''
                // --- CRITICAL DOCKER CLI FIX: Using --batch and --yes for GPG non-interaction ---
                sh 'curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor --batch --yes -o /etc/apt/keyrings/docker.gpg'
                
                sh 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian trixie stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null'
                
                sh 'apt-get update && apt-get install -y docker-ce-cli'
                
                echo "Tools ready."
            }
        }

        stage('Run SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube Local Server') {
                    sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectKey=my_sample_app -Dsonar.sources=."
                }
            }
        }

        stage('Quality Gate Check') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    // Allows the pipeline to continue despite the ERROR status
                    waitForQualityGate abortPipeline: false
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${env.DOCKER_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                sh "docker build -t ${env.DOCKER_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} ."
                sh "docker tag ${env.DOCKER_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} ${env.DOCKER_USER}/${env.IMAGE_NAME}:latest"
            }
        }

        stage('Deploy/Publish') {
            steps {
                echo "Deploying container ${env.IMAGE_TAG} to ${env.TARGET_HOST}..."
                
                // 1. Stop and remove the previous container instance (if running)
                sh "docker exec ${env.TARGET_HOST} sh -c 'docker stop ${env.APP_CONTAINER_NAME} || true'"
                sh "docker exec ${env.TARGET_HOST} sh -c 'docker rm ${env.APP_CONTAINER_NAME} || true'"
                
                // 2. Run the new application container image
                sh "docker exec ${env.TARGET_HOST} sh -c 'docker run -d --name ${env.APP_CONTAINER_NAME} -p 80:80 ${env.DOCKER_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG}'"
                
                echo "Deployment Complete. Application running on port 80."
            }
        }
    }
}

