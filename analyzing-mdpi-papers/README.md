# Analyzing 922,544 papers published by MDPI so you don't have to

Many (most?) academics will know the academic published "Multidisciplinary Digital Publishing Institute" - MDPI - that published many, many open access journals.

MDPI journals are (in)famous for their suspiciously quick review times (sometimes less than a week, whereas more conventional journals can take months) and allegations of scientific and editorial misconduct. MDPI has been alleged to emphasize speed (and profits) over quality, but MDPI journals have seen tremendous growth irrespective of their questionable reputation.

I wanted to analyze MDPI journals and papers in greater detail than was done before. For example, how quick is the editorial process actually, from start to finish? Do we see any differences across journals? How many papers are actually published? Can we get an idea of what kinds of papers each journal publishes (i.e., are they similar in topics or do some journals just publish anything)?

To do that, I retreived most* papers published in MDPI journals (922,544 to be exact) and analyzed the speed of the review and publication process and tried to visualize the abstracts of each journal.

# How did I do that and what is in this repo?

## Data retreival

First, I got a record of most of MDPI's published papers. Thankfully, MDPI does partake in the "Open Archives Initiative Protocol for Metadata Harvesting" (OAI), which made this task pretty easy, albeit time consuming. 
Via OAI, I was able to get all MDPI papers published after January 12, 2012. Papers before that date are not included in the analysis and I found it honestly too tedious to try to track them down. Retreiving all these papers already too more than two hours(!) as OAI retreival is really slow when there are this many papers...
I did this step in R, the script can be found in `scripts/get_papers.R`, and the results are contained in `data/papers.csv`.

Second, I needed to obtain the publication history of each article (which, sadly, can't be retreived via OAI. `data/papers.csv` contains the link to each paper, which I used to scrape the publication history from the respective websites using `selenium` and `BeautifulSoup` from `bs4` in Python. 
The code for this step is contained in `scripts/get_pub_hist.py` and the results are contained in `data/pubhistory.csv`.

Third, I merged `data/papers.csv` and `data/pubhistory.csv` using `pd.merge` in Python. The result is stored in `data/complete_results.py`. 

## Analyzing publication speed

I analyzed the speed of peer review and publication by journal. 

