from pyleapcard import *
from pprint import pprint
from getpass import getpass

def getLeapInfo(username, password):
    session = LeapSession()
    session.try_login(username, password)
     
    overview = session.get_card_overview()
    pprint(vars(overview))
     
    events = session.get_events()
    for item in events:
       pprint(vars(item))
    
username = input("Enter Username:")
password = getpass("Enter Password:")

getLeapInfo(username, password)
