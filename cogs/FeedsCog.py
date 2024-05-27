import time

from discord.ext import commands, tasks
import feedparser

feed_urls = ['https://feeds.feedburner.com/ign/games-all']


class FeedsCog(commands.Cog):
    def __init__(self, client):
        print("Registering Feeds Cog")
        self.client = client
        self.post_feeds.start()

    @tasks.loop(hours=1)
    async def post_feeds(self):
        channel = await self.client.fetch_channel(1143292455433801739)
        print(channel)
        print('Posting feeds')
        for feed_url in feed_urls:
            print('Posting feed ' + feed_url)
            feed = feedparser.parse(feed_url)

            for item in feed.entries:
                print(time.mktime(time.localtime()) - time.mktime(item.published_parsed))

            last_hour = [entry for entry in feed.entries if
                         (time.mktime(time.localtime()) - time.mktime(entry.published_parsed) < 3600) and (
                                     time.mktime(time.localtime()) - time.mktime(entry.published_parsed) > 0)]
            for post in last_hour:
                print('Posting: ' + post.link)
                await channel.send(post.link)


async def setup(client):
    await client.add_cog(FeedsCog(client))
