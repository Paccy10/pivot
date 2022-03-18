import json
import psycopg2
import unicodedata
from sql_queries import *


def process_tweets_file(cur):
    ids = []
    languages = ["ar", "en", "fr", "in", "pt", "es", "tr", "ja"]
    hashtag_table = []
    excluded_hashtags = []
    user_ids = []

    file = open('hashtags.txt', 'r')
    lines = file.readlines()
    for line in lines:
        tag = unicodedata.normalize(
            'NFKD', u"{0}".format(line.strip())).encode('ascii', 'ignore')
        excluded_hashtags.append(tag.decode())

    with open('data.txt', 'r') as file:
        for i, line in enumerate(file):
            reply_to_tweet_id = None
            reply_to_user_id = None
            tweet_type = None
            retweet_to_tweet_id = None
            retweet_to_user_id = None

            try:
                tweet = json.loads(line)

                id = tweet.get("id", None)
                id_str = tweet.get("id_str", None)
                created_at = tweet.get("created_at", None)
                text = tweet.get("text", None)
                hashtags = tweet["entities"].get("hashtags", None)
                user = tweet["user"]
                user_id = user.get("id", None)
                user_id_str = user.get("id_str", None)
                user_screen_name = tweet["user"].get("screen_name", None)
                user_description = tweet["user"].get("description", None)
                retweeted_status = tweet.get("retweeted_status", None)
                in_reply_to_user_id = tweet.get("in_reply_to_user_id", None)
                in_reply_to_screen_name = tweet.get(
                    "in_reply_to_screen_name", None)
                in_reply_to_status_id = tweet.get(
                    "in_reply_to_status_id", None)
                lang = tweet.get("lang", None)

                if not id or \
                        not id_str or \
                        not created_at or \
                        not text or \
                        not hashtags or \
                        not user_id or \
                        not user_id_str or \
                        id in ids or \
                        lang not in languages:
                    continue

                elif hashtags and len(hashtags) == 0:
                    continue
                else:
                    ids.append(id)
                    if in_reply_to_user_id is not None and in_reply_to_status_id is not None:
                        tweet_type = "reply"
                        reply_to_tweet_id = in_reply_to_status_id
                        reply_to_user_id = in_reply_to_user_id

                    if retweeted_status is not None:
                        tweet_type = "retweet"
                        retweet_to_tweet_id = retweeted_status.get("id", None)
                        retweet_to_user_id = retweeted_status["user"].get(
                            "id", None)

                    tags = []
                    for tag in hashtags:
                        if u"{0}".format(tag["text"]) not in excluded_hashtags:
                            tags.append(u"{0}".format(tag["text"]))
                            ht = {
                                "tweet_id": id,
                                "user_id": user_id,
                                "hashtag_name": u"{0}".format(tag["text"])
                            }
                            if ht not in hashtag_table:
                                hashtag_table.append(ht)
                                hashtag_table_values = [
                                    id, user_id, u"{0}".format(tag["text"])]

                                cur.execute(hashtags_table_insert,
                                            hashtag_table_values)

                    text = u"{0}".format(text)
                    user_description = u"{0}".format(
                        user_description) if user_description else None
                    hash_tags = ",".join(tags)

                    values = [id, created_at, text, user_id, user_screen_name, user_description,
                              tweet_type, reply_to_tweet_id, reply_to_user_id, retweet_to_tweet_id, retweet_to_user_id, hash_tags]

                    cur.execute(tweets_table_insert, values)

                    if user_id not in user_ids:
                        user_ids.append(user_id)
                        screen_name = user.get("screen_name", None)
                        description = user.get("description", None)
                        name = user.get("name", None)
                        user_created_at = user.get("created_at", None)
                        user_values = [user_id, screen_name,
                                       u"{0}".format(
                                           description) if description else None, name, user_created_at]

                        cur.execute(users_table_insert, user_values)

                    if reply_to_user_id and reply_to_user_id not in user_ids:
                        user_ids.append(reply_to_user_id)
                        user_values = [reply_to_user_id,
                                       in_reply_to_screen_name, None, None, None]
                        cur.execute(users_table_insert, user_values)

                    if retweeted_status:
                        retweeet_to_user_id = retweeted_status["user"].get(
                            "id")

                        if retweeet_to_user_id not in user_ids:
                            user_ids.append(retweeet_to_user_id)
                            screen_name = retweeted_status["user"].get(
                                "screen_name", None)
                            description = retweeted_status["user"].get(
                                "description", None)
                            name = retweeted_status["user"].get("name", None)
                            user_created_at = retweeted_status["user"].get(
                                "created_at", None)
                            user_values = [retweeet_to_user_id, screen_name,
                                           u"{0}".format(
                                               description) if description else None, name, user_created_at]

                            cur.execute(users_table_insert, user_values)

            except ValueError:
                continue

            print(f"Line {i} is done.")
    print(len(ids))
    print(len(hashtag_table))
    print(len(user_ids))


def main():

    host = 'localhost'
    port = '5432'
    dbname = 'pivot_db'
    user = 'postgres'
    password = 'password'

    conn = psycopg2.connect(host=host, port=port, user=user,
                            dbname=dbname, password=password)
    cur = conn.cursor()

    process_tweets_file(cur)
    conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
