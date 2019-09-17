#!/usr/bin/python2.7

import os
import string
import hashlib
import datetime
import subprocess
import dateutil.parser
from random import *

# Check Deadline.
# If past deadline send reset action to Raffle.

# Create a random string of characters (the passwords) for each bot.
# Save these characters to a file for each of the bot sessions.

def dPrint(*msg):
    if msg:
        for message in msg:
            print "*** DEBUG: <"+message+">"
    else:
        print "*** DEBUG:"

def init():
    # Set CWD to script location so that `passwords` dir is created/accessed exactly where it needs to.
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    dirName = "passwords"
    try:
        os.mkdir(dirName)
        dPrint("Directory "+dirName+" created ")
    except Exception as e:
        dPrint("Can't create "+dirName+" because it probably already exists.")
        dPrint("Exception: " +str(e))

    # Get game info:
    game_info = os.popen("cleos -u https://eos.greymass.com:443 get table billionraffl billionraffl gamev2")
    player_info = os.popen("cleos -u https://eos.greymass.com:443 get table billionraffl billionraffl player")

    return game_info.read(), player_info.read()

def savePasswords(password0, password1, password2, password3):
    f = open("passwords/password0.txt", "w")
    f.write(password0)
    f.close()

    f = open("passwords/password1.txt", "w")
    f.write(password1)
    f.close()

    f = open("passwords/password2.txt", "w")
    f.write(password2)
    f.close()

    f = open("passwords/password4.txt", "w")
    f.write(password3)
    f.close()

    dPrint("Saved passwords.")

def genPasswd():
    characters = string.ascii_letters + string.digits
    password0 =  "".join(choice(characters) for x in range(randint(10, 16)))
    password1 =  "".join(choice(characters) for x in range(randint(10, 16)))
    password2 =  "".join(choice(characters) for x in range(randint(10, 16)))
    password3 =  "".join(choice(characters) for x in range(randint(10, 16)))
    dPrint("Generated passes:", password0, password1, password2, password3)

    return password0, password1, password2, password3

def loadPasswords():
    # Retrieves the generated passwords from the files and saves them in memory for use.f = open('password0.txt')
    f0 = open('passwords/password0.txt')
    p0 = f0.readline()
    f0.close()

    f1 = open('passwords/password1.txt')
    p1 = f1.readline()
    f1.close()

    f2 = open('passwords/password2.txt')
    p2 = f2.readline()
    f2.close()

    f3 = open('passwords/password2.txt')
    p3 = f3.readline()
    f3.close()

    return p0, p1, p2, p3

def getHash(plaintext_string):
    # Have to hash the passwords, twice with the sha256 algorithm.
    secret = hashlib.sha256(plaintext_string)
    hashe = hashlib.sha256(secret.digest()).hexdigest()
    dPrint("getHash() double sha256 for \'"+plaintext_string+"\': "+hashe)

    return hashe

def getSecretAndHashe(plaintext_string):
    secret = hashlib.sha256(plaintext_string)
    hashe = hashlib.sha256(secret.digest()).hexdigest()
    dPrint("getSecretAndHashe() generated double sha256 for \'"+plaintext_string+"\'; secret: "+secret.hexdigest()+"; hash: "+hashe)

    return secret.hexdigest(), hashe

