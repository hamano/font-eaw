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

clean:
	rm -rf build/*
