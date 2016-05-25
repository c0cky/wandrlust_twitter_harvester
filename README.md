# Wandrlust Twitter Harvester

* clone the repo
* create a new venv: `virtual venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `python main.py`

add your credentials into `keys.txt` file in the format of

* 1: consumer_key
* 2: consumer_secret
* 3: access_token_key
* 4: access_token_secret


To run this you run:
`python main.py --command <command> --query <query> --file <file_file>`

if not specified the output file will be `statuses.json`

# Available commands:
* `harvest` - the `<query>` parameter is required here. This command gets all tweets that match your query and likes them and saves.
* `followup` - This compares all the tweets you have harvested to your followers (if someone followed you from harvesting)
* `followers` - Un follows all people that dont follow you
* `create` - Follows all people associated with a query
* `user` - Gets all the tweets from a user. Works around the 3200 limit.


# Streamer

You can run `python stream.py --query <query>` to get tweets to print out from the twitter stream. 
This is usually piped to a file.
