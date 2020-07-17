#https://coderbook.com/@marcus/load-test-your-django-website-using-locustio/
#https://docs.locust.io/en/stable/quickstart.html
#https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/gunicorn/
#https://docs.gunicorn.org/en/latest/deploy.html
#https://gist.github.com/Atem18/4696071

from locust import HttpLocust, TaskSet, task

    
class UserBehavior(TaskSet):

    def home(self):
        self.client.get("")

    def signup(self):
        self.client.get("signup")

    def on_start(self):
        self.signup()

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 15000