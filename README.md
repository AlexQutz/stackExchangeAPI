# StackStats API

The StackStats API is a RESTful service that retrieves data from the StackExchange API, calculates various statistics, and provides them to the user. The API is designed to be a long-running service with caching capabilities to improve performance.

## Prerequisites
- In order to run the API successfully you will need to have Docker installed on your local machine.
- If you don't already have it installed , navigate to [Docker's official website](https://www.docker.com/get-started) for the instructions.
- It will be useful to have Postman installed also for testing the answers, so optionally head to [Postman's official website](https://www.postman.com/downloads/) and download it.

## Features

- Retrieve StackOverflow answer data for a given date/time range.
- Calculate statistics such as the total number of accepted answers, average score for accepted answers, and more.
- Cache responses to improve performance and reduce load on the StackExchange API.

## Getting Started

To use the StackStats API, follow these steps:

1. Unzip the folder from the python-assignment
2. Open a terminal inside the Obrela folder
3. Run

   ```bash
   docker-compose up --build
4. Congratulations you know run the StackStats API!!!


## Example request

- http://localhost:5000/api/v1/stackstats?since=2017-01-01 14:30:00&until=2022-01-31 14:30:00


## Example response
    
    ```json
    {
        "total_accepted_answers": 6,
        "average_score_accepted_answers": 0.8333333333333334,
        "average_answer_count_per_question": 1.0344827586206897,
        "top_10_comments_count": {
            "70927643": 2,
            "70927641": 1,
            "70927677": 0,
            "70927640": 2,
            "70927686": 3,
            "70927673": 0,
            "70927653": 0,
            "70927652": 1,
            "70927647": 8,
            "70927644": 1
        }
    }

## Run the unit test

 While having the docker container up, open a terminal in the Obrela folder location and run:

 ```bash
 python unit_test.py

