
  # Transport
  Transport uses the [NYC Open Data](https://opendata.cityofnewyork.us/) to predict the best method of transportation 
  to get from point A to B based on user preferences. It not only considers factors like traffic, bus routes and subway
  maintance, but also environmental factors like air quality and carbon footprint. Goal of the project is to make 

  ## Architecture Diagram

  ## Technologies utilized
  Transport is deployed in an Amazon EKS cluster. Each worker node in the cluster represents a step in the data process. Even though
  it is code agnostic, vast majority of the code is written in python, my preffered language for data engineering and science.
  Below is a quick list of each step and what is deployed in the worker node.
  
  ### Step 1: Gathering Data

  ### Step 2: Data preperation and wrangling

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
