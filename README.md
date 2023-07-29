# mac.bid
This is a tool to parse the site [Mac.Bid](http://mac.bid) and find deals without having to click through their web interface.

# Installation
There isn't any real installation necessary other than building the Docker container. That's done with the typical manner:
```
docker build -t macbid .
```

You can also run it on your host, but you will need to install the dependencies with:
```
pip3 install -r requirements.txt
```

# Usage
Their Greenville, SC location is what I'm interested in, so I have that set. Though you can change it to whatever you want in the `getSearchData()` call. The data is sorted by the auction that is closing first is at the top.

Generally, I run it out of a container like so:
```
docker run --rm -it -v $(pwd):/ws macbid -f bestDeal.txt -p 95
```
This will collect all the items that are more than 95% off from retail price. Another useful one is:
```
docker run --rm -it -v $(pwd):/ws macbid -f cheapStuff.txt -l 10
```
This searches for all the stuff that nobody is bidding on.

You can combine the two like this:
```
docker run --rm -it -v $(pwd):/ws macbid -f bestDeal.txt -p 95 -f cheapStuff.txt -l 10
```

# Donate
If you like useful apps like this, you can [![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoff.ee/bandi13)

