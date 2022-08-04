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
        returnStdout: true
    )
    return result
}

// def set_status(status){
//     script: {
//         if [ $status == 'fail' ]
//         then
//             echo "status: fail"
//             currentBuild.result = 'FAILURE'
//         fi
//         if [ $status == 'pass' ]
//         then
//             echo "status: pass"
//             currentBuild.result = 'SUCEESS'
//         fi
//         if [ $status == 'warnings' ]
//         then
//             currentBuild.result = 'WARNINGS'
//         fi
//     }

// }

// def run_command_and_return_output(command){
//     result = sh (
//         script: "ls",
//         returnStdout: true
//     )
//     return result
// }

def check_failure(){
    sh """
    export status=\$(cat report_result.txt)
    if [ "\$status" = "fail" ]; then exit 1; fi
    """
}

def check_unstable(){
    sh """
    export status=\$(cat report_result.txt)
    if [ "\$status" = "warnings" ]; then exit 1; fi
    """
}


pipeline {
    agent any

    stages {
        stage("Checkout source and install libs") {
            steps {
                checkout_source()
                sh "rm -rf reports && mkdir reports"
                // make_virtualenv()
                // run_command("pip install -r requirements.txt")
            }
        }
        stage("Run Test") {
            steps{
                script {
                    try{
                        run_command("""
                            locust --host=http://127.0.0.1:8000 \
                            --run-time=$RUN_TIME \
                            --autostart \
                            --autoquit 5 \
                            --users=$USERS \
                            --spawn-rate=$SPAWN_RATE \
                            --html=reports/report.html \
                            --loglevel=DEBUG \
                            --logfile=reports/log \
                            --csv=reports/ \
                            --web-port=8099
                        """)
                    }catch (error) {
                    }
                }
            }
        }
        stage("Verify Report"){
            steps{
                script{
                    echo "Verify report status"
                    status = run_command_and_return_output("""
                        python analytical_report.py reports/_stats.csv $WARNINGS_THRESHOLD $FAILURE_THRESHOLD
                        
                    """)
                    sh """
                        echo "$status" > report_result.txt
                    """
                    try {
                        check_failure()
                    }catch(error){
                        currentBuild.result = 'FAILURE'
                        currentBuild.currentResult = 'FAILURE'
                    }
                    
                    try{
                        check_unstable()
                    }catch(error){
                        currentBuild.result = 'UNSTABLE'
                        unstable("current build is unstable")
                    }
                }
            }
        }
    }

}