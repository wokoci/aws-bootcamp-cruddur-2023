.PHONY: npm
npm:
	cd frontend-react-js; npm i 
	cd ..

build:
	echo "building froment reack docker image"
	docker build -t  backend-flask ./backend-flask
	echo "building backend python docker image"
	docker build -t frontend-react-js ./frontend-react-js


run:
	echo "starting app"
	docker run --rm -p 4566:4567 -it -d -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
	docker run -p 3000:3000 -d frontend-react-js

stop:
	echo "stopping running containers"
	docker container stop $(docker container ls -aq)



clean:
	echo "removing all docker images"
	docker rmi $(docker image ls -aq)