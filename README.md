# BeatAssessment

## Introduction

This is a project regarding my application to Beat for the position of Site Reliability Engineer.

## Deployment

The application is production ready so the code is packaged as a Docker image and is stored in my public repository at Dockerhub (nikosleventis/beatassessment).
The v0.6 is the latest stable image and it can be used to production.
In order to deploy the image in a K8s environment use deploy-beatassessment.yaml and run the following command:
`kubectl apply -f deploy-beatassessment.yaml`

The above command will create a deployment and a Nodeport K8s service.
**You will need internet access from your K8s cluster to download the image from Dockerhub.
If you don't have internet connection then create an image to the locan Docker repository by running:**
`docker build -t nikosleventis/beatassessment:v0.6`

## Access the application

Application is hosted on port 5000 and is available through a Nodeport service.
Before accessing the application run:
`kubectl get services`
This command will reveal the Nodeport Cluster IP.
Then you can access the applicatin like this:
`curl http://<your-Nodeport-ClusterIP>:5000/stories`

**The application takes arround 3 minutes to run.**

## Implementation

This is a Python application that uses Flask framework.
Flask spins up a web server that listens for GET /stories requests on port 5000.

All logic is handled by `buildStories()` function on backend.py file.
At first a call to HackerNews API is made to receive the 500 latest stories. Then for every story two calls are made until reaching the TOP 50 stories. One to fetch the metadata of the story and one more to fetch the user's data.
In order to reduce overall response time of the application I use a Session object with `pool_connections=10`. This way the TCP connections to HackerNews API persist.

Regarding `position` I used the Insertion Sort algorithm and a two dimensional position list.
The position list contains in each row a list with two values that are associated with a particular story. In the first column, the number of comments are stored while in the second column the index that the story has in the TOP 50 stories is stored.
For every new story that belongs to the TOP 50 the Insertion Sort algorithm is called to sort the position list according to the number of comments.

At the end, when the `stories` dictionary contains the TOP 50 stories the `fixPositions` function is called to assign the correct position to every story.
Position assignment can only happen at the end when the TOP 50 stories are selected. Only then you know the number of comments of all stories. My implementation doesn't wait until all stories are collected. Position list is sorted every time a new story is added using the Insertion Sort algorithm.

Monitoring metrics like HackerNews API request latency for each request and the total number of incoming requests served are reported using logging.
The logs are streamed to the stdout where the Kubernetes can access them.
You can access these metrics running: `kubectl logs <pod-name>`

## Further ideas

### Response time

The application takes arround 3 minutes to execute. This is due to the high number of GET requests that my application does to the HackerNews API.
Some general ideas that could reduce the overall response time are:

1. Increase the number of connection pool.
2. Add more threads so that requests execute in parallel.
3. Use another sorting algorithm.

### Monitoring

For monitoring we could use:

1. Code instrumentation and send the metrics to a monitoring tool like Prometheus.
2. Use a log extractor like Fluentd to extract the logs.

### Deployment

For deployment I would use a private image repository.
