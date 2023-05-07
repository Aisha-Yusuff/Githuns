pipeline{
    agent any
    environment {
        dockerImage = ''
        registry = 'dominiqued/python-flask-githuns'
        registryCredential='domdockerhub'

    }
    stages{
        stage('build'){
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Aisha-Yusuff/Githuns']])
            }
        }

        stage('Docker Image'){
            steps {
                script{
                    dockerImage = docker.build registry
                }
            }

        }
        stage('Push Docker Image'){
            steps {
                script{
                    docker.withRegistry('',registryCredential){
                        dockerImage.push()
                    }
                }
            }

        }
    }
}