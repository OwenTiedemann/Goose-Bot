import time
from datetime import datetime

from discord.ext import commands, tasks
import feedparser

feed_urls = ['https://feeds.feedburner.com/ign/games-all', 'https://www.windowscentral.com/rss.xml', 'https://news.xbox.com/en-us/feed/']


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
                print('Posting: ' + post.link)
                await channel.send(post.link)


async def setup(client):
    await client.add_cog(FeedsCog(client))
