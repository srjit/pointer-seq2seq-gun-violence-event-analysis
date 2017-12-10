# Gun-violence-event-analysis


###Folders

  - Corpus: Collect news from google news via rss feed filter them by keywords and add to a postgres database


###Steps

1. Postgres
	a. Create database news in postgres
	b. Run: Create Table gnews_search_results(scrapetime timestamp, rss_id varchar(20), queryinfo varchar(30),url varchar(100),keywords varchar(100),entry varchar(400));
	c. Run: create table page_downloads(url text, downloadtime timestamp, status_code text, http_header text, page_content text, source text)
2. Data Collection
   	a. Run gnews_scrape.py (collects google news results)
   	b. Run corpus/consolidated_page_downloader.py  (collects htmls)
3. Text Extraction
   	a. Use Lynx browser to extract text from the webpages collected
		   
