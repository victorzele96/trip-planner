pipeline {
    agent any

    parameters {
        choice(name: 'ACTION', choices: ['start', 'stop'], description: 'Start or stop the app')
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/victorzele96/trip-planner.git', branch: 'main', credentialsId: 'github-token'
            }
        }

        stage('Create App env') {
            steps {
                script {
                    def envFile = '.env'
                    env.ENV_FILE = envFile
                    echo "Using env file: ${envFile}"
                }
            }
        }

        stage('Manage App') {
            steps {
                script {
                    if (params.ACTION.toLowerCase() == 'start') {
                        bat "docker compose --env-file ${env.ENV_FILE} up -d --build app db"
                    } else if (params.ACTION.toLowerCase() == 'stop') {
                        bat "docker compose --env-file ${env.ENV_FILE} down"
                    }
                }
            }
        }
    }
}
