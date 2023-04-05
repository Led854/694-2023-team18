# Datastores & Search Application Design
<p align="center">
<img src="https://user-images.githubusercontent.com/129342767/229957140-c46cc804-19f8-4cfa-bbab-baed59cb9eb2.png" width="600" />
</p>

## Loads:
- 10 mins presentation
- 8 slides
- 8-10 pages of report

## Delivery
- Introduction
- Dataset
- Persisted Data Model and Datastores
  - Describe your user and tweet data model in detail (preferably with diagrams).
  - Describe how you stored the data in the datastores.
  - What did you optimize for? What were the tradeoffs?
  - Did you create any indexes for the datastores?
- Processing tweets for storing in datastores
  - Make sure that you processed the tweets and stored the information (users, tweets) in the datastores one at a time (DO NOT load all the data into a dataframe and then load the dataframe into the datastore)
- Search Application Design
  - What types of searches are allowed? What kinds of drill-downs are allowed?
  - How were search queries translated into queries for the datastores?
  - What was your notion of relevance (i.e. how did you order the results of the search queries)?
  - How is the cache used?
- Results
  - Show the results of each type of query.
  - Timings of your test search queries (make sure you are hitting cached and non cached data)
- Conclusions
  - What are your conclusions regarding your design and experiments?
  - What did you learn from the project?
- References
- List what each team member did for the project.

## Part of the project
- relational datastore
- non-relational datastore
- cache
- search application
