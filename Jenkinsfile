pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/victorzele96/trip-planner.git', branch: 'main', credentialsId: 'github-token'
            }
        }

        stage('Create App env') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'trip_db_user', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD')]) {
                    script {
                        def DB_HOST = credentials('DB_HOST')
                        def DB_PORT = credentials('DB_PORT')
                        def DB_NAME = credentials('DB_NAME')
                        def STREAMLIT_PORT = credentials('STREAMLIT_PORT')

                        sh """
                        cat > .env <<EOF
                            DB_HOST=${DB_HOST}
                            DB_PORT=${DB_PORT}
                            DB_NAME=${DB_NAME}
                            DB_USER=${DB_USER}
                            DB_PASSWORD=${DB_PASSWORD}
                            STREAMLIT_PORT=${STREAMLIT_PORT}
                            EOF
                        """
                    }
                }
            }
        }

        stage('Build & Deploy App') {
            steps {
                sh 'docker compose up -d --build app'
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v || true'
        }
    }
}
