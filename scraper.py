import asyncio
import json
from typing import List
from urllib.parse import urlencode
import httpx
import sys
from datetime import datetime

params = {
    "x-algolia-agent": "Algolia for JavaScript (4.14.3); Browser (lite); autocomplete-core (1.7.4)",
    "x-algolia-api-key": "c3438d9345401783e3534bbb40d820be",
    "x-algolia-application-id": "1YFMY7AAMM",
}
search_url = "https://1yfmy7aamm-dsn.algolia.net/1/indexes/*/queries?" + urlencode(params)

def getSearchData(p=0):
    search_data = {
        'requests':[{'indexName':'prod_macdiscount','query':'','params':'hitsPerPage=96&facetFilters=[["auction_location:Greenville"],["is_open:1"]]','page':p}]
    }
    return search_data

async def scrape_search() -> List[dict]:
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as session:
        # scrape first page for total number of pages
        response_first_page = await session.post(search_url, json=getSearchData())
        data_first_page = response_first_page.json()["results"][0]
#        print(json.dumps(data_first_page, indent=1))

        results = data_first_page["hits"]
        total_pages = data_first_page["nbPages"]

        # scrape remaining pages concurrently
        other_pages = [ session.post(search_url, json=getSearchData(i)) for i in range(2, total_pages + 1) ]
        for response_page in asyncio.as_completed(other_pages):
            page_data = (await response_page).json()["results"][0]
            results.extend(page_data["hits"])
        return results

def printResult(r,file=sys.stdout):
    print (f'{r["product_name"].strip(): <{50}.{50}}\t${r["current_bid"]}\t${r["retail_price"]}\t  {r["discount_percentage"]}%',file=file, end="\r\n")

def getLessThanDollar(results,dollar,file=sys.stdout):
    print (f'Less than ${dollar}',file=file,end="\r\n")
    bestItems={}
    for r in results:
        if r["current_bid"] <= dollar:
            bestItems[100 * int(r["expected_closing_utc"] / 100) - r["retail_price"] / 1000000] = r

    for r in sorted(bestItems.keys(),reverse=False):
        printResult(bestItems[r],file)

def getMoreThanPercent(results,percent,file=sys.stdout):
    bestItems={}
    print (f'Less than {percent}%',file=file,end="\r\n")
    for r in results:
        if r["discount_percentage"] >= percent:
            bestItems[100 * int(r["expected_closing_utc"] / 100) - r["retail_price"] / 100000] = r

    for r in sorted(bestItems.keys(),reverse=False):
        printResult(bestItems[r],file)

if __name__ == "__main__":
    results = asyncio.run(scrape_search())

    f = sys.stdout
    i = 0
    while i < len(sys.argv):
        arg = sys.argv[i]
        i += 1
        if arg == "-l":
            getLessThanDollar(results,int(sys.argv[i]),f)
            i += 1
        elif arg == "-p":
            getMoreThanPercent(results,int(sys.argv[i]),f)
            i += 1
        elif arg == "-f":
            f = open(sys.argv[i],'w')
            i += 1

#with open('zeroDollars.txt', 'w') as f:
#    getZeroDollar(results,f)
#getLessThanDollar(results,0)

#with open('fivePercentDiscount.txt', 'w') as f:
#    getMoreThanPercent(results,95,f)
#getMoreThanPercent(results,95)
