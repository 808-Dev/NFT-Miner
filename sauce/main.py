#I know this code sucks but trust me it will maybe be understandable soon.
#
import configparser, os, time, mysql.connector,wget,tweepy
os.system('cls' if os.name=='nt' else 'clear')
def get_hashtag_array():
    sql_db = mysql.connector.connect(host="",user="",password="",database="")
    db_cursor = sql_db.cursor()

    db_cursor.execute("SELECT * FROM hashtags_to_follow")

    return db_cursor.fetchall()

def id_check(author):
    sql_db = mysql.connector.connect(host="",user="",password="",database="")
    db_cursor = sql_db.cursor()
    query = "SELECT author FROM farts WHERE id = %s"
    values_to_push = (author,)
    db_cursor.execute(query,values_to_push)
    for x in db_cursor.fetchall():
        return 'skip'

def get_hashrate():
    sql_db = mysql.connector.connect(host="",user="",password="",database="")
    db_cursor = sql_db.cursor()
    db_cursor.execute("SELECT * FROM farts")
    i = 0
    for e in db_cursor.fetchall():
        i = i + 1
    return str(i)

def push_hashtag_array(tweet_id, tweet_author, tweet_data, tweet_time):
    sql_db = mysql.connector.connect(host="",user="",password="",database="")
    db_cursor = sql_db.cursor()
    query = "INSERT INTO farts (id, author, data, time) VALUES (%s, %s, %s, %s)"
    values_to_push = (tweet_id, tweet_author, tweet_data, tweet_time)
    db_cursor.execute(query, values_to_push)
    sql_db.commit()


config = configparser.ConfigParser()
def generate_file():
    try:
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
        config.add_section("ADMIN")
        config.set("ADMIN", "ADMIN_TWITTER_ID", "")
        config.set("ADMIN", "DEFAULT_SAVE_FOLDER", "")
        with open("config.ini", 'w') as configfile:
            config.write(configfile)
    except:
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
    path_exists = os.path.exists(DEFAULT_FOLDER)
    if not path_exists:
        print('Notice: Folder doesn\'t exist.');
    auth = tweepy.OAuthHandler(API_PUBLIC_KEY, API_PRIVATE_KEY)
    auth.set_access_token(API_PUBLIC_TOKEN, API_PRIVATE_TOKEN)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print('Notice: Logged in. Close this window to stop mining...')
    while True:
        for hashtag in get_hashtag_array():
            anti_spam = False
            try:
                public_tweets = api.search_tweets(hashtag)
                for tweet in public_tweets:
                    if id_check(tweet.id) != 'skip':
                        if 'media' in tweet.entities:
                            if not os.path.exists(DEFAULT_FOLDER+str(tweet.extended_entities['media'][0]['media_url_https'])):
                                print(tweet.author.screen_name)
                                push_hashtag_array(tweet.id,tweet.author.screen_name,str(tweet.extended_entities['media'][0]['media_url_https']),str(tweet.created_at))
                                wget.download(tweet.extended_entities['media'][0]['media_url_https'], out = DEFAULT_FOLDER)
                time.sleep(8)
            except tweepy.errors.HTTPException as e:
                if '429' in str(e):
                    print('Notice: Rate Limit Exceeded. Waiting for 5 minutes.')
                    print('Notice: Sending status report to Bot Administrator.')
                    if anti_spam != True:
                        api.send_direct_message(TWITTER_ID,'Status: Current hash amount is: '+get_hashrate())
                    anti_spam = True
                    time.sleep(60*5)
                if '403' in str(e):
                    print('Error: Unable to acces Direct Message. Please verify you are not spamming.')
                    print('Notice: Further messaging will be disabled until program is restarted.')
                    anti_spam = True
                    time.sleep(1)
