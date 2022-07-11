.PHONY: vendor
vendor:
	pip3 install -r requirements.txt --target=./vendor

.PHONY: start
start:
	python3 main.py
debug:
	nodemon --exec python3 -m debugpy --listen localhost:9229 main.py