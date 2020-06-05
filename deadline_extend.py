
# import flask dependencies:
from flask import Flask, request, make_response, jsonify
import time
import json
from datetime import datetime, timedelta

# initialize the flask app:
app = Flask(__name__)
start=''

# function for webhook responses:
def broadbridge_webhook_results():

    # get current time by using below command:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    # extended time by 3 sec to make condition which is execute before webhook deadline occur:
    extended_time = now + timedelta(seconds=3)
    print("extended Time =", extended_time.time())

    # Dialogflow agent json response:
    req = request.get_json(force=True)

    action = req.get('queryResult').get('action')
    reply=''
    
    # If "welcome" intent is detected then below condition becomes "True": 
    # First intent action:
    if action=='input.welcome':

        # Added time delay to fail the below 'if condition' of normal response for welcome intent:
        time.sleep(3.5)
        
        # if current time is less than or equal to extended time then only below condition becomes "True":
        if now<=extended_time:
            # make a webhook response for welcome intent:
            reply={ "fulfillmentText": "This is simple welcome response from webhook",
                    "fulfillmentMessages": [
                            {
                            "text": {
                                    "text": [
                                        "This is simple welcome response from webhook"
                                    ]
                                }
                            }
                        ],  
                }

        # Create a Followup event when above "if condition" fail:
        reply={
                "followupEventInput": {
                        "name": "extent_webhook_deadline",
                        "languageCode": "en-US"
                    }
            }

    # Create a chain of followup event. Enter into first follow up event:
    # second intent action:
    if action=='followupevent':
        print("enter into first followup event")

        # Added time delay to fail the below 'if condition' and extend time by "3.5 sec", means right now total time "7 seconds" after webhook execute:
        time.sleep(3.5)
        
        # if current time is less than or equal to extended time then only below condition becomes "True": 
        if now<=extended_time:
            reply={ "fulfillmentText": "Yea, hi there. this is followup 1 event response for webhook.",
                    "fulfillmentMessages": [
                            {
                            "text": {
                                    "text": [
                                        "Yea, hi there. this is followup 1 event response for webhook."
                                    ]
                                }
                        }
                    ],
                "languageCode": "en",
            }

        # Create a Followup event number 2 when above "if condition" fail:
        reply={
                "followupEventInput": {
                        "name": "extent_webhook_deadline_2",
                        "languageCode": "en-US"
                    }
            }
    
    # Third intent action: 
    if action=='followupevent_2':
        print("enter into second followup event")

        # Added time delay to fail the below condition and extended more time by "3.5 sec", means right now total time "10.5 seconds" after webhook execute:
        time.sleep(3.5)
        
        # below response should be generated for extended webhook deadline:
        reply={ "fulfillmentText": "Yea, hi there. this is followup event 2 response for webhook.",
                    "fulfillmentMessages": [
                            {
                            "text": {
                                    "text": [
                                        "Yea, hi there. this is followup event 2 response for webhook."
                                    ]
                                }
                            }
                        ],
                "languageCode": "en",
            }
        
        print("Final time of execution:=>", now.strftime("%H:%M:%S"))
    return reply
    

# create a route for webhook: =>   example:http://localhost:5000/webhook
@app.route('/webhook/', methods=['GET', 'POST'])
def webhook():

    # return response
    return make_response(jsonify(broadbridge_webhook_results()))

# run the app
if __name__ == '__main__':
   app.run()