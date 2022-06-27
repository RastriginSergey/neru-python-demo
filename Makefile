.PHONY: vendor
vendor:
	pip3 install -r requirements.txt --target=./vendor

.PHONY: start
start:
	python3 main.py