pipeline {
    agent any

    parameters {
        choice(name: 'ACTION', choices: ['START', 'STOP'], description: 'Start or stop the services')
        string(name: 'ENVIRONMENT', defaultValue: 'app', description: 'app or tests')
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
                    def envFile = (params.ENVIRONMENT.toUpperCase() == 'tests') ? '.env.test' : '.env'
                    env.ENV_FILE = envFile
                    echo "Using env file: ${envFile}"
                }
            }
        }

        stage('Manage Services') {
            steps {
                script {
                    if (params.ACTION.toLowerCase() == 'start') {
                        if (params.ENVIRONMENT.toLowerCase() == 'app') {
                            bat "docker compose --env-file ${env.ENV_FILE} up -d --build app db"
                        } else if (params.ENVIRONMENT.toLowerCase() == 'tests') {
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
