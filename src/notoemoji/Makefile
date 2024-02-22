.PHONY: update

URL:=https://raw.githubusercontent.com/google/fonts/main/ofl/notoemoji
SRC:=NotoEmoji%5Bwght%5D.ttf OFL.txt

update:
	@for f in $(SRC); do \
		curl -sw "%{http_code} $$f\n" --etag-save $$f.etag --etag-compare $$f.etag -o $$f ${URL}/$$f; \
	done

