.PHONY: build run

build:
	docker build -t editor .

.DEFAULT_GOAL :=
run: build
	docker run --env-file=.env -p "5000:5000" editor