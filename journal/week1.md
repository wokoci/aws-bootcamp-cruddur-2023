# Week 1 — App Containerization


To start docker with environment variables, we use
~~~
FRONTEND_URL="*" BACKEND_URL="*" 
To run docker with environment variables, use the following:

docker run -p 4567:4567 -e FRONTEND_URL='*' -e BACKEND_URL='*'  backend-flask
~~~