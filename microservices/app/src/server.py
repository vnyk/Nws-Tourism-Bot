import os, sys
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response, get_news_elements

app = Flask(__name__)
accesstoken="Page access token here"
bot=Bot(accesstoken)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					# Echo
					response = None
					#categories=None
					entity, value, categories=wit_response(messaging_text)

					if entity =='location':
						response="Welcome to {}".format(str(value))
						categories="{}".format(str(value))

					if entity == 'food':
						respo="If you are hungry, please have a look at this"
						bot.send_text_message(sender_id, respo)
						response="https://droolraftan.wordpress.com/tag/jaipur-food"

					if entity=='developer':
						elements=[]
						element = {
												'title': "Vinayak Sharma",
												'buttons': [{
															'type': 'web_url',
															'title': "LinkedIn",
															'url': "https://www.linkedin.com/in/vinayak-sharma-2ab488142"
												},
												{
															'type': 'web_url',
															'title': "Website",
															'url': "http://vinayaksharma.blog"
												},
												{
															'type': 'web_url',
															'title': "Facebook",
															'url': "https://www.facebook.com/srma.vnyk19"
												}],
												'image_url': "https://spiderimg.amarujala.com/assets/images/2017/12/03/500x500/udaipur_1512275413.jpeg"
									}
						elements.append(element)
						bot.send_generic_message(sender_id, elements)
						response="Vinayak made me <3"


					if entity=='greetings':
						cresponse="Hi! I am Bhaya from Rajasthan"
						'''Cus_response="Hi! I am Bhaya from Rajasthan"'''
						response="how can I help you?"
						bot.send_text_message(sender_id, cresponse)

					if entity =='news':
						if(categories):
							elements=get_news_elements(categories)
							bot.send_generic_message(sender_id, elements)
							response="here it is! what else?"
						else:
							response="Where are u in Rajastan?"
						
					if response==None:
						response="please speak clearly!"

					bot.send_text_message(sender_id, response)

	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80)