from locust import HttpUser, task, between

class TestPerformance(HttpUser):
    wait  = between(2,5)
    
    #Path or the endpoint to be tested
    @task
    def app(self):
        self.client.get("/")