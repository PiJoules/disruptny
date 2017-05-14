from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

import json

#CHANNEL = "mapquest_channel"
#test_msg = {
#    "location": "40.709762, -73.986275",
#}

CHANNEL = "neximo_channel"
test_msg = {
    "targets": ["17325134403", "15164264399"],
    "text": "Test msg lol send from script",
}

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-1ce8260e-3828-11e7-9843-0619f8945a4f'
pnconfig.publish_key = 'pub-c-c03226af-2644-4bae-8a63-b34a6ce4e323'

pubnub = PubNub(pnconfig)


def my_publish_callback(envelope, status):
    print(status, envelope)
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel(CHANNEL).message(test_msg).async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        print(json.dumps(message.message, indent=4))
        pass  # Handle new message stored in message.message


def main():
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(CHANNEL).execute()

if __name__ == "__main__":
    main()
