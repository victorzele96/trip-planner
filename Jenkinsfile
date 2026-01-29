pipeline {
    agent any

    parameters {
        choice(name: 'ACTION', choices: ['start', 'stop'], description: 'Start or stop the app')
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/victorzele96/trip-planner.git',
                    branch: 'main',
                    credentialsId: 'github-token'
            }
        }

        stage('Create App Env') {
            when {
                expression { params.ACTION == 'start' }
            }
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'trip_db_user', usernameVariable: 'DB_USER_SECRET', passwordVariable: 'DB_PASSWORD_SECRET'),
                    string(credentialsId: 'DB_HOST', variable: 'DB_HOST_VAR'),
                    string(credentialsId: 'DB_PORT', variable: 'DB_PORT_VAR'),
                    string(credentialsId: 'DB_NAME', variable: 'DB_NAME_VAR'),
                    string(credentialsId: 'STREAMLIT_PORT', variable: 'STREAMLIT_PORT_VAR')
                ]) {
                    sh """
                    echo "DB_HOST=${DB_HOST_VAR}" > .env
                    echo "DB_PORT=${DB_PORT_VAR}" >> .env
                    echo "DB_NAME=${DB_NAME_VAR}" >> .env
                    echo "DB_USER=${DB_USER_SECRET}" >> .env
                    echo "DB_PASSWORD=${DB_PASSWORD_SECRET}" >> .env
                    echo "STREAMLIT_PORT=${STREAMLIT_PORT_VAR}" >> .env
                    """
                }
            }
        }

        stage('Deploy / Stop App') {
            steps {
                script {
                    if (params.ACTION == 'start') {
                        // Starting app profile
                        sh "docker compose --project-name trip-planner --profile app --env-file .env up -d --force-recreate app db"
                        
                        echo "===================================="
                        echo " App is running (Control Start):"
                        echo " http://localhost:${env.STREAMLIT_PORT}"
                        echo "===================================="
                    } else {
                        // Stoping app profile
                        sh "docker compose --project-name trip-planner --profile app stop app db || true"
                        echo "===================================="
                        echo " App is stopped (Control Stop)."
                        echo "===================================="
                    }
                }
            }
        }
    }
}
