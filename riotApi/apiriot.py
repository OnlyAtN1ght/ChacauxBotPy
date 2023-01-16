import requests

from TOKEN import API_KEY_RIOT

API_BASE_URL = "https://euw1.api.riotgames.com/"
class API():
	

	def __init__(self):
		pass

	def make_requests(self,endpoint):
		url = API_BASE_URL + endpoint + "?api_key=" + API_KEY_RIOT
		r = requests.get(url)
		return r.json()


	def search_username(self,username):
		endpoint = "lol/summoner/v4/summoners/by-name/" + username 
		data = self.make_requests(endpoint)
		print(data)


if __name__ == '__main__':
	a = API()
	a.search_username("OnlyAtN1ght")