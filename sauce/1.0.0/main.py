#Author: 808-Dev
#License: GPL - GNU General Public License
#Version: V.1.0.0 (Version 1: Patch 1)

#-----------------------------------------
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
#------------------------------------------
import configparser, os, time, mysql.connector,wget,tweepy,sys,datetime

a = datetime.datetime(100,1,1,11,34,59)
b = a + datetime.timedelta(0,237600)

os.system('cls' if os.name=='nt' else 'clear')
def get_hashtag_array(): #Grab array of hashtags from server
    sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    db_cursor = sql_db.cursor()
    db_cursor.execute("SELECT * FROM hashtags_to_follow")
    return db_cursor.fetchall()

def grab_new_version(): #Get a new version I guess
    sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    db_cursor = sql_db.cursor()
    db_cursor.execute("SELECT version_file FROM version_data WHERE platform = "+os.name)
    return db_cursor.fetchall()

def id_check(author): #Check for author ID
    sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    db_cursor = sql_db.cursor()
    query = "SELECT author FROM farts WHERE id = %s"
    values_to_push = (author,)
    db_cursor.execute(query,values_to_push)
    for x in db_cursor.fetchall():
        return 'skip'

def get_hashrate(): #Get quantity of images saved lol.
    sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    db_cursor = sql_db.cursor()
    db_cursor.execute("SELECT * FROM farts")
    i = 0
    for e in db_cursor.fetchall():
        i = i + 1
    return str(i)

def push_hashtag_array(tweet_id, tweet_author, tweet_data, tweet_time): #send data to Zuckerfuckbook.
    sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    db_cursor = sql_db.cursor()
    query = "INSERT INTO farts (id, author, data, time) VALUES (%s, %s, %s, %s)"
    values_to_push = (tweet_id, tweet_author, tweet_data, tweet_time)
    db_cursor.execute(query, values_to_push)
    sql_db.commit()


config = configparser.ConfigParser()

def generate_file():
    try: #Create config.ini file
        config.add_section("KEYS")
        config.set("KEYS", "API_PUBLIC_KEY", "")
        config.set("KEYS", "API_PRIVATE_KEY", "")
        config.add_section("TOKENS")
        config.set("TOKENS", "API_PUBLIC_TOKEN", "")
        config.set("TOKENS", "API_PRIVATE_TOKEN", "")
        config.add_section("MYSQL")
        config.set("MYSQL", "DB_NAME", "u991861799_fartmart")
        config.set("MYSQL", "DB_USER", "u991861799_python")
        config.set("MYSQL", "DB_PASSWORD ", "pufpoLM10$!")
        config.set("MYSQL", "HOST_NAME", "sql557.main-hosting.eu")
        config.add_section("ADMIN")
        config.set("ADMIN", "ADMIN_TWITTER_ID", "")
        config.set("ADMIN", "DEFAULT_SAVE_FOLDER", "")
        config.set("ADMIN", "ADMIN_PASSWORD", "0000")
        with open("config.ini", 'w') as configfile:
            config.write(configfile) #Write to the file
        
    except: #I don't know how this can happen but like I put it in anyway cuz I dislike errors
        print('File already generated but an error was encountered.')
        wait = input('Press \'Enter\' to exit this program.')
if not os.path.exists('config.ini'):
        generate_file()
        print("This software needs you to apply for a Twitter Developer account before use."+
              "\n\nPlease goto: https://dev.twitter.com/ to register for one."+
              "\nOnce completed, please fill in the config.ini file that this program generated."+
              "\nPlease note: While there is an SQL section, it is not operational as of this build."+
              "That is because I am lazy.")
        wait = input('Press \'Enter\' to exit this program.')
        exit()
else:

    config.read("config.ini")

    API_PUBLIC_KEY = config['KEYS']['api_public_key']
    API_PRIVATE_KEY = config['KEYS']['api_private_key']
    API_PUBLIC_TOKEN = config['TOKENS']['api_public_token']
    API_PRIVATE_TOKEN = config['TOKENS']['api_private_token']
    TWITTER_ID = config['ADMIN']['admin_twitter_id']
    DEFAULT_FOLDER = config['ADMIN']['default_save_folder']
    ADMIN_PASSWORD = config['ADMIN']['admin_password']
    SQL_HOSTNAME = config['MYSQL']['host_name']
    DB_NAME = config['MYSQL']['db_name']
    DB_USER = config['MYSQL']['db_user']
    DB_PASSWORD = config['MYSQL']['db_password']

    path_exists = os.path.exists(DEFAULT_FOLDER)

    if not path_exists and DEFAULT_FOLDER != '':
        print('Notice: Folder doesn\'t exist.')
        try:
            os.mkdir(DEFAULT_FOLDER)
        except:
            print('Unable to create folder. Please create folder.')

    auth = tweepy.OAuthHandler(API_PUBLIC_KEY, API_PRIVATE_KEY)
    auth.set_access_token(API_PUBLIC_TOKEN, API_PRIVATE_TOKEN)
    api = tweepy.API(auth)

    print('Notice: Logged in. Close this window to stop mining...')

    while True: #Initiate loop

        for hashtag in get_hashtag_array(): #Get hashtag from database then apply that to the hashtag

            try: #Attempt to maybe do something correctly for once.

                public_tweets = api.search_tweets(hashtag)
                time.sleep(3)
                print('Searching for Tweets')
                for tweet in public_tweets:  #Get individual tweet from tweet array.
                    anti_spam = False
                    if id_check(tweet.id) != 'skip': #If in db then skip
                        messages = api.get_direct_messages()
                        for message in reversed(messages):
                            if message.message_create['message_data']['text'] == 'server:kill':
                                api.send_direct_message(TWITTER_ID,'Are you sure you want to remotely kill this instance? Type your configuration password to kill otherwise ignore this message.')
                                kill_signal = True
                                print('Notice: Kill command issued. Waiting for administrator confirmation.')
                            if message.message_create['message_data']['text'] == ADMIN_PASSWORD:
                                if kill_signal == True:
                                    api.send_direct_message(TWITTER_ID,'Killing bot...')
                                    print('Notice: Kill confirmed. Killing bot...')
                                    api.delete_direct_message(message.id)
                                    exit()
                                else:
                                    api.send_direct_message(TWITTER_ID,'You must use "server:kill" to kill the bot...')
                                    print('Warning: Rogue kill confirmation command given. Ignoring...')
                                    api.delete_direct_message(message.id)
                            if message.message_create['message_data']['text'] == 'server:version:upgrade':
                                api.send_direct_message(TWITTER_ID,'Upgrading bot. Mining will be temporarily stopped while bot upgrades...')
                                print('Notice: Upgrading bot...')
                                try:
                                    print('Notice: Downloaded new version.')
                                    print('Notice: Killing old bot...')
                                    os.system('delete '+sys.argv[0] if os.name=='nt' else 'rm ./'+sys.argv[0])
                                    wget.download(grab_new_version())
                                    os.system('rename NFT_Miner.exe '+sys.argv[0] if os.name=='nt' else 'cp ./NFT_Miner '+sys.argv[0])
                                    api.delete_direct_message(message.id)
                                    os.system('start '+sys.argv[0] if os.name=='nt' else './'+sys.argv[0])
                                    exit()
                                except:
                                    print('Notice: Unable to grab new files. Returning to downloading...')
                                    api.delete_direct_message(message.id)

                            api.delete_direct_message(message.id)
                        if 'media' in tweet.entities: #If media not in there then ignore
                            if not os.path.exists(DEFAULT_FOLDER+str(tweet.extended_entities['media'][0]['media_url_https'])): #skip if file exists on system

                                print(tweet.author.screen_name)
                                push_hashtag_array(tweet.id,tweet.author.screen_name,str(tweet.extended_entities['media'][0]['media_url_https']),str(tweet.created_at))
                                wget.download(tweet.extended_entities['media'][0]['media_url_https'], out = DEFAULT_FOLDER)
                

            except tweepy.errors.HTTPException as e: #Complain when something inevitably breaks

                if '429' in str(e): #429 error thing

                    print('Notice: Rate Limit Exceeded. Waiting for 5 minutes.')
                    print('Notice: Sending status report to Bot Administrator.')
                    if anti_spam != True:
                        api.send_direct_message(TWITTER_ID,'Status: Current hash amount is: '+get_hashrate())
                    anti_spam = True
                    time.sleep(300)
                if '403' in str(e): #I'm not going to explain this. If you don't know what a 403 you are worse at coding than I am.

                    print('Error: Unable to acces Direct Message. Please verify you are not spamming.')
                    print('Notice: Further messaging will be disabled until program is restarted.')
                    anti_spam = True
                    time.sleep(1)
