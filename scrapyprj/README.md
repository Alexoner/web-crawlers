## europerail

Input and output are configured in "\$HOME/work/".
You need to provide pairs.txt file as input seeds.Each line of the file is in the format
'city1 city2'.

To run it,
```shell
./run.sh
```


## TODO

- [ ] keyword extraction from articles
    - [ ] TF-IDF
    - [ ] textrank
- [ ] visualization

## distributed deploying with frontera

```shell
# start the message broker
python -m frontera.contrib.messagebus.zeromq.broker > zeromq.log 2>&1 &
# start the db worker
python -m frontera.worker.db --config frontier.workersettings > db.log 2>&1 &
# start the strategy worker
# ...
# run spider workers parallely
# run spider worker that loads seeds
scrapy crawl general -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider0 -s SEEDS_SOURCE=seeds.txt
# run spider worker that only crawls
scrapy crawl general -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider1
scrapy crawl general -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider2
```
