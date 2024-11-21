import requests

from Auth import Auth
from Base import Base


class Request(Base):
    def __init__(self) -> None:
        super().__init__()
        self.Auth = Auth()

    def get_cookies(self):
        """
        Retrieve cookies from the Selenium driver and format them for the requests library.
        """
        selenium_cookies = self.seleniumDriver.get_cookies()
        cookies = {cookie['name']: cookie['value']
                   for cookie in selenium_cookies}
        return cookies

    def get_csrf_token(self):
        """
        Extract the CSRF token from the page using Selenium.
        Assumes the token is stored in a meta tag like <meta name="csrf-token" content="...">
        """
        try:
            csrf_token = self.seleniumDriver.execute_script(
                "return document.querySelector('meta[name=\"csrf-token\"]').getAttribute('content');"
            )
            if not csrf_token:
                raise ValueError("CSRF token not found in the page.")
            return csrf_token
        except Exception as e:
            print(f"An error occurred while fetching CSRF token: {e}")
            return None

    def get_user_agent(self):
        """
        Retrieve the User-Agent string from the Selenium driver.
        """
        try:
            user_agent = self.seleniumDriver.execute_script(
                "return navigator.userAgent;")
            if not user_agent:
                raise ValueError("User-Agent could not be retrieved.")
            return user_agent
        except Exception as e:
            print(f"An error occurred while fetching User-Agent: {e}")
            return None

    def json(self, url):
        try:
            # Ensure the user is authenticated
            if not self.Auth.isLoggedIn():
                if self.Auth.loginIfNotBlocked():
                    return self.json(url)

            # Get cookies from Selenium
            cookies = self.get_cookies()

            # Get CSRF token from Selenium
            csrf_token = self.get_csrf_token()
            if not csrf_token:
                print("CSRF token is missing.")
                return None

            # Get User-Agent from Selenium
            user_agent = self.get_user_agent()
            if not user_agent:
                print("User-Agent is missing.")
                return None

            # Define headers
            headers = {
                "User-Agent": user_agent,
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRF-Token": csrf_token,
                "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
            }

            # Make the GET request using requests
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status code {
                      response.status_code}: {response.text}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
