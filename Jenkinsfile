def checkout_source(){
    checkout([
        $class: 'GitSCM', 
        branches: [
            [name: '*/main']
        ], 
        extensions: [], 
        userRemoteConfigs: [[
            credentialsId: '3373b64f-27bb-440a-88f2-843c02843a99', 
            url: 'https://github.com/duongngochau/app_template.git'
        ]]])
}

def make_virtualenv(python_version='python3.9'){
    sh "which ${python_version}"
    sh "which $python_version"
    sh """
        py=\$(which ${python_version})
        \$py -m pip install --upgrade virtualenv
        \$py -m venv .venv
    """
}

def run_command(command){
    sh """
    . .venv/bin/activate
    $command
    """
}

def remove_virtualenv(){
    sh """
        rm -rf .venv
    """
}

pipeline {
    
    agent any
    
    stages{
        stage('Checkout Source & install libs') {
            steps {
                echo "Check out source code"
                checkout_source()
                echo "Install libs"
                make_virtualenv("python3.9")
                run_command("pip install -r requirements.txt")
            }
        }
        stage('Build') {
            steps {
                run_command("""
                    python run_app.py 
                """)
            }
        }
    }
    post{
        always{
            remove_virtualenv()
        }
        success{
            echo "Success"
        }
        failure{
            echo "Failure"
        }
    }
}