pipeline {
    agent any

    parameters {
        choice(name: 'ACTION', choices: ['START', 'STOP'], description: 'Start or stop the services')
        string(name: 'ENVIRONMENT', defaultValue: 'APP', description: 'APP or TEST')
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/victorzele96/trip-planner.git', branch: 'main', credentialsId: 'github-token'
            }
        }

        stage('Set Env File') {
            steps {
                script {
                    def envFile = (params.ENVIRONMENT.toUpperCase() == 'TEST') ? '.env.test' : '.env'
                    env.ENV_FILE = envFile
                    echo "Using env file: ${envFile}"
                }
            }
        }

        stage('Manage Services') {
            steps {
                script {
                    if (params.ACTION.toLowerCase() == 'start') {
                        if (params.ENVIRONMENT.toUpperCase() == 'APP') {
                            bat "docker compose --env-file ${env.ENV_FILE} up -d --build app db"
                        } else if (params.ENVIRONMENT.toUpperCase() == 'TEST') {
                            bat "docker compose --env-file ${env.ENV_FILE} up -d --build test_db tests"
                        }
                    } else if (params.ACTION.toLowerCase() == 'stop') {
                        bat "docker compose --env-file ${env.ENV_FILE} down"
                    }
                }
            }
        }
    }
}
