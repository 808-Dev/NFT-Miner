#Author: 808-Dev
#License: GPL - GNU General Public License
#Version: V.1.2.0 (Version 1: Patch 2)
#This Patch Fixes:
# -Issues brought with Patch 1
# -Removing Auto Upgrade since Windows 10 & 11 think I'm making a virus.
# -Notifies user when service grabs an image.
# -Fixes database connection timeout (hopefully)
# -Integrates monki as official new icon of NFT Miner.
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
import configparser, os, time, mysql.connector, wget, tweepy, datetime

a = datetime.datetime(100,1,1,11,34,59)
b = a + datetime.timedelta(0,237600)
config = configparser.ConfigParser()
os.system('cls' if os.name=='nt' else 'clear')
def get_hashtag_array(sql_db): #Grab array of hashtags from server

    db_cursor = sql_db.cursor()
    db_cursor.execute("SELECT * FROM hashtags_to_follow")
    return db_cursor.fetchall()

def hide_downloadbar(): #So it can compile

    useless_variable = 1

def id_check(author, sql_db): #Check for author ID
    #sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    db_cursor = sql_db.cursor()
    query = "SELECT author FROM farts WHERE id = %s"
    values_to_push = (author,)
    db_cursor.execute(query,values_to_push)
    for x in db_cursor.fetchall():
        return 'skip'

def get_hashrate(sql_db): #Get quantity of images saved lol.
    #sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    db_cursor = sql_db.cursor()
    db_cursor.execute("SELECT * FROM farts")
    i = 0
    for e in db_cursor.fetchall():
        i = i + 1
    return str(i)

def push_hashtag_array(tweet_id, tweet_author, tweet_data, tweet_time, sql_db): #send data to Zuckerfuckbook.
    #sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)
    db_cursor = sql_db.cursor()
    query = "INSERT INTO farts (id, author, data, time) VALUES (%s, %s, %s, %s)"
    values_to_push = (tweet_id, tweet_author, tweet_data, tweet_time)
    db_cursor.execute(query, values_to_push)
    sql_db.commit()

def generate_file():
    try: #Create config.ini file
        config.add_section("KEYS")
        config.set("KEYS", "API_PUBLIC_KEY", "")
        config.set("KEYS", "API_PRIVATE_KEY", "")
        config.add_section("TOKENS")
        config.set("TOKENS", "API_PUBLIC_TOKEN", "")
        config.set("TOKENS", "API_PRIVATE_TOKEN", "")
        config.add_section("MYSQL")
        config.set("MYSQL", "DB_NAME", "")
        config.set("MYSQL", "DB_USER", "")
        config.set("MYSQL", "DB_PASSWORD ", "")
        config.set("MYSQL", "HOST_NAME", "")
        config.add_section("ADMIN")
        config.set("ADMIN", "ADMIN_TWITTER_ID", "")
        config.set("ADMIN", "DEFAULT_SAVE_FOLDER", "")

        with open("config.ini", 'w') as configfile:
            config.write(configfile) #Write to the file

    except: #I don't know how this can happen but like I put it in anyway cuz I dislike errors
        print('File already generated.')

if not os.path.exists('config.ini'):
        generate_file()
        print("This software needs you to apply for a Twitter Developer account before use."+
              "\n\nPlease goto: https://dev.twitter.com/ to register for one."+
              "\n\nOnce completed, please fill in the config.ini file that this program generated."+
              "\n\nPlease note: While there is an SQL section, it is not operational as of this build."+
              "That is because I am lazy.")

else:

    config.read("config.ini")

    API_PUBLIC_KEY = config['KEYS']['api_public_key']
    API_PRIVATE_KEY = config['KEYS']['api_private_key']
    API_PUBLIC_TOKEN = config['TOKENS']['api_public_token']
    API_PRIVATE_TOKEN = config['TOKENS']['api_private_token']
    TWITTER_ID = config['ADMIN']['admin_twitter_id']
    DEFAULT_FOLDER = config['ADMIN']['default_save_folder']
    SQL_HOSTNAME = config['MYSQL']['host_name']
    DB_NAME = config['MYSQL']['db_name']
    DB_USER = config['MYSQL']['db_user']
    DB_PASSWORD = config['MYSQL']['db_password']

    sql_db = mysql.connector.connect(host=SQL_HOSTNAME,user=DB_USER,password=DB_PASSWORD,database=DB_NAME)

    path_exists = os.path.exists(DEFAULT_FOLDER)

    if not path_exists and DEFAULT_FOLDER != '':
        print('Notice: Folder doesn\'t exist.')
        try:
            os.mkdir(DEFAULT_FOLDER)
        except:
            print('Error: Unable to create folder. Please create folder.')

    auth = tweepy.OAuthHandler(API_PUBLIC_KEY, API_PRIVATE_KEY)
    auth.set_access_token(API_PUBLIC_TOKEN, API_PRIVATE_TOKEN)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    print('Notice: Logged in. Close this window to stop mining...')

    while True: #Initiate loop
        for hashtag in get_hashtag_array(sql_db): #Get hashtag from database then apply that to the hashtag
            try: #Attempt to maybe do something correctly for once.
                public_tweets = api.search_tweets(hashtag)
                for tweet in public_tweets:  #Get individual tweet from tweet array.
                    if id_check(tweet.id,sql_db) != 'skip': #If in db then skip
                        if 'media' in tweet.entities: #If media not in there then ignore
                            if not os.path.exists(DEFAULT_FOLDER+str(tweet.extended_entities['media'][0]['media_url_https'])): #skip if file exists on system
                                print('\nGrabbed tweet id: '+str(tweet.id))
                                push_hashtag_array(tweet.id,tweet.author.screen_name,str(tweet.extended_entities['media'][0]['media_url_https']),str(tweet.created_at),sql_db)
                                wget.download(tweet.extended_entities['media'][0]['media_url_https'], out = DEFAULT_FOLDER, bar = hide_downloadbar())
                                time.sleep(3)

            except tweepy.errors.HTTPException as e: #Complain when something inevitably breaks

                if '429' in str(e): #429 error thing

                    print('Notice: Rate Limit Exceeded. Waiting for 5 minutes.')
                    print('Notice: Sending status report to Bot Administrator.')
                    if anti_spam != True:
                        api.send_direct_message(TWITTER_ID,'Status: Current hash amount is: '+get_hashrate(sql_db))
                    anti_spam = True
                    time.sleep(300)

                if '403' in str(e): #I'm not going to explain this. If you don't know what a 403 you are worse at coding than I am.

                    print('Error: Unable to acces Direct Message. Please verify you are not spamming.')
                    print('Notice: Further messaging will be disabled until program is restarted.')
                    anti_spam = True
                    time.sleep(1)