def registerXBL(password0, password1, password2):
    # registers 0.0001 XBL (or whatever the minimum amount is) and submits the saved passwords for each of the three bots.
    # Have to check the cleos syntax (github) and generate the hashes.
    hash0 = getHash(password0)
    hash1 = getHash(password1)
    hash2 = getHash(password2)
    hash3 = getHash(password3)

    os.system('cleos -u https://eos.greymass.com:443 push action billionairet transfer \'{\"from\":\"billionbot11\",\"to\":\"billionraffl\",\"quantity\":\"0.0010 XBL\",\"memo\":\"'+hash0+'\"}\' -p billionbot11')
    os.system('cleos -u https://eos.greymass.com:443 push action billionairet transfer \'{\"from\":\"billionbot12\",\"to\":\"billionraffl\",\"quantity\":\"0.0010 XBL\",\"memo\":\"'+hash1+'\"}\' -p billionbot12')
    os.system('cleos -u https://eos.greymass.com:443 push action billionairet transfer \'{\"from\":\"billionbot13\",\"to\":\"billionraffl\",\"quantity\":\"0.0010 XBL\",\"memo\":\"'+hash2+'\"}\' -p billionbot13')
    os.system('cleos -u https://eos.greymass.com:443 push action billionairet transfer \'{\"from\":\"billionbot14\",\"to\":\"billionraffl\",\"quantity\":\"0.0010 XBL\",\"memo\":\"'+hash3+'\"}\' -p billionbot14')

    #cleos push action $xbltoken transfer '{"from":"accountnum13","to":"'billionraffl'","quantity":"0.001 XBL","memo":"d533f24d6f28ddcef3f066474f7b8355383e485681ba8e793e037f5cf36e4883"}' -p accountnum13

def submitBoth(one, two, three, four):
    dPrint(" ","Submit both running...", "  "," ","")
    password0, password1, password2 = loadPasswords()

    bot11_secret, bot11_hashe = getSecretAndHashe(password0)
    bot12_secret, bot12_hashe = getSecretAndHashe(password1)
    bot13_secret, bot13_hashe = getSecretAndHashe(password2)
    bot14_secret, bot14_hashe = getSecretAndHashe(password3)

    dPrint('Loaded password0: '+password0, bot11_secret, bot11_hashe, "")
    dPrint('Loaded password1: '+password1, bot12_secret, bot12_hashe, "")
    dPrint('Loaded password2: '+password2, bot13_secret, bot13_hashe, "")
    dPrint('Loaded password2: '+password3, bot14_secret, bot14_hashe, "")

    bot11_register = 'cleos -u https://eos.greymass.com:443 push action billionraffl submitboth \'{\"player\":\"billionbot11\",\"hash\":\"'+bot11_hashe+'\",\"secret\":\"'+bot11_secret+'\"}\' -p billionbot11'
    bot12_register = 'cleos -u https://eos.greymass.com:443 push action billionraffl submitboth \'{\"player\":\"billionbot12\",\"hash\":\"'+bot12_hashe+'\",\"secret\":\"'+bot12_secret+'\"}\' -p billionbot12'
    bot13_register = 'cleos -u https://eos.greymass.com:443 push action billionraffl submitboth \'{\"player\":\"billionbot13\",\"hash\":\"'+bot13_hashe+'\",\"secret\":\"'+bot13_secret+'\"}\' -p billionbot13'
    bot14_register = 'cleos -u https://eos.greymass.com:443 push action billionraffl submitboth \'{\"player\":\"billionbot14\",\"hash\":\"'+bot14_hashe+'\",\"secret\":\"'+bot14_secret+'\"}\' -p billionbot14'

    if one == 0: 
        os.system(bot11_register)
    if two == 0: 
        os.system(bot12_register)
    if three == 0:
        os.system(bot13_register)
    if four == 0:
        os.system(bot14_register)

    print "Commands given:\n%s \n %s \n %s " % (bot11_register, bot12_register, bot13_register, bot14_register)

def sendReset():
    # We have to use subprocess, otherwise the cleosm alias won't work.
    os.system('cleos -u https://eos.greymass.com:443 push action billionraffl reset \'{\"contract\":\"billionraffl\"}\' -p billionbot11@active')
    # Make sure this was succesful.

def getStage(game_info):
    stage = int(game_info.split("\"stage\": ")[1].split(",")[0])
    dPrint("We are in stage: "+(str(stage)))

    return stage

def checkRegistered(player_info):
    dPrint("Checking if bots are already registered this round...")
    #if string: "player": "billionbot13" in output of player info, then player = registered.

    b11_r = False
    b12_r = False
    b13_r = False
    b14_r = False

    if (player_info.find('"player": "billionbot11"') != -1):
        dPrint("Bot 11 is registered this round.")
        b11_r = True

    if (player_info.find('"player": "billionbot12"') != -1):
        dPrint("Bot 12 is registered this round.")
        b12_r = True

    if (player_info.find('"player": "billionbot13"') != -1):
        dPrint("Bot 13 is registered this round.")
        b13_r = True

    if (player_info.find('"player": "billionbot14"') != -1):
        dPrint("Bot 14 is registered this round.")
        b14_r = True

    #print player_info

    if (b11_r == False and b12_r == False and b13_r == False and b14_r == False):
        # Maybe we should have (or) instead of (and) for this qualification.
        dPrint("checkRegistered() returning False")
        return False
    else:
        dPrint("checkRegistered() returning True")
        return True

def getResetFlag(game_info):
    date_string = game_info.split("\"deadline\": \"")[1].split("\"")[0]
    #ate_string = "2019-04-11T13:27:18"
    dPrint("date_string: "+date_string)
    # This calculates and sees if time expired or not and so if it needs to send reset.  

    raffle_datetime = dateutil.parser.parse(date_string)
    difference = raffle_datetime - datetime.datetime.now()
    dPrint(str(difference)+" left on timer.")
    if difference.days < 0:
        reset_flag = True
    else:
        reset_flag = False

    return reset_flag

def updateStage(stage):
    # Advances stage.
    if stage == 1:
        stage = 2
    else:
        stage = 1
        
    return stage

def checkSubmitted(player_info):
    empty_secret =  '"0000000000000000000000000000000000000000000000000000000000000000",'
    submitted_11 = False
    submitted_12 = False
    submitted_13 = False
    submitted_14 = False

    counter = 0

    while counter < len(player_info):
        if "billionbot11" in player_info[counter]:
            if player_info[counter+4] != empty_secret: # This is where the secret lies
                submitted_11 = True

        if "billionbot12" in player_info[counter]:
            if player_info[counter+4] != empty_secret: # This is where the secret lies
                submitted_12 = True
        
        if "billionbot13" in player_info[counter]:
            if player_info[counter+4] != empty_secret: # This is where the secret lies
                submitted_13 = True 

        if "billionbot14" in player_info[counter]:
            if player_info[counter+4] != empty_secret: # This is where the secret lies
                submitted_14 = True 

        counter += 1
        
    dPrint("Bot11 Submitted: "+ str(submitted_11))
    dPrint("Bot12 Submitted: "+ str(submitted_12))
    dPrint("Bot13 Submitted: "+ str(submitted_13))
    dPrint("Bot14 Submitted: "+ str(submitted_14))
    return submitted_11, submitted_12, submitted_13, submitted_14

def main():
    game_info, player_info = init()
    stage = getStage(game_info)

    if ( getResetFlag(game_info) == True ):
        dPrint("Need to reset, sending...")
        sendReset()
        stage = updateStage(stage)
        registered = False
    else:
        dPrint("No need to reset yet.")
        registered = checkRegistered(player_info)

    if (stage == 2):
        submitted_11, submitted_12, submitted_13, submitted_14 = checkSubmitted(player_info.split())

    if (stage == 1) and (registered == False):
        # Registers passwords for all three bots.
        dPrint("Bots are not registered this round. Generating passwords...")
        password0, password1, password2, password3 = genPasswd()
        dPrint()

        savePasswords(password0, password1, password2, password3)

        # We gotta register the hashed passwords to the raffle.
        registerXBL(password0, password1, password2, password3)
        dPrint("Registered passwords to raffle.")

    elif (stage == 2) and ((submitted_11 == False) or (submitted_12 == False) or 
            (submitted_13 == False) or (submitted_14 == False)):
        # Submits the secret and hash for the bots that have not submitted already.
        submitBoth(submitted_11, submitted_12, submitted_13, submitted_14)

    else:
        # No actions to take.
        dPrint("Nothing to do yet. Exiting program.")

if __name__ == '__main__':
    main()