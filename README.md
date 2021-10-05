# San Antonio Express-News COVID-19 tracker

## Summary

This tool pulls data from the city of San Antonio's COVID-19 open data portal and formats it for use in graphics in the [San Antonio Express-News' COVID-19 dashboard](https://www.expressnews.com/coronavirus/article/coronavirus-tracking-san-antonio-texas-15301562.php).

## How to run 
1. Clone the repository.
2. Install the dependencies: `pip install -r requirements.txt`.
3. Run `python app.py`.

## Backstory
Our [COVID-19 dashboard](https://www.expressnews.com/coronavirus/article/coronavirus-tracking-san-antonio-texas-15301562.php) has been powered by this code since the start of the pandemic. Up until now, I've been running it on a [Linode](http://linode.com/) server that I spun up for $5 a month. Then a colleague tossed the idea of running it for free on GitHub using GitHub Actions ... something I did not know about. 

GitHub Actions are legit.