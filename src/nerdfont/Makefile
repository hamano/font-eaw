.PHONY: update

URL:=https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0
SRC:=NerdFontsSymbolsOnly.zip

update:
	@for f in $(SRC); do \
		curl -sw "%{http_code} $$f\n" -L --etag-save $$f.etag --etag-compare $$f.etag -o $$f ${URL}/$$f; \
	done
	if [ -f NerdFontsSymbolsOnly.zip ]; then \
		unzip -o NerdFontsSymbolsOnly.zip LICENSE SymbolsNerdFontMono-Regular.ttf; \
	fi

