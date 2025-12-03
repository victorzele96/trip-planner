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
                withCredentials([
                    usernamePassword(credentialsId: 'trip_db_user', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD'),
                    string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                    string(credentialsId: 'DB_PORT', variable: 'DB_PORT'),
                    string(credentialsId: 'DB_NAME', variable: 'DB_NAME'),
                    string(credentialsId: 'STREAMLIT_PORT', variable: 'STREAMLIT_PORT')
                ]) {
                    bat """
                    echo DB_HOST=%DB_HOST% > .env
                    echo DB_PORT=%DB_PORT% >> .env
                    echo DB_NAME=%DB_NAME% >> .env
                    echo DB_USER=%DB_USER% >> .env
                    echo DB_PASSWORD=%DB_PASSWORD% >> .env
                    echo STREAMLIT_PORT=%STREAMLIT_PORT% >> .env
                    """
                }
            }
        }

        stage('Manage App') {
            steps {
                script {
                    def envFile = params.ENV_FILE ?: '.env'
                    if (params.ACTION.toLowerCase() == 'start') {
                        bat "docker compose --env-file ${envFile} up -d --build app"
                    } else if (params.ACTION.toLowerCase() == 'stop') {
                        bat "docker compose --env-file ${envFile} down"
                    }
                }
            }
        }

    }
}
