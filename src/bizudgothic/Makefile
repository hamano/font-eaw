.PHONY: update

URL:=https://raw.githubusercontent.com/google/fonts/main/ofl/bizudgothic
SRC:=OFL.txt BIZUDGothic-Regular.ttf BIZUDGothic-Bold.ttf

update:
	@for f in $(SRC); do \
		curl -sw "%{http_code} $$f\n" --etag-save $$f.etag --etag-compare $$f.etag -o $$f ${URL}/$$f; \
	done

