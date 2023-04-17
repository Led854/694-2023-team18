## Goal Define
- I/O operations (querying databases, network services)

## Cache framework selection
### 1. cache tool & storage location
- Memcached `pymemchache` vs. ==Redis==
	- both are
		- NoSQL key-value in-memory data storage systems
		- Open source
		- Used to speed up applications
		- Support sub-millisecond latency
	- selection
		- Redis outperforms Memcached by offering richer functionality and various features that are promising for complex use-cases.
			- data structure; secondary database model; different types of eviction policies.
			- in case to add information like images or geographic location information to the cache.

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

### 2. cache structure
- dictionary

### 3. cache content
- "popular" by user/hashtags
- SCD (slowly changing dimension)

### 4. invalid strategy - eviction policies
- use some of the eviction policies redis supports
	- volatile-ttl
	- allkeys-lfu
- set a time for invalidation
	- for those time-sensitive data
- invalidate it when you want
	- slowly changing dimension: when changed
	- updated data

### 5. other optimization
### 6. evaluation

## Practice
- Redis installation
	- Install Redis on macOS
		```
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
	- Connect Python to a Redis database
		```
		# install redis-py
		pip install redis
		
		# connect
		r = redis.Redis(host='localhost', port=6379,
		decode_responses=True)
		```
- Redisearch Installation
	```
	# via Docker
	% docker run -d --name redis-stack-server -p 6379:6379
	redis/redis-stack-server:latest
	
	# check if it's installed
	% redis-cli
	module list
	```
	- [RediSearch quick start](https://redis.io/docs/stack/search/quick_start/)
	- [Run Redis Stack on Docker](https://redis.io/docs/stack/get-started/install/docker/)

## References
- `redis-py`
	- [Python guide | Redis](https://redis.io/docs/clients/python/)
	- [GitHub](https://github.com/redis/redis-py)
	- [Command Reference](https://redis-py.readthedocs.io/en/stable/commands.html)
	- [Tutorials](https://redis.readthedocs.io/en/stable/examples.html)

## Issue Resolution Log
- Cannot use command like `FT.CREATE` in Python 
	- is from `RediSearch` module
	- need to install RediSearch module in Redis Server
