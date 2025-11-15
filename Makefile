.PHONY: build

all:
	PYTHONPATH=/usr/lib/python3/dist-packages \
	uv run doit run all

test:
	PYTHONPATH=/usr/lib/python3/dist-packages \
	uv run pytest -sv

install:
	install build/EAW-CONSOLE.ttc ~/.fonts/truetype/eaw/
	fc-cache -f

lint:
	uv run ruff check dodo.py

clean:
	rm -rf build/*
