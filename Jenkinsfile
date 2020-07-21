pipeline {
    agent any
    environment {
        python_package = 'connector'
        git_url = 'https://github.com/byt3-m3/connector.git'
    }

    stages {
        stage('Prep') {
            steps {

            git credentialsId: '7716661b-b5b1-4817-bf7f-22a92b1cf815', url: "https://github.com/byt3-m3/connector.git"
            }
        }

        stage('Building Test Env') {
            steps {

                sh "python3 -m venv venv"

                withPythonEnv("${WORKSPACE}/venv/bin/python3") {

                    sh "pip install -r ${WORKSPACE}/requirements.txt"

                }
            }
        }

        stage('Running Tests') {
            steps {
                // One or more steps need to be included within the steps block.
                  withPythonEnv("${WORKSPACE}/venv/bin/python3") {

                    sh "python ${WORKSPACE}/test_suite.py"

                }

            }
        }
        stage("Building Docker Image") {
            steps {
                sh "cd ${WORKSPACE} && docker build -f build.Dockerfile -t cbaxter1988/connector ."
            }

        }

        stage("Cleaning"){
            steps {
                sh "rm -rf ${WORKSPACE}/venv"
            }

        }

        stage("Publishing to Docker Registry"){
            steps {

                    withDockerRegistry(credentialsId: '5d7125e3-665c-41ff-88d1-269308e2b016', url: ' https://index.docker.io/v1/') {
                        // some block
                        sh "docker push cbaxter1988/connector"



                    }





            }

        }


}

}

