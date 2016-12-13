import os
import time
from slackclient import SlackClient


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
ADD_COMMAND = "!add"
LIST_COMMAND = "!list"
REMOVE_COMMAND = "!remove"
CLEAR_COMMAND = "!clear"

# list
myList = []


# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *!" + \
               "* command with List, Add, Remove, or Clear, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that! Example command"
   
    if command.startswith(ADD_COMMAND):
        added = command.lstrip('!ad').rstrip()
        myList.append(added)
        print (myList)
        response = "Sure...I've added '" + added + "' to the list."
        
    if command.startswith(REMOVE_COMMAND):
        removed = command.lstrip('!remov').rstrip()
        myList.remove(removed)
        print (myList)
        response = "I've removed " + removed + " from the list."
    if command.startswith(LIST_COMMAND): 
        tempList = []
        for item in myList:
            tempList.append("-- " + item + " \n ")
            
        tempStr = "".join(tempList)    
        response = "Here's the current grocery list: \n " + tempStr
        print (myList)
    if command.startswith(CLEAR_COMMAND):
        del myList[:]
        response = "The list has been cleared!"
        print (myList)
   

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
                          
                          
                          
def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Grocery Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")