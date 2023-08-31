# orderbook

## Content
* [Technology stack](#technology-stack)
* [Commands overview](#commands-overview)
	* [Build project](#build-project)
	* [Run project](#run-project)
	* [Stop project](#stop-project)
* [Extend functionality](#extend-functionality)

## Technology stack
All project is wrapped into **Docker compose**.
There are 5 services total:
1. Kafka
2. Zookeeper
3. Fetcher
4. Dashboarder
4. Storage

**Kafka and Zookeeper** are help services to manage broker configuration. Kafka was used as a message queue (an alternative is RabbitMQ e.g.), because after fetching data from Binance API we need to visualize and store it. To keep this logic separated and because fetching data is a continuous process we need to implement some streaming logic. 

The main goal of the project was to fetch data from Binance API and then visualize and store it. Because fetching data is continuous a process we need to implement some streaming logic. Kafka was used as a message queue (alternative is RabbitMQ e.g.) hence Kafka and Zookeeper are help services to manage broker configuration.

**Fetcher** is a service responsible for fetching data and producing it to Kafka topic.

**Dashboarder** is a service to visualize data. On a regular basis, the last message is consumed from a topic and then transformed into a simple orderbook table presentation and depth graph chart. To make this visualization Plotly Dash framework is used.

**Storage** is a service to save data. Data is consumed from a topic, transformed to a unified view, and then stored in PSQL database hosted on AWS RDS instance was picked 

## Commands overview
To manipulate with a project you need to clone it.
### Build project
To **build** a project run this command
```
make build-project
```
### Run project
To **run** a project run this command
```
make run-project
```
When the project is running you can visit `http://127.0.0.1:8050/` to check real time orderbook dashboard visualizations.
To check data inside PSQL database use PgAdmin or any other similar program.
Credentials can be found inside `docker-compose.yml` file in storage service under environment configuration.

### Stop project
To **stop** a project run this command
```
make stop-project
```

## Extend functionality
You can easily switch a pair of currencies by changing the `SYMBOL env variable` inside `docker-compose.yml`.
Also, other charts can be built to visualize real-time orderbook updates. This can be done via transforming data to a needed format and adding extra output fields to Plotly Dash.

Because we are using Kafka we can easily create other consumers to do other tasks with real time data, for example, store data in other SQL and NoSQL databases(depending on a business goals), attach some ML models to do real-time predictions or other calculations.
Also, other frameworks can be used to visualize data: for example, Django can be used on top of a PSQL database and more complex platform for data visualization can be implemented if needed.

