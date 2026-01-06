.PHONY: build

all:
	uv run doit run all

test:
	uv run pytest -sv

install:
	install build/EAW-CONSOLE.ttc ~/.fonts/truetype/eaw/
	fc-cache -f

lint:
	uv run ruff check dodo.py

clean:
	rm -rf build/*
