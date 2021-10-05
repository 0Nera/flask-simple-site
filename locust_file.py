from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
   def on_start(self):
       self.client.get("/")

   @task(2)
   def posts(self):
       self.client.get("/gen-img")

class WebsiteUser(HttpUser):
   tasks = [UserBehavior]
   min_wait = 100
   max_wait = 2000