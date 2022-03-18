# Create tables
tweets_table_create = ("""CREATE TABLE IF NOT EXISTS tweets
 (tweet_id bigint NOT NULL PRIMARY KEY, created_at timestamp NOT NULL, text varchar NOT NULL, user_id bigint NOT NULL, user_screen_name varchar,
 user_description varchar, tweet_type varchar, reply_to_tweet_id bigint, reply_to_user_id bigint, retweet_to_tweet_id bigint, retweet_to_user_id bigint, hashtags varchar);
 """)

hashtags_table_create = ("""CREATE TABLE IF NOT EXISTS hashtags
 (id SERIAL PRIMARY KEY, tweet_id bigint NOT NULL, user_id bigint NOT NULL, hashtag_name varchar NOT NULL,
 CONSTRAINT tweet_user_hashtag UNIQUE(tweet_id,user_id,hashtag_name));
 """)

users_table_create = ("""CREATE TABLE IF NOT EXISTS users
 (id SERIAL PRIMARY KEY, user_id bigint NOT NULL, screen_name varchar NULL, description varchar NULL,
 name varchar NULL, created_at timestamp NULL);
 """)

# Drop tables
tweets_table_drop = "DROP TABLE IF EXISTS tweets;"
hashtags_table_drop = "DROP TABLE IF EXISTS hashtags;"
users_table_drop = "DROP TABLE IF EXISTS hashtags;"

# Insert values
tweets_table_insert = ("""INSERT INTO tweets
 (tweet_id, created_at, text, user_id, user_screen_name, user_description, tweet_type, reply_to_tweet_id, reply_to_user_id, retweet_to_tweet_id, retweet_to_user_id, hashtags) 
 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
 ON CONFLICT DO NOTHING;
""")

hashtags_table_insert = ("""INSERT INTO hashtags
 (tweet_id, user_id, hashtag_name) 
 VALUES (%s, %s, %s)
 ON CONFLICT DO NOTHING;
""")

users_table_insert = ("""INSERT INTO users
 (user_id, screen_name, description, name, created_at) 
 VALUES (%s, %s, %s, %s, %s)
 ON CONFLICT DO NOTHING;
""")

create_table_queries = [tweets_table_create,
                        hashtags_table_create, users_table_create]
drop_table_queries = [tweets_table_drop, hashtags_table_drop, users_table_drop]
