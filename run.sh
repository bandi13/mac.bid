docker build -t macbid .
docker run --rm -it -v $(pwd):/ws macbid -f bestDeal.txt -p 95 -f cheapStuff.txt -l 10
head -n 50 bestDeal.txt
echo "========="
head -n 50 cheapStuff.txt
