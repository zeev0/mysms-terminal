import os
import argparse
import sys

from mysmsterminal.api.calls import Calls

VERSION = '1.0'
LICENSE = 'GPLv2'
c = Calls() ##API Client Object - All interactions with mysms are through this

def clearScreen(options=[]):
    os.system('cls' if os.name == 'nt' else 'clear')

def helpScreen(options=[]):
    print('mysms terminal interface')
    print('version: ' + VERSION + '\n')
    print('commands: ' + availableOptions())

menuOptions = {'clear'       : clearScreen,
               'help'        : helpScreen,
               'contacts'    : c.getContacts,
               'recent'      : c.getConversations,
               'message'     : c.prepareSMS,
               'reply'       : c.replyToActiveConvo,
               'open'        : c.openConversation,
               'unread'      : c.numUnreadMessages,
               'update'      : c.updateConvos,
               'exit'        : sys.exit
}

def availableOptions(options=[]):
    options = ''
    for key in menuOptions:
        options += str(key) + ', '
    return options

def processInput(inStr):
    splitString = inStr.split()
    command = splitString[0]
    options = splitString[1:]
    if command in menuOptions:
        clearScreen()
        menuOptions[command](options)
    elif command in [a[0] for a in c.returnConvos()]: #if its a conv num
        clearScreen()
        c.openConversation([command])
    else:
        print('command not recognized')

def menu():
    while True:
        inStr = input('> ')
        processInput(inStr)

def main():
    # Creating the arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s '+ VERSION)
    parser.add_argument('-n', '--noninteractive', help='allows for usage without\
                        using the program interface', action='store_true')
    parser.add_argument('-l', '--login', help='phone number for login',
                        action='store')
    parser.add_argument('-p', '--password', help='password for login',
                        action='store')
    parser.add_argument('-u', '--unread', help='gets the number of unread messages',
                        action='store_true')
    args = parser.parse_args()

    if args.noninteractive:
        if args.login == None or args.password == None:
            print('login and password required for noninteractive mode')
        else:
            c.login(args.login, args.password)
            if args.unread:
                print(c.numUnreadMessages())
    else:
        c.login(args.login, args.password)
        if args.unread:
            print(c.numUnreadMessages())
        clearScreen()
        c.getConversations()
        menu()

if __name__ == "__main__":
    main()
