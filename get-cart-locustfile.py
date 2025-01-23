from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login


class AddToCart(FastHttpUser):
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
        self.username = "test123"
        self.password = "test123"
        
        # Login to get the token and set it
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        print(f"Token received: {self.token}")  # For debugging purpose

    @task
    def add_item_to_cart(self):
        """Request to add an item to the cart"""
        headers = self.default_headers.copy()  # Make a copy of the default headers
        headers.update({
            "Cookies": f"token={self.token}",
            "Referer": "http://localhost:5000/product/1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        })

        with self.client.get("/cart", headers=headers, catch_response=True) as resp:
            if resp.status_code == 200:
                print("Successfully fetched the cart.")
                resp.success()  # Mark the request as successful
            else:
                print(f"Request failed with status code: {resp.status_code}")
                resp.failure("Failed to fetch cart")  # Mark the request as failed

if __name__ == "__main__":
    run_single_user(AddToCart)
