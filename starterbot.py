import pprint
import os
import json
import time
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    #print(slack_events)
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            pprint.pprint(event)
            return event["text"], event["channel"], event["user"]
    return None, None, None

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        api_list = slack_client.api_call("channels.list")
        channel_info = slack_client.api_call("channels.info", channel="CGNSTHE0Y")
        pprint.pprint(channel_info)
        mess_dict = dict()
        while True:
            text, channel, user_id = parse_bot_commands(slack_client.rtm_read())
            if channel != None and text != None:
                if channel in mess_dict:
                    mess_dict[channel] += [{user_id:text}]
                else:
                    mess_dict[channel] = [{user_id:text}]   
                with open("try.json", "w") as f:
                    json.dump(mess_dict,f)
    else:
        print("Connection failed. Exception traceback printed above.")
