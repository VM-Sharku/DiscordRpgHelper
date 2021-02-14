import random
import re
import sys
import time
from asyncio.tasks import sleep
from random import randint

import discord
from discord.ext import commands
from discord.ext.commands import errors

import effects
import enchantdb
from enchant import *
from item import Item


class RuleBook():
    def __init__(self):
        pass
    def dice(self, max=6):
        return random.randrange(0,max) + 1

dicePattern = re.compile("(^\d+)d(\d+)((\+|\-)(\d+)){0,1}$")

class RPGBot(commands.Bot):
    async def invoke(self, ctx):
        """|coro|
        Invokes the command given under the invocation context and
        handles all the internal event dispatch mechanisms.
        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context to invoke.
        """
        if ctx.command is not None:
            self.dispatch('command', ctx)
            try:
                if await self.can_run(ctx, call_once=True):
                    await ctx.command.invoke(ctx)
                else:
                    raise errors.CheckFailure('The global check once functions failed.')
            except errors.CommandError as exc:
                await ctx.command.dispatch_error(ctx, exc)
            else:
                self.dispatch('command_completion', ctx)
        elif ctx.invoked_with:
            result = dicePattern.match(ctx.invoked_with)
            if result != None:
                modifier_mult = int(result.groups()[0])
                modifier_dice = int(result.groups()[1])
                modifier_ops = None
                modifier_const = 0
                if result.groups()[2] != None:
                    modifier_ops = result.groups()[3]
                    modifier_const = int(result.groups()[4])
                await dice_internal(ctx, modifier_dice, mult=modifier_mult, ops=modifier_ops, constant=modifier_const)
            else:
                exc = errors.CommandNotFound('Command "{}" is not found'.format(ctx.invoked_with))
                self.dispatch('command_error', ctx, exc)
    

bot = RPGBot(command_prefix="!")

bot.EnchantItems = dict()
bot.EnchantDB = enchantdb.EnchantDB()
for item in bot.EnchantDB.getItems():
    bot.EnchantItems[item.Name] = item

@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)

@bot.command()
async def dice(ctx, max=6, count=1):
    print(ctx)
    await dice_internal(ctx, max, count)

@bot.command()
async def 다이스(ctx, max=6, count=1):
    await dice_internal(ctx, max, count)

@bot.command()
async def d4(ctx, count=1):
    await dice_internal(ctx, 4, count)

@bot.command()
async def d6(ctx, count=1):
    await dice_internal(ctx, 6, count)

@bot.command()
async def d8(ctx, count=1):
    await dice_internal(ctx, 8, count)

@bot.command()
async def d10(ctx, count=1):
    await dice_internal(ctx, 10, count)

@bot.command()
async def d20(ctx, count=1):
    await dice_internal(ctx, 20, count)

@bot.command()
async def d100(ctx, count=1):
    await dice_internal(ctx, 100, count)

@bot.command(name="다이스tts")
async def dice_tts(ctx, max=6, count=1):
    await dice_internal(ctx, max, count, tts=True)

async def dice_internal(ctx, max=6, count=1, mult=1, ops="", constant=0, use_tts=False):
    if count > 6:
        await ctx.send(f"너무 많이 굴리시네요! 스팸 방지. 5번만 굴려드릴게요.")
        count = 5
    for i in range(count):
        time.sleep(1)
        if ops == None or ops == "":
            pass
        elif ops == "+":
            constant = abs(constant)
        elif ops == "-":
            constant = constant * -1
        else:
            raise ValueError("Operator for dice should be + or -")
        result = mult * (random.randrange(0,max)+1) + constant
        await ctx.send(f"{ctx.author}님의 1d{max} 주사위 굴리기 결과 : {result}", tts=use_tts)

@dice.error
async def dice_error(ctx, error):
    print(ctx)
    print(error)

@bot.command()
async def join(ctx):
    voiceChannel = ctx.author.voice.channel
    if voiceChannel is not None:
        await voiceChannel.connect()

@bot.command()
async def effect(ctx, effectName):
    voiceClient = None
    for vc in bot.voice_clients:
        if vc.channel == ctx.author.voice.channel:  
            voiceClient = vc
    if voiceClient == None:
        voiceClient = await ctx.author.voice.channel.connect()
    if voiceClient.is_playing():
        voiceClient.stop()
    sourceFile = ""
    if effectName in effects.Files:
        sourceFile = f"sounds/{effects.Files[effectName]}"
    else:
        sourceFile = f"sounds/{effectName}"
    #if os.path.exists(sourceFile) != True:
    #    raise FileNotFoundError()
    audio = discord.FFmpegPCMAudio(executable="bin/ffmpeg.exe", source=sourceFile)
    voiceClient.play(audio)

@bot.command(name="강화")
async def enchant(ctx, itemname="당신의 미래"):
    uid = ctx.author.id
    item = bot.EnchantDB.getItem(itemname)
    if item == None:
        item = Item(itemname)
        bot.EnchantDB.addItem(item)
    rank = bot.EnchantDB.getRanking(itemname)
    prevHighestLevel = 0
    if rank != None:
        _, _, prevHighestLevel, _ = bot.EnchantDB.getRanking(itemname)
    else:
        bot.EnchantDB.addRanking(itemname, uid, 0, 0)
    enchantResult = enchant_internal(item.Level)
    item.IncreaseEnchantCount()
    # maple story enchant rule - fail-in-row sures 100% success in next trial
    resultMessage = "```\n"
    if item.ChanceTime == True:
        enchantResult = EnchantResult.SUCCESS
        resultMessage += "☆★되는게 없는 당신을 위한 선물★☆\n"
    # setup message
    newHighestLevel = prevHighestLevel
    resultMessage += f"+{item.Level}강 {item.Name} 의 강화에 {enchantResult}하였습니다.\n"
    if enchantResult == EnchantResult.SUCCESS:
        item.Enchant(1)
        resultMessage += f"+{item.Level}강 {item.Name} " + SuccessMessage[random.randrange(0,len(SuccessMessage))]
        if item.Level > prevHighestLevel:
            bot.EnchantDB.updateRanking(itemname, uid, item.Level, item.EnchantCount)
            newHighestLevel = item.Level
        item.ChanceTime = False
    elif enchantResult == EnchantResult.NORMAL:
        resultMessage += f"{item.Name} " + NormalMessage[random.randrange(0,len(NormalMessage))]
    elif enchantResult == EnchantResult.FAIL:
        if item.LastEnchantResult == EnchantResult.FAIL:
            item.ChanceTime = True
        item.Enchant(-1)
        resultMessage += f"{item.Name} " + FailMessage[random.randrange(0,len(FailMessage))]
    elif enchantResult == EnchantResult.BREAK:
        resultMessage += f"+{item.Level}강 {item.Name}" + BreakMessage[random.randrange(0,len(BreakMessage))]
        bot.EnchantDB.removeItem(itemname)
    item.LastEnchantResult = enchantResult
    if item.LastEnchantResult != EnchantResult.BREAK:
        bot.EnchantDB.updateItem(item)
    resultMessage += f"\n강화 횟수: {item.EnchantCount} | 최대 강화 레벨: {newHighestLevel}\n```"
    await ctx.send(resultMessage)

@bot.command(name="강화순위")
async def enchantrecord(ctx, count=10):
    ranks = bot.EnchantDB.getRankings(count)
    messages = []
    rankIndex = 1
    if ranks != None:
        for itemname,user_id,level,enchantcount in ranks:
            username = "None"
            user = await bot.fetch_user(user_id)
            if user != None:
                username = user.name
            messages.append(f'{rankIndex}등\t| {itemname} | +{level}강 | {username} | 강화 횟수: {enchantcount}회')
            rankIndex += 1
    rankMessage = "\n".join(messages)
    await ctx.send(f"```\nTOP {count} LIST\n{rankMessage}\n```" )

@bot.command()
async def vcs(ctx):
    print(bot.voice_clients)

if __name__ == "__main__":
    try:
        bot.run(str(sys.argv[1]))
    except IndexError as e:
        print('run 스크립트로 실행하지 않아서 token 정보를 불러오는데 실패했습니다. ' + e)
