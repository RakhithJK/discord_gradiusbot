import asyncio
import discord
import logging
import traceback
from libs import banpool
from libs import banpool_configuration
from discord import Embed, Color, Permissions

banpool_manager = banpool.BanPoolManager()
banpool_config_manager = banpool_configuration.BanpoolConfigManager()

# Setup Logging
logger = logging.getLogger('banpool_manager')
logger.setLevel(logging.DEBUG)

logger.info("[Scheduled Task] <banpool_tasks.py>: Scheduled tasks for the banpool.")


@asyncio.coroutine
async def action(client, config):
    admin_server_id = config.getint('banpool', 'admin_server_id')
    admin_chan_name = config.get('banpool', 'admin_chan')
    task_length = config.getint('banpool', 'task_length')
    admin_chan = None

    setting_up = True
    while setting_up:
        logger.info("Waiting for client to log in...")
        if client.is_ready():
            # Setup Admin Messaging
            admin_server = discord.utils.get(client.guilds, id=admin_server_id)
            admin_chan = discord.utils.get(admin_server.channels, name=admin_chan_name)
            setting_up = False
        await asyncio.sleep(5)

    while True:
        try:
            if client.is_ready():
                # iterate through each guild, initialize warn/ban lists
                for guild in client.guilds:
                    notify_channel = banpool_config_manager.get_announce_chan(guild.id)
                    notify_list = []
                    ban_list = []
                    bot_perms = admin_chan.permissions_for(guild.me)

                    if not bot_perms.ban_members:
                        logger.error("The bot does not have ban permissions on {}[{}]".format(guild.name, guild.id))

                    else:
                        # identify which pool subs a guild has, pull banned members from each pool, add to warn/ban lists
                        # TODO : implement
                        # TODO: consider evaluating if the guild has a notify channel before creating a warn pool

                        # check to see if any ids in the server match these pools, and action
                        for banned_user_id in ban_list:
                            user = guild.get_member(banned_user_id)

                            if user and bot_perms.ban_members:
                                # ban the discord user
                                # TODO: implement
                                pass

                        for warn_user_id in notify_list and notify_channel:
                            user = guild.get_member(warn_user_id)

                            if user and bot_perms.ban_members:
                                # send warning message to configured guild channel
                                # TODO: implement
                                pass

            await asyncio.sleep(task_length)

        except RuntimeError:
            logger.error(traceback.format_exc())
            exit(0)

        except:
            logger.error(traceback.format_exc())
