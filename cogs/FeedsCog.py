import time
from datetime import datetime

from discord.ext import commands, tasks
import feedparser

feed_urls = ['https://feeds.feedburner.com/ign/games-all',
             'https://www.windowscentral.com/rss.xml',
             'https://news.xbox.com/en-us/feed/',
             'https://www.theverge.com/rss/games/index.xml',
             'https://www.inverse.com/rss']


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


class FeedsCog(commands.Cog):
    def __init__(self, client):
        print("Registering Feeds Cog")
        self.client = client
        self.post_feeds.start()

    @tasks.loop(hours=1)
    async def post_feeds(self):
        channel = await self.client.fetch_channel(self.client.NEWS_CHANNEL_ID)
        print('Posting feeds')
        for feed_url in feed_urls:
            print('Posting feed ' + feed_url)
            feed = feedparser.parse(feed_url)

            last_hour = [entry for entry in feed.entries if
                         ((time.time() - time.mktime(entry.published_parsed) - (4 * 3600)) < 3600) and (
                                     (time.time() - time.mktime(entry.published_parsed) - (4 * 3600) > 0))]
            for post in last_hour:
                if feed_url == 'https://www.theverge.com/rss/games/index.xml':
                    if post.author == 'Tom Warren':
                        print('Posting: ' + post.link)
                        await channel.send(post.link)
                    else:
                        print("The verge had a post not by tom warren: " + post.author)
                elif feed_url == 'https://www.inverse.com/rss':
                    if contains(post.tags, lambda x: x.term == 'Gaming'):
                        print('Posting: ' + post.link)
                        await channel.send(post.link)
                else:
                    print('Posting: ' + post.link)
                    await channel.send(post.link)


async def setup(client):
    await client.add_cog(FeedsCog(client))
