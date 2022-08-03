def checkout_source(){
    checkout([
        $class: "GitSCM", 
        branches: [
            [name: "*/main"]
        ], 
        extensions: [], 
        userRemoteConfigs: [[
            credentialsId: "3373b64f-27bb-440a-88f2-843c02843a99", 
            url: "https://github.com/duongngochau/Locust_Test_FastAPI.git"
        ]]])
}

def make_virtualenv(python_version="python3.9"){
    // sh "which ${python_version}"
    // sh "which $python_version"
    sh """
        py=\$(which ${python_version})
        \$py -m pip install --upgrade virtualenv
        \$py -m venv venv
    """
}

def run_command(command){
    sh """
    . venv/bin/activate
    $command
    """
}

def run_command_and_return_output(command){
    result = sh (
        script: """
            . venv/bin/activate
            $command
        """,
        returnStatus: true
    )
    return result
}

pipeline {
    agent any

    stages {
        stage("Checkout source and install libs") {
            steps {
                checkout_source()
                make_virtualenv()
                command("pip install -r requirements.txt")
            }
        }
        stage("Build") {
            steps{
                script {
                    try{
                        command("""
                            locust --host=http://127.0.0.1:8000 \
                            --run-time=30s \
                            --autostart \
                            --autoquit 5 \
                            --users=2500 \
                            --spawn-rate=1000 \
                            --html=reports/report.html \
                            --loglevel=DEBUG \
                            --logfile=reports/log \
                            --csv=reports/ \
                            --web-port=8099
                        """)
                    }catch (error) {
                    }         
                    command("""
                        data=$(python analytical_report.py reports/_stats.csv 10 30)
                        if [ $data == "pass" ]
                        then
                            echo "OK"
                        elif [ $data == "fail" ]
                        then
                            echo "Failure"
                        else
                            echo "warnings"
                        fi
                    """)
                }
            }
        }
    }

}