from locust import HttpUser, task, between
import random


class APIUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(5)
    def predict(self):
        # sends a small example wav (you should provide a small sample file under data/sample.wav)
        try:
            with open('data/sample.wav', 'rb') as f:
                files = {'file': ('sample.wav', f, 'audio/wav')}
                self.client.post('/predict', files=files, timeout=30)
        except Exception:
            # fallback: hit health
            self.client.get('/health')
