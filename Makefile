.PHONY: build

all:
	poetry run doit run all

test:
	poetry run pytest -sv

install:
	install build/EAW-CONSOLE.ttc ~/.fonts/truetype/eaw/
	fc-cache -f

clean:
	rm -rf build/*
