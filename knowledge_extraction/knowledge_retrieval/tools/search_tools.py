import json
import os

import requests
from langchain.tools import tool

serpa_key = os.getenv('SERPER_API_KEY')
# print(f"SERPER_API_KEY: {serpa_key}")

if not serpa_key:
    raise KeyError("SERPER_API_KEY environment variable is not set")

class SearchTools:

    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet
        about a given topic and return relevant results"""
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': serpa_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            # print(response.text)
        except requests.exceptions.HTTPError as http_err:
            print(f'####### HTTP error occurred: {http_err}')
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            print(f'####### Other error occurred: {err}')
            return f'Other error occurred: {err}'

        # check if there is an organic key
        if 'organic' not in response.json():
            return "Sorry, I couldn't find anything about that, there could be an error with your Serper API key."
        else:
            results = response.json()['organic']
            string = []
            for result in results[:top_result_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}", f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    continue

            print(f'**** SEARCH Result: {string}')
            return '\n'.join(string)


# import json
# import os

# import requests
# from langchain.tools import tool

# serpa_key = os.getenv('OPENAI_API_KEY')
# print(f"SERPER_API_KEY: {serpa_key}")

# if not serpa_key:
#     raise KeyError("SERPER_API_KEY environment variable is not set")

# class SearchTools():

#   @tool("Search the internet")
#   def search_internet(query):
#     """Useful to search the internet
#     about a a given topic and return relevant results"""
#     top_result_to_return = 4
#     url = "https://google.serper.dev/search"
#     payload = json.dumps({"q": query})
#     headers = {
#         'X-API-KEY': os.getenv('OPENAI_API_KEY'),
#         'Content-Type': 'application/json'
#     }

#     try:
#       response = requests.request("POST", url, headers=headers, data=payload)
#       print(response.text)
#     except Exception as err:
#       print(f'####### Other error occurred: {err}')

#     # check if there is an organic key
#     if 'organic' not in response.json():
#       return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
#     else:
#       results = response.json()['organic']
#       string = []
#       for result in results[:top_result_to_return]:
#         try:
#           string.append('\n'.join([
#               f"Title: {result['title']}", f"Link: {result['link']}",
#               f"Snippet: {result['snippet']}", "\n-----------------"
#           ]))
#         except KeyError:
#           next

#         print(f'**** SEARCH Result: {string}')
#       return '\n'.join(string)
