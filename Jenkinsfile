pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/your-repo-url.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Pytest Suite') {
            steps {
                sh '''
                . venv/bin/activate
                pytest --maxfail=1 --disable-warnings -v
                '''
            }
        }

    }

    post {
        always {
            junit 'pytest.xml'
        }
        success {
            echo "🎉 All tests passed successfully!"
        }
        failure {
            echo "❌ Test suite failed!"
        }
    }
}
