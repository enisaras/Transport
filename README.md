
  # Transport
  Transport uses the [NYC Open Data](https://opendata.cityofnewyork.us/) to predict the best method of transportation 
  to get from point A to B based on user preferences. It not only considers factors like traffic, bus routes and subway
  maintance, but also environmental factors like air quality and carbon footprint. Goal of the project is to make 

  ## Architecture Diagram

  ![Architecture Diagram](https://github.com/enisaras/Transport/blob/main/diagrams/DataEngineeringProject.png)
  ## Technologies utilized
  Transport is deployed in an Amazon EKS cluster. Each namespace in the cluster represents a step in the data process. Even though
  it is code agnostic, vast majority of the code is written in python, my preffered language for data engineering and science.
  Below is a quick list of each step and what is deployed in each namespace.
  
  ### Step 1: Gathering Data
    Data comes into the application in two forms:

    1. Real-time data: subway trip data, traffic data.

    2. Batch data: Taxi trip data, subway utilization, subway stops and routes.

    For a list of all datasets and APIs used in this project, please refer to
    the data section.
  ### Step 2: Data preperation and wrangling
    Once we have identified the data sources, the next step is to perform
    ETL on this data.

    To extract the data we make requests to each API endpoint, endpoints
    used in this project can be found in their respective folders.

    As an orchestration tool for batch data, we use [Apache Airflow](https://airflow.apache.org/). Airflow is a powerful ETL tool that works really well in Kubernetes deployments through its KubernetesOperator. Airflow uses a PostGres database to store its operation metadata. We build and deploy airflow from scratch but keep in mind there are many managed solutions out there for Airflow that can be used interchangeably with less setup effort.

    For streaming real-time data, we will use Apache Kafka. Kafka streams work with producers, which send data to a Kafka cluster, and consumers, which read the data by subscribing to a Kafka topic. Please refer to the architecture diagram below for an example.

    [Kafka Real-Time Streaming](https://github.com/enisaras/Transport/blob/main/diagrams/MTAKafkaExample.png)

  ### Step 3: Analyze and Develop Model

  ### Step 4: Train and Test Model

  ### Step 5: Deploy Model


  ## Data
  [NYC Subway Lines](https://data.cityofnewyork.us/Transportation/Subway-Lines/3qz8-muuu)

  [2021 Yellow Taxi Trip Data](https://data.cityofnewyork.us/Transportation/2021-Yellow-Taxi-Trip-Data/m6nq-qud6)

  [Real Time Traffic Speed Data](https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/qkm5-nuaq)

  [NYC Bike Routes](https://data.cityofnewyork.us/Transportation/New-York-City-Bike-Routes/7vsa-caz7)

  [NYC Bicycle Counters](https://data.cityofnewyork.us/Transportation/Bicycle-Counters/smn3-rzf9)
  
  
  ## Screenshots
