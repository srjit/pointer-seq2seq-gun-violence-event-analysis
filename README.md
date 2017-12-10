# Gun-violence-event-analysis


### Folders

  - Corpus: Collect news from google news via rss feed filter them by keywords and add to a postgres database


### Steps - Preprocessing

1. Postgres
	- Create database news in postgres
	- Run: Create Table gnews_search_results(scrapetime timestamp, rss_id varchar(20), queryinfo varchar(30),url varchar(100),keywords varchar(100),entry varchar(400));
	- Run: create table page_downloads(url text, downloadtime timestamp, status_code text, http_header text, page_content text, source text)
2. Data Collection
   	- Run gnews_scrape.py (collects google news results)
   	- Run corpus/consolidated_page_downloader.py  (collects htmls)
3. Text Extraction
   	- Use Lynx browser to extract text from the webpages collected
		   
