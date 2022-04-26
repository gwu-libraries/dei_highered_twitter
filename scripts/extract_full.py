import json
import csv

### Utility function

def extract_hashtags(entities_ht):
    ht_text = []
    for v in entities_ht:
        ht_text += [v['text']]
    print(' '.join(ht_text))
    return ' '.join(ht_text)

### Main code

json_path = 'tweets.json'
output_file_path = 'full_text.csv'

json_file = open(json_path, 'r', encoding='utf-8')

headers = ['id_str', 'source_full_text', 'source_hashtags']
output_file = open(output_file_path, 'w', encoding='utf-8')
output_writer = csv.DictWriter(output_file, fieldnames=headers, lineterminator='\n')
output_writer.writeheader()

for line in json_file:
    tweet = json.loads(line)
    tweet_out = {}
    tweet_out['id_str'] = tweet['id_str']

    if tweet.get('quoted_status') is not None:
        # then this is a retweeet
        qt = tweet.get('quoted_status')
        if qt.get('extended_tweet') is not None:
            tweet_out['source_full_text'] = qt['extended_tweet']['full_text'].replace('\n',' ')
            tweet_out['source_hashtags'] = extract_hashtags(qt['extended_tweet']['entities']['hashtags'])
        else:
            tweet_out['source_full_text'] = qt['text'].replace('\n',' ')
            tweet_out['source_hashtags'] = extract_hashtags(qt['entities']['hashtags'])

    elif tweet.get('retweeted_status') is not None:
        # then this is a retweeet
        rt = tweet.get('retweeted_status')
        if rt.get('extended_tweet') is not None:
            tweet_out['source_full_text'] = rt['extended_tweet']['full_text'].replace('\n',' ')
            tweet_out['source_hashtags'] = extract_hashtags(rt['extended_tweet']['entities']['hashtags'])
        else:
            tweet_out['source_full_text'] = rt['text'].replace('\n',' ')
            tweet_out['source_hashtags'] = extract_hashtags(rt['entities']['hashtags'])

    output_writer.writerow(tweet_out)
