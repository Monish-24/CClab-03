from locust import task, run_single_user
from locust import FastHttpUser


class browse(FastHttpUser):
    host = "http://localhost:5000"
    
    # Default headers applied globally
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    def on_start(self):
        """Executed when the test starts for this user."""
        print("Starting the test for this user...")
        # You can add any setup logic here like logging in if required.
    
    def on_stop(self):
        """Executed when the test stops for this user."""
        print("Test completed for this user.")
        # Perform any cleanup tasks if needed, like logging out.

    @task
    def t(self):
        # Making the request with default headers
        with self.client.get("/browse", headers=self.default_headers, catch_response=True) as resp:
            # Check if response status code is 200
            if resp.status_code == 200:
                print("Request to /browse was successful.")
            else:
                print(f"Request failed with status code: {resp.status_code}")
            # You can assert response to make sure it meets expectations
            resp.success()  # Marks the response as successful (or you can call `resp.failure()` for failure)

if __name__ == "__main__":
    run_single_user(browse)
