import asyncio
import click
import discord
import mongoengine
from discord.ext import commands

from m0rkcoin_tip_bot import models, store
from m0rkcoin_tip_bot.config import config

bot_description = "Tip M0RKs to other users on your server."
bot_help_register = "Register yourself on the tip bot."
bot_help_withdraw = "Withdraw M0RKs from your balance."
bot_help_balance = "Check your M0RK balance."
bot_help_tip = "Give M0RKs to a user from your balance."

bot = commands.Bot(command_prefix='$')


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
async def register(context: commands.Context, wallet_address: str):
    user_id = context.message.author.id

    existing_user: models.User = models.User.objects(user_id=user_id).first()
    if existing_user:
        await bot.say(
            f'{context.message.author.mention}, you are already registered. '
            f'More details have been sent privately.')
        await bot.send_message(
            context.message.author,
            f'{context.message.author.mention}, you are already registered. '
            f'\nYour deposit address is '
            f'`{existing_user.balance_wallet_address}`.')
        return

    new_user = store.register_user(user_id, wallet_address)
    await bot.say(
        f'{context.message.author.mention}, you have been registered. More '
        f'details have been sent privately.')
    await bot.send_message(
        context.message.author,
        f'{context.message.author.mention}, you have been registered. '
        f'\nYou can send your deposits to '
        f'`{new_user.balance_wallet_address}` and your '
        f'balance will be available once confirmed.')


@bot.command(pass_context=True, help=bot_help_withdraw)
async def withdraw(context: commands.Context, amount: float):
    await bot.say('Not implemented.')


@bot.command(pass_context=True, help=bot_help_balance)
async def balance(context: commands.Context):
    user_id = context.message.author.id
    balance = store.get_wallet_balance(user_id)
    if not balance:
        await bot.send_message(context.message.author,
                               "You do not seem to have an available balance, "
                               "are you registered?")
        return

    await bot.send_message(
        context.message.author, '**Your balance**\n\n'
        f'Available: {balance["availableBalance"] / 1000000000000:.12f} M0RK\n'
        f'Pending: {balance["lockedAmount"] / 1000000000000:.12f} M0RK\n')


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


async def update_balance_wallets():
    while not bot.is_closed:
        store.update_balances()
        await asyncio.sleep(config.wallet_balance_update_interval)


@click.command()
def main():
    mongoengine.connect(db=config.database.db, host=config.database.host,
                        port=config.database.port,
                        username=config.database.user,
                        password=config.database.password)
    bot.loop.create_task(update_balance_wallets())
    bot.run(config.discord.token)


if __name__ == '__main__':
    main()
