## GCloud Kubernetes project
This Project shows how can you implement a base Kubernetes infrastructure in Gcloud using gcloud cli and python to create a rest api with basic operations. 
The application consist in 2 API endpoints which interact with a redis instance to update and read the value of a key. The key it's a counter which can be incremented or read.

## Installation
We start form the assumption that you have a runner or virtual machine with the required software installed. The software required for this is:
* Docker -> https://docs.docker.com/engine/install/
* Kubectl -> https://kubernetes.io/docs/tasks/tools/
* curl -> https://help.ubidots.com/en/articles/2165289-learn-how-to-install-run-curl-on-windows-macosx-linux

And depending the type of this project execution, you will need Minikube or GCloud:
* Minikube(Optional) ->https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download
* Gcloud CLI (Optional)-> https://cloud.google.com/sdk/docs/install

In case you don't have any of these, just follow the instructions to install. Install it's pretty straightforward and no further configuration is required for this.

## Setup 
While uncompressing the file you will see the following files:
* Dockerfile: File with the contruction and instructions for the container creation.
* app.py: Rest API application file in Python language with 2 endpoints to operate with redis.
* deploy.sh: Shell script to deploy the application in the corresponding host/runner.
* k8s/*: Deployment and Services manifests for the application and redis services.

## Deployment
In order to deploy you need to provide a wayt to connect to the cluster. For this example we are using minikube but you can use any Kubernetes provider. For Gcloud I let a basic example using GitHub Actions for a personal acccount in GKE in: https://github.com/dvalleit/k8s_example/blob/main/.github/workflows/action.yml

## Execution
To execute you need to allow the system to execute the script file first, then run the code:
```
chmod +x deploy.sh
./deploy.sh
```

Now in a different terminal window execute **minikube tunnel**

**Done!**

The application should be runnind and available in localhost [127.0.0.1:80 ](http://127.0.0.1/)

To interact with the app you can do from:
1. Browser - Get current counter value [http://127.0.0.1/get](http://127.0.0.1/get)
2. Curl call:
    1. Get current counter value: 'curl http://127.0.0.1/get'
    2. Increment the counter: 'curl -X POST -H "Content-Type: application/json" http://127.0.0.1/post'



## Extra considerations for this project
* This guide considers you have docker pointing to minikube, in case you don't have it run
```
eval $(minikube docker-env)
```
* redis-client.yml file it's only to validate the redis connection, not required for the purpose of the project


## Security considerations
* Safe and trusted container registry/hub
* Minimal base image usage 
* Use of env vars PYTHONUNBUFFERED and PYTHONDONTWRITEBYTECODE 
* Non root user 
* Image vulnerability scans with 3rd party tools
* With an ingres controller it's possible to create a ingress and expose only a domain for the service itself
* Limit resources
* Limit capabilities
* Image udpated if required
* sign images
* No new privileges
* Readonly fs
* Docker secrets
* This app doesn't contain an ingress given it was not required but obviously for security res


## More Security
In order to secure this more you could set service type as NodePort and use an ingress
To use you need to:
1. Enable ingress on minikube
```minikube addons enable ingress
```
2. Modify service type to NodePort and port to 8080
3. Create ingress in k8s folder
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: service-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: flask-api-service.task
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: flask-api-service
                port:
                  number: 8080
```
4. Execute again the deploy.sh script
5. Kill **minikube tunnel** command with Ctrl+C and run it again
6. Execute the following command in a new terminal:
```
curl --resolve "flask-api-service.task:80:127.0.0.1" -i http://flask-api-service.task
```

