from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/user")

c = """run command
locust --host=http://127.0.0.1:8000 \
       --run-time=20s \
       --autostart \
       --autoquit 5 \
       --users=1000 \
       --spawn-rate=100 \
       --html=reports/report.html \
       --loglevel=DEBUG \
       --logfile=reports/log \
       --csv=reports/ \
       --web-port=8099
"""