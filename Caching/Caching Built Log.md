## Intro
- *Caching is a crucial component of the layered architecture of the search application, typically used to improve user experience by reducing waiting time and server workload.
- Goal Define: I/O operations (querying databases, network services)

# Redis as Cache
## Cache framework selection
### 1. Redis as Cache
- *Memcached vs. Redis
	
	- both are
		- NoSQL key-value in-memory data storage systems
		- Open source
		- Used to speed up applications
		- Support sub-millisecond latency
		
	- selection
		- Redis outperforms Memcached by offering richer functionality and features promising for complex use cases.
			
			- *data structure; secondary database model; different types of eviction policies.
			- in case we need to add information like images and geographic locations to the cache.

|          Parameter           |                                                 REDIS                                                 |                      MEMCACHED                      |
|:----------------------------:|:-----------------------------------------------------------------------------------------------------:|:---------------------------------------------------:|
|       Initial Release        |                                       It was released in 2009.                                        |              It was released in 2003.               |
|          Developer           |                               It was developed by Salvatore Sanfilippo.                               |       It was developed by Danga Interactive.        |
|          Cores Used          |                                         It uses single cores.                                         |               It uses multiple cores.               |
|     ==Length of a key==      |                                 In Redis, maximum key length is 2GB.                                  |   In Memcached, maximum key length is 250 bytes.    |
|         Installation         |                     It is simple and easier to install as compared to Memcached.                      |           It may be difficult to install.           |
|      ==Data Structure==      |                    It uses string, hash, list, set, sorted set as data structure.                     | It uses only string and integers as data structure. |
|            Speed             |                          It reads and writes speed is slower than Memcached.                          |   It reads and writes speed is higher than Redis.   |
|         Replication          |              It supports Master-Slave Replication and Multi-Master Replication  methods.              |     It does not support any replication method.     |
|        ==Durability==        |                                  It is more durable than Memcached.                                   |           It is less durable than Redis.            |
| ==Secondary database model== | It has Document Store, Graph DBMS, Search Engine, and Time Series DBMS as  secondary database models. |        It has no secondary database models.         |
|         Persistence          |                                       It uses persistent data.                                        |          It does not use persistent data.           |                                                                             
|      Geospatial Support      |              ✅                                                                                       |    ❌                                                 |

[[Redis-vs-Memcached-Infographic-ScaleGrid-Blog.pdf]]

[Difference between Redis and Memcached - GeeksforGeeks](https://www.geeksforgeeks.org/difference-between-redis-and-memcached/)  
[Redis Vs Memcached - 2021 Comparison, Features](https://scalegrid.io/blog/redis-vs-memcached-2021-comparison/)  
[caching - If redis is already a part of the stack, why is Memcached still used alongside Redis? - Stack Overflow](https://stackoverflow.com/questions/23601622/if-redis-is-already-a-part-of-the-stack-why-is-memcached-still-used-alongside-r/23650189#23650189)  
[caching - Memcached vs. Redis? - Stack Overflow](https://stackoverflow.com/questions/10558465/memcached-vs-redis)  
[Redis vs Memcached: which one to pick? (imaginarycloud.com)](https://www.imaginarycloud.com/blog/redis-vs-memcached/)  
[Memcached vs Redis | Baeldung](https://www.baeldung.com/memcached-vs-redis)  

### 2. Cache-Aside Pattern as Cache Mode
The cache contains only data that the application requests, which helps keep the cache size cost-effective.   
*However, some overhead is added to the initial response time because additional roundtrips to the cache and database are needed. (some trade-off to use cache).

- **The reading procedure is showed as below**: (cache hit / cache miss)

  <img src="/Users/cyan/Documents/Obsidian Vault/Attachment/cache side pattern - read.jpeg" alt="cache side pattern - read" style="zoom:60%;" />

- The order for writing is swapped based on the default process (attached below) in this project for better consistency. Nevertheless, this order may lead old data into the cache. 

  <img src="/Users/cyan/Documents/Obsidian Vault/Attachment/cache side pattern - write.jpeg" alt="cache side pattern - write" style="zoom:60%;" />

[Consistency between Redis Cache and SQL Database | Yunpeng's Blog (yunpengn.github.io)](https://yunpengn.github.io/blog/2019/05/04/consistent-redis-sql/)

### 3. Attributes Structure Exploration

- There are several types of tweets
	- original 
	- reply
	- quote
	- retweet
- Attributes Structure
	-  \# of fundamental attributes: 28
	- optional attributes
		- retweets can be distinguished from typical Tweets by the existence of a `retweeted_status` attribute.
		- `display_text_range` & **`extended_tweet`** when `truncated` is True.
		- `quoted_status_id` & `quoted_status_id_str` when the Tweet is a quote Tweet.
	- Main objects
		- Parent object
			- Tweet
				- Tweets are the basic atomic building block of all things Twitter. Tweets are also known as “status updates”.
		- Child objects
			- User
				- User objects can be retrieved using the `id` or `screen_name`.
				- The User object contains Twitter User account metadata that describes the Twitter User referenced.
					- e.g. In case of Retweets and Quoted Tweets
						- the top-level `user` object represents what account took that action.
						- the JSON payload will include a second `user` within the `retweeted_status` for the account that created the original Tweet.
				- In general these `user` metadata values are relatively constant.
			- Entities
				- Entities provide metadata and additional contextual information about content posted on Twitter.
			- Extended entities
				- When it comes to any native media (photo, video, or GIF), the extended_entities is the preferred metadata source.
				- If a Tweet contains native media (shared with the Tweet user-interface as opposed via a link to elsewhere), there will also be a extended_entities section.
				- For all Tweets with more than one photo, a video, or animated GIF, the reader is directed to the `extended_entities` section.

[Tweet object | Docs | Twitter Developer Platform](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet)  
[Extended entities object | Docs | Twitter Developer Platform](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/extended-entities)

### 4. Schema Design
See the highlight part of `twitter_data_dictionary.xlsx` file.

### 5. Data Store using Redis OM for Python

- [Redis OM Python](https://github.com/redis/redis-om-python) is a Redis client that provides high-level abstractions for managing document data in Redis.
  - *Provides Model classes, such as `HashModel` and `JsonModel`, which function similarly to Pydantic models, by automatically validating data using a defined schema to ensure correct formats before use.

  - Thus leads to fast performance, save development time and reduce the risk of errors.

- Build JsonModel class with Redis OM 
  - *Considering that there are nested structures, such as `user` object and `entities` object being the next level of `tweet` object, use `JsonModel` and `EmbeddedJsonModel` here.
  - Set second indexing for searching by various attributes
    - `index = True` in `JsonModel`
    - *Basically, set `id_str`, `user.id_str`, `user.screen_name`, `entities.hashtags.text`, `user.followers_count`, `text`, `created_at` as indicies to support searches by string, user and hashtag.
- *Eviction policy setting
  - Set TTL for 1 day (24\*3600) in general to handle stale data.
  - Set the maxmemory to 5MB, which is approximately 2,000 entries.
  - Set the eviciton policy as `volatile-lfu`, which evicts the least frequently used keys from those that have a TTL set
    - let the searches itself decide what are the popular contents.
    - [Key eviction | Redis](https://redis.io/docs/reference/eviction/)


[redis-om-python/getting_started.md at main · redis/redis-om-python (github.com)](https://github.com/redis/redis-om-python/blob/main/docs/getting_started.md)	

[Introducing Redis OM For Python | Redis](https://redis.com/blog/introducing-redis-om-for-python/)	

[redis-om-python/models and fields (github.com)](https://github.com/redis/redis-om-python/blob/main/docs/models.md)

[Redis OM Python with Flask | Redis](https://redis.io/docs/stack/get-started/tutorials/stack-python/)

[Redis OM (Python) issues - Redis client libraries (Java, Python, JS, etc.) - Redis Community Forum](https://forum.redis.com/t/redis-om-python-issues/1639)

- Querying for Models With Expressions
  - [redis-developer/redis-om-python-flask-skeleton-app: A starter application for performing CRUD type operations with Redis OM Python and the Flask Microframework (github.com)](https://github.com/redis-developer/redis-om-python-flask-skeleton-app#find-a-person-by-id)
  - [Redis OM Python | Redis](https://redis.io/docs/stack/get-started/tutorials/stack-python/#start-the-flask-application)

### 6. Optimization
- initial cache content - later
	- "popular" by user/hashtags
	- SCD (slowly changing dimension)
- invalid strategy - eviction policies
	- invalidate it when changed
	  - slowly changing dimension
	  - updated data

### 7. Evaluation

## Practice
- Redis installation
	- Install Redis on macOS
		```bash
	  # install Redis on the system
	  brew install redis 
	  
	  # start the process in the background
	  brew services start redis 
	  
	  # check status
	  brew services info redis
	  # check the version of redis server
	  redis-server --version
	  
	  # to stop the service
	  brew services stop redis 
	  
	  # open the Reids REPL
	  redis-cli
	  ```
	- Redisearch Installation via Docker (the redis-stack Docker image)
		```dockerfile
		# via Docker
		% docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
		
		# check if it's installed
		% redis-cli
		module list
		```
		
	- Connect Python to a Redis database
	
	  ```python
	  # install redis-py
	  pip install redis
	  
	  # connect
	  r = redis.Redis(host='localhost', port=6379,
	  decode_responses=True)
	  ```
- Redis Start & Shut down via Docker
	```dockerfile
	# 1. Start a redis via docker & enter redis-cli
	docker run -p 6379:6379 -it redis/redis-stack:latest
	
	# or start a redis server
	docer run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
	# 2. or start the whole redis-stack (along with redisinsight)
	docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest # 8001 for redisinsight
	# docker start containerID # to start an exsiting container
	# 3. Enter redis-cli
	docker exec -it redis-stack redis-cli
	# 127.0.0.1:6379 # connect by another device
	
	# 4. check status
	docker ps
	
	# 5. Shut down via docker
	docker-compose down
	```
	- [RediSearch quick start](https://redis.io/docs/stack/search/quick_start/)
	- [Run Redis Stack on Docker](https://redis.io/docs/stack/get-started/install/docker/)
	- [Add a Redis database | Redis Documentation Center](https://docs.redis.com/latest/ri/using-redisinsight/add-instance/)

## References
- `redis-py`
	- [Python guide | Redis](https://redis.io/docs/clients/python/)
	- [GitHub](https://github.com/redis/redis-py)
	- [Command Reference](https://redis-py.readthedocs.io/en/stable/commands.html)
	- [Tutorials](https://redis.readthedocs.io/en/stable/examples.html)

## Troubleshooting Log
- Cannot use command like `FT.CREATE` in Python 
	- is from `RediSearch` module;
	- need to install RediSearch module in Redis Server.
	
- Multiple connected Clients
	- config timeout to remove idle clients.
	
	  `config set time out 3600`
	
- Index setting are not in effect when building an embedded sub-model `twt_user` with Redis OM

  - add the below to the schema class and run `Migrator().run()` after saving data into Redis.
  - `class Meta:
            database = get_redis_connection()`
  - Ref: [Redis OM (Python) issues - Redis client libraries (Java, Python, JS, etc.) - Redis Community Forum](https://forum.redis.com/t/redis-om-python-issues/1639)

- Cannot import some package after installation 
  - `pip show packagename` to provide the location of the installed package;
  - `import sys; sys.path` to show where Python searches for any packages imported;
  - `sys.path.append('package_location_seen_in_step_1')` .
  
- Cannot push to the repo using username and password
  
  - need to generate token and use username and token to push
  
  - [git - Support for password authentication was removed on August 13, 2021 - Stack Overflow](https://stackoverflow.com/questions/68781928/support-for-password-authentication-was-removed-on-august-13-2021)
  
- Set localhost Redis data can be visited by another device

  - set password 
    - `redis 127.0.0.1:6379> CONFIG SET requirepass "7ptbtptp"`
      - remove password: `redis 127.0.0.1:6379> CONFIG SET requirepass "7ptbtptp"`
      - `config get requirepass`
    - `redis 127.0.0.1:6379> AUTH 7ptbtptp`
    - Ref: [php - How to set password for Redis? - Stack Overflow](https://stackoverflow.com/questions/7537905/how-to-set-password-for-redis)
  - `/usr/local/etc/redis.conf` to revise the bind command
    - `bind 127.0.0.1` -> `bind IPaddress`
  
  - How to connect to a Redis Database
    - `redis-cli -h 172.31.139.108 -p 6379 -a 7ptbtptp`
      - `ifcofig` to get IP address
    - `auth 7ptbtptp` to query data
    - `ping` testing connnection
    - Ref: [How To Connect to a Redis Database | DigitalOcean](https://www.digitalocean.com/community/cheatsheets/how-to-connect-to-a-redis-database)

- Run MongoDB

  ```
  # start
  brew services start mongodb-community@6.0
  
  # stop
  brew services stop mongodb-community@6.0
  
  # import
  mongoimport --db 694db_nsdb --collection twt --jsonArray  --file /Volumes/Dish/corona3_sorted_tweets_processed.jsonf
  ```


- Run MySQL
	```
	# download MySQL for Mac
	brew install mysql
	
	# connection
	mysql -u root -p 694RDBMS
	
	# start with MySQL.prefPane
	# or
	brew services start mysql
	
	# import data
	mysql -u root -p 694RDBMS < /Volumes/Dish/694RDBMS.sql
	```

- You need to run docker, start Redis, run MongoDB and MySQL for initialization.

# Python Dictionary as Cache

## Requirements

- Design and implement a cache for storing "popular" (frequently  accessed) data so that this data does not have to be retrieved from the  database each time it is accessed.   
  - Some hashtags/users may be popular and their data may be cached.   
- You can use a Python dictionary for implementing the cache, but you must :
  - limit the size of the dictionary by evicting entries using a strategy (E.g. least accessed). 
  - You must checkpoint your data on disk at periodic intervals. 
  - When your search application starts up, you must reload the state of the cache from the disk. 
- Questions to consider 
  - Can an entry in the cache get stale (is not representing the correct state)? 
  - How will you update or purge stale data? 
  - An advanced feature that you could implement is an expiry mechanism  for an entry in the cache by having a Time-To-Live field for each entry  that determines the amount of time the entry will be retained in the  cache. 
- Timings of your test search queries (make sure you are hitting cached and non cached data)
