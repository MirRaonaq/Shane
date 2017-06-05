import requests
import json


class APICall:
    def __init__(self, access_token):
        self.author = 'MD ISLAM'
        self.access_token = access_token

    def makeRequest(self, url):
        url = url + '?access_token=' + self.access_token
        # print url
        return requests.get(url).text

    def makeRequestPost(self, url, data):
        url = url + '?access_token=' + self.access_token
        # print url
        return requests.post(url, json=json.loads(json.dumps(data))).text


'''
curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type" : "domain_whitelisting",
  "whitelisted_domains" : ["https://655ac952.ngrok.io"],
  "domain_action_type": "add"
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAAEKsbOLkpoBAIZCxlh1E0TAoo11OrB1WRC1CrAClnHBJA2fQjORWC5h0JXbWrjh878lPASIQrrloje5RuhH6NgpIMX4lVWd1tOUJ9tlWnQ5VOIR0ae2mVR13SnJi0JwSjuZBZCWjSRxHZBZBuyHuMLv6LUMg9vDFMgtrYIH30ZCJdhZAR9Bb12ZAZAMaCL3SkQAZD"

'''