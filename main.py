import discord
import settings
from discord.ext import commands
from discord.ext.commands import Bot
from requests.sessions import session
from requests_html import HTMLSession


session = HTMLSession()

client = discord.Client()
bot = commands.Bot(command_prefix="??")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='??sauce followed by an image url.'))
    print('Logged on as {0}!'.format(bot.user))

@bot.command()
async def sauce(ctx, arg):
    provided_image = arg
    req_obj = {'url': provided_image}
    url = "https://saucenao.com/search.php"
    req = session.post(url, req_obj)
    error_message = "Specified file does not seem to be an image..."
    supplied_image_error = "Supplied URL is not usable..."
    dimension_image_error = "image dimensions too small..."
    check_for_error = req.html.find("body", first=True).text
    if error_message == check_for_error:
        return await ctx.send("This isn't an image...")
    elif supplied_image_error == check_for_error:
        return await ctx.send("This isn't an image...")
    elif dimension_image_error == check_for_error:
        return await ctx.send("Image too small...")
    else:
        most_similar_image = req.html.find('#resImage0', first=True).attrs        
        most_similar_text = req.html.find('.resultcontentcolumn', first=True).absolute_links
        if most_similar_text is not None:
            await ctx.send("Most relevant Artist & Post:\n{}\n{}\n".format(list(most_similar_text)[1], list(most_similar_text)[0])) 
        else:
            await ctx.send("Something went wrong when getting the Artist.")
        if most_similar_image is not None:
            await ctx.send("Most Relevant Image:\n{}\n".format(most_similar_image.get('src')))
        else:
           return await ctx.send("Something went wrong when getting the supplied image.")    
bot.run(settings.TOKEN)