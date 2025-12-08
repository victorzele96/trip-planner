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
                    string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                    string(credentialsId: 'DB_PORT', variable: 'DB_PORT'),
                    string(credentialsId: 'DB_NAME', variable: 'DB_NAME'),
                    string(credentialsId: 'STREAMLIT_PORT', variable: 'STREAMLIT_PORT')
                ]) {
                    bat """
                    echo DB_HOST=%DB_HOST% > .env
                    echo DB_PORT=%DB_PORT% >> .env
                    echo DB_NAME=%DB_NAME% >> .env
                    echo DB_USER=%DB_USER_SECRET% >> .env
                    echo DB_PASSWORD=%DB_PASSWORD_SECRET% >> .env
                    echo STREAMLIT_PORT=%STREAMLIT_PORT% >> .env
                    """
                    withEnv([
                        "APP_IMAGE=${env.APP_IMAGE}",
                        "DB_USER=${DB_USER_SECRET}",
                        "DB_PASSWORD=${DB_PASSWORD_SECRET}"
                    ]) {}
                }
            }
        }

        stage('Deploy / Stop App') {
            steps {
                script {
                    if (params.ACTION == 'start') {
                        // Starting app profile
                        bat "wsl docker compose --profile app --env-file .env up -d --force-recreate"
                        
                        echo "===================================="
                        echo " App is running (Control Start):"
                        echo " http://localhost:8501"
                        echo "===================================="
                    } else {
                        // Stoping app profile
                        bat "wsl docker compose down || exit /b 0"
                        echo "===================================="
                        echo " App is shut down (Control Stop)."
                        echo "===================================="
                    }
                }
            }
        }
    }
}
