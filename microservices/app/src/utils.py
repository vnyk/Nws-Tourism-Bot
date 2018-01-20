from wit import Wit
from gnewsclient import gnewsclient

witaccess_token="Wit API access key here"

client=Wit(access_token= witaccess_token)

loc={'area':None}
def wit_response(message_text):
	resp=client.message(message_text)
	
	entity=None
	value=None
	categories=None
	try:
		entity=list(resp['entities'])[0]
		
		value=resp['entities'][entity][0]['value']
		if(entity=='location'):
			loc['area']=None
			loc['area']="{}".format(str(value))
		categories={'news':None}
		categories[entity] = resp['entities'][entity][0]['value']
	except:
		pass

	return(entity,value,categories)


def get_news_elements(categories):
	news_client = gnewsclient()
	news_client.query = ''
	news_client.location=loc['area']

	if categories['news'] != None:
		news_client.query += categories['news'] + ' '

	news_items = news_client.get_news()

	elements = []

	for item in news_items:
		element = {
					'title': item['title'],
					'buttons': [{
								'type': 'web_url',
								'title': "Read more",
								'url': item['link']
					}],
					'image_url': item['img']		
		}
		elements.append(element)

	return elements