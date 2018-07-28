import asyncio
import logging

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

help_string = """
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

            if len(split_content) == 3:
                # User is setting the announcement channel
                if split_content[1] == 'set-announce-chan':
                    announce_chan_str = split_content[2]

            if len(split_content) == 4:
                # User wants to set a banpool level: ignore, notify, ban
                if split_content[1] == 'set-pool-level':
                    pool_name = split_content[2]
                    level = split_content[3]

                    if level == 'ignore':
                        pass
                    elif level == 'notify':
                        pass
                    elif level == 'ban':
                        pass

