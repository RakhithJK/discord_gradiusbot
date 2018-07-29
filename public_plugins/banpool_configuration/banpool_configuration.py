import asyncio
import logging
from libs.banpool_configuration import BanpoolConfigManager

# Setup Logging
logger = logging.getLogger('banpool_configuration')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('banpool_configuration.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

logger.info("[Public Plugin] <banpool_configuration.py>: This plugin configures the banpool.")

bcm = BanpoolConfigManager()

help_string = """
Test help string.
"""


@asyncio.coroutine
async def action(**kwargs):
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    # Check to see if the message author is an administrator in the server
    if message.author.guild_permissions.administrator:
        split_content = message.content.split()

        if len(split_content) > 0 and split_content[0] == '!bpc':
            if len(split_content) == 2:
                if split_content[1] == 'help':
                    await message.channel.send(help_string)

                # User is setting the announcement channel
                if split_content[1] == 'set-announce-chan':
                    success = bcm.set_announce_chan(message.guild.id, message.channel.id,
                                                    message.author.name + message.author.discriminator, message.author.id)

                    if success:
                        await message.channel.send('Successfully set announcement channel.')

                    else:
                        await message.channel.send('Was unable to set announcement channel.')

                if split_content[1] == 'send-test-message':
                    announce_chan_id = bcm.get_announce_chan(message.guild.id)
                    target_channel = message.guild.get_channel(announce_chan_id)

                    if target_channel:
                        await target_channel.send('This is a test announcement message to the configured channel.')
                    else:
                        await message.channel.send('An announcement channel has not been set. Please set one with the `!bpc set-announce-chan` command in the desired channel.')

            if len(split_content) == 4:
                # User wants to set a banpool level: ignore, notify, ban
                if split_content[1] == 'set-pool-level':
                    pool_name = split_content[2]
                    level = split_content[3]

                    if level in ['ignore', 'notify', 'ban']:
                        bcm.set_pool_level(message.guild.id, pool_name, level,
                                           message.author.name+message.author.discriminator, message.author.id)
                    else:
                        await message.channel.send('Unable to set pool level, please select between "ignore, notify, or ban"')

