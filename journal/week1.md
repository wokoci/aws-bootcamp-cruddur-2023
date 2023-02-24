# Week 1 — App Containerization


To start docker with environment variables, we use
~~~
FRONTEND_URL="*" BACKEND_URL="*" 

build docke image for the backend with:


To run docker with environment variables, use the following:

docker run -p 4567:4567 -e FRONTEND_URL='*' -e BACKEND_URL='*'  backend-flask
~~~

Created a docker file for the frontend React js application and ran the following docker command to build the docker image for the frontend
~~~
docker build -t frontend-react-js ./rontend-react-js
~~~

Run the frontend app with :
~~~
docker run -p 3000:3000 -d frontend-react-js
~~~


Ran npm command to install all needed dependences need to run node as well npm audit for fix potential vulnerabilities.
~~~
npm install 
npm audit fix --force
~~~

with all the images created, the output of docker images will like what's been build 

![docker images](./assets/docker.jpg)




