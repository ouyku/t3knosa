# decisions

## image search API

**decision:** google custom search API + programmable search engine

**alternatives considered:**
- google lens — no public API
- google reverse image search — no public API, wrong direction
- cloud vision API — analyzes images, does not find them
- serpapi — only 100 free requests/month, too limited for development
- bing image search — good option but requires azure account with credit card

**why google custom search:**
- free 100 requests/day, no credit card
- official google API, reliable and structured JSON response
- web scraping was ruled out — fragile and against google's terms

**tradeoff:**
new programmable search engines can no longer search the entire web as of january 2026.
we are using a curated list of product-relevant domains instead.
this is acceptable and may actually produce better results for product images.
