import time
from locust import HttpUser, task

class QuickstartUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")

    @task(3)
    def view_item(self):
        for item_id in range(10):
            self.client.get("/add?a=10&b=90")
            time.sleep(1)