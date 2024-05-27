import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont
import functools
import CONSTANTS


def prepare_gif():
    images = []
    size = 64, 64
    profilePic = Image.open('yeet/user.png')
    profilePic.thumbnail(size, Image.LANCZOS)

    for i, (framePath, options) in enumerate(zip(CONSTANTS.yeetFrames, CONSTANTS.profilePicCoords)):
        frame = Image.open(framePath)
        profilePic.thumbnail(options['size'], Image.LANCZOS)
        frame.paste(profilePic, options["coords"])
        text = ImageDraw.Draw(frame)
        myFont = ImageFont.truetype('arial.ttf', 50)
        text.text((115, 140), "YEET", font=myFont)
        images.append(frame)
        profilePic.thumbnail(size, Image.LANCZOS)

    images[0].save('yeet/yeet.gif',
                   save_all=True, append_images=images[1:], optimize=False, duration=80, loop=0)


def sync_func():
    size = 128, 128

    authorIm = Image.open('../Goose-Bot/slap/author.png')
    authorIm.thumbnail(size, Image.LANCZOS)
    userIm = Image.open('../Goose-Bot/slap/user.png')
    userIm.thumbnail(size, Image.LANCZOS)
    batmanIm = Image.open('../Goose-Bot/slap/batman.jpg')

    batmanIm.paste(authorIm, (150, 25))
    batmanIm.paste(userIm, (300, 110))
    batmanIm.save("slap/slap.png")


class MemeCog(commands.Cog):
    def __init__(self, client):
        print("Registering Meme Cog")
        self.client = client

    @commands.command()
    async def yeet(self, ctx, user: discord.User):
        user_avatar = user.display_avatar
        await user_avatar.save("yeet/user.png")

        thing = functools.partial(prepare_gif)

        some_stuff = await self.client.loop.run_in_executor(None, thing)

        file = discord.File("yeet/yeet.gif")
        await ctx.send(file=file)

    @commands.command()
    async def slap(self, ctx, user: discord.User):
        author = ctx.author
        author_avatar = author.display_avatar
        user_avatar = user.display_avatar
        await author_avatar.save("slap/author.png")
        await user_avatar.save("slap/user.png")

        thing = functools.partial(sync_func)

        some_stuff = await self.client.loop.run_in_executor(None, thing)

        file = discord.File("../Goose-Bot/slap/slap.png")
        await ctx.send(file=file)


async def setup(client):
    await client.add_cog(MemeCog(client))
