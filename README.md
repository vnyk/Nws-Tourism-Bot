# News-Tourism bot
The chat bot will reply to general tourism queries for rajasthan tourists. The bot will also help in generating area specific news from any part of World. Following is the tutorial for making the bot.

For the chat bot to function we'll need a server that will receive the messages sent by the Facebook users, process this message and respond back to the user. To send messages back to the server we will generate webhooks, the endpoint URL of our server should be accessible to the Facebook server and should use a secure HTTPS URL. For this reason, running our server locally will not work and instead we need to host our server online. In this tutorial, we are going to deploy our server on Hasura which automatically provides SSL-enabled domains.

# Requirements

* Python 3
* pip
* Hasura CLI
* Git


# Get Started

## Set up CLI

* In the shell run the following commands

```sh
$ pip install flask
$ pip install pymessenger
$ pip install gnewsclient 
```

## Create a facebook app

* Navigate to https://developers.facebook.com/apps/
* Click on *'+ Create a new app’ or '+ Add a new app’ *

![Alt Text](https://raw.githubusercontent.com/vipulrawat/fb-pincode-bot/master/assets/1.png)

* Give a display name for your app and a contact email.
* Hover over Messenger and click on Set Up.

![AltText](https://raw.githubusercontent.com/vipulrawat/fb-pincode-bot/master/assets/2.png)

* To generate token select a page from the list and generate a token.

![AltText](https://raw.githubusercontent.com/vipulrawat/fb-pincode-bot/master/assets/3.png)

## Set up built-in NLP
* Here we are using NLP from wit.ai, Login to wit.ai and create an app.
* From the settings generate an API access key.

## Customise

* Open server.py from `microservices\app\src` 
* Paste Your fb page token in `accesstoken='Your token here'`
* Open utils.py from `microservices\app\src`
* Paste your wit.ai API access key in `witaccess_token=' your token here'`

## Set up webhook

In your fb app page, scroll down until you find a card name `Webhooks`. Click on the `setup webhooks` button.

![Enable webhooks2](https://raw.githubusercontent.com/vipulrawat/fb-pincode-bot/master/assets/4.png "fb webhook screen")

* The `callback URL` is the URL that the facebook servers will hit to verify as well as forward the messages sent to our bot. The nodejs app in this project uses the `/webhook` path as the `callback URL`. Making the `callback URL` https://bot.YOUR-CLUSTER-NAME.hasura-app.io/webhook (in this case -> https://bot.oblong44.hasura-app.io/webhook/)
* The `verify token`is the verify token that you set in your secrets above (in the command $ hasura secrets update bot.fb_verify_token.key <YOUR-VERIFY-TOKEN>)
* After selecting all the `Subsciption Fields`. Submit and save.
![Subsciption page](https://raw.githubusercontent.com/vipulrawat/fb-pincode-bot/master/assets/5.png "fb subscribe screen")
* You will also see another section under `Webhooks` that says `Select a page to subscribe your webhook to the page events`, ensure that you select the respective facebook page here.

## Final Step!!

* Open git bash and change the directory to your cluster.
* Run the following commands.
        `git add .`
* Commit your changes
        `git commit -am "commit message"`
* Push your repository
         `git push hasura master`
