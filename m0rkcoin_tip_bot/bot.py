import os

import click
import discord
import yaml
from discord.ext import commands
from munch import Munch

config_file_path = os.path.join(
    os.path.dirname(__file__), os.path.pardir, 'config.yml')

bot_description = "Tip M0RKs to other users on your server."
bot_help_register = "Register yourself on the tip bot."
bot_help_withdraw = "Withdraw M0RKs from your balance."
bot_help_balance = "Check your M0RK balance."
bot_help_tip = "Give M0RKs to a user from your balance."

config = {}
bot = commands.Bot(command_prefix='$')


def load_config():
    with open(config_file_path) as config_file:
        _config = yaml.load(config_file)
        globals()['config'] = Munch.fromDict(_config)


@bot.event
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)


@bot.command(pass_context=True)
async def echo(context: commands.Context, content: str):
    await bot.say(content)
    await bot.send_message(context.message.author, content)


@bot.command(pass_context=True, help=bot_help_register)
async def register(context: commands.Context, wallet_id: str):
    await bot.say('Not implemented.')


@bot.command(pass_context=True, help=bot_help_withdraw)
async def withdraw(context: commands.Context, amount: float):
    await bot.say('Not implemented.')


@bot.command(pass_context=True, help=bot_help_balance)
async def balance(context: commands.Context):
    await bot.say('Not implemented.')


@bot.command(pass_context=True, help=bot_help_tip)
async def tip(context: commands.Context, member: discord.Member,
              amount: float):
    await bot.say('Not implemented.')


@tip.error
async def tip_error(error, context: commands.Context):
    if isinstance(error, commands.BadArgument):
        await bot.say(f'Invalid arguments provided. {error.args[0]}')
    else:
        await bot.say('Unexpected error.')


@click.command()
def main():
    global config
    load_config()
    bot.run(config.discord.token)


if __name__ == '__main__':
    main()
