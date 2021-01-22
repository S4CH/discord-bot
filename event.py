from utils import not_recognized
from services.user import get_user_email_and_id, submit_user_details
from services.content import fetch, mark_ques_status
from services.mmt import assign_mentors_to_all
from services.report import get_report_from_db, show_user_report, calc_days
import discord
import os
from dotenv import load_dotenv
import requests

load_dotenv()


def get_prompt_help():
    return discord.Embed(
        title='DN Bot Guide', description="Use these commands for smooth experience on the platform \n"
    ).set_thumbnail(
        url='https://cdn.wayscript.com/blog_img/83/DiscordBotThumb.png'
    )


async def on_user_message(message):
    if message.content.startswith('dn-assign-mentors'):
        await assign_mentors_to_all(message)

    if message.content.startswith('dn-hello'):
        msg = 'hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('dn-help'):
        msg = 'dn-help: To get command help \n dn-ask: To contact moderators \n dn-fetch: To get list of questions \n dn-done: To mark question done \n dn-undone: To mark question undone \n dn-doubt: To get mark question as doubt \n dn-report: To get progress report \n dn-leaderboard: To get list of top 10 students of week \n '

        prompt = get_prompt_help()
        prompt.add_field(
            name="Here is your ultimate guide to DN bot.\n",
            value=msg,
            inline=False)

        await message.channel.send(embed=prompt)

    if message.content.startswith('dn-email'):
        user_email = await get_user_email_and_id(message.author)
        if user_email:
            await submit_user_details(user_email, message.author)
            print('sending')

    if message.content.startswith('dn-fetch'):
        response = await fetch(message.author, message)
        if not response:
            await not_recognized(message.author, 'dn-fetch')

    if message.content.startswith('dn-done'):
        response = await mark_ques_status(message.author, message, 1)
        if not response:
            await not_recognized(message.author, 'dn-fetch')

    if message.content.startswith('dn-undone'):
        response = await mark_ques_status(message.author, message, 0)
        if not response:
            await not_recognized(message.author, 'dn-fetch')

    if message.content.startswith('dn-doubt'):
        response = await mark_ques_status(message.author, message, 2)
        if not response:
            await not_recognized(message.author, 'dn-fetch')

    if message.content.startswith('dn-report'):
        days = await calc_days(message)
        resp = await get_report_from_db(message, days)
        await show_user_report(resp, message, days)
