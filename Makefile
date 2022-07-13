.PHONY: vendor
vendor:
	pip3 install -r requirements.txt --python-version 3.10 --platform manylinux2014_x86_64 --only-binary=:all: --target=./vendor

.PHONY: deploy
deploy:
	rm -rf vendor
	make vendor
	neru deploy

.PHONY: start
start:
	python3 main.py

.PHONY: debug
debug:
	# python3 main.py
	nodemon --exec python3 -m debugpy --listen localhost:9229 --wait-for-client main.py
	# nodemon --exec python3 -m debugpy --listen localhost:9229 --wait-for-client main.py