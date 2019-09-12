from discord.ext import commands
from discord.ext import tasks
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import aiohttp
import discord


class Contest:
    def __init__(self, **data):
        self.title = data.pop("title")
        self.time = data.pop("time")
        self.url = "https://atcoder.jp" + data.pop("url")
        self.duration = data.pop("duration")
        self.rating = data.pop("rating")
        self.loop = None

    def to_embed(self):
        embed = discord.Embed(title=self.title)
        embed.add_field(name="コンテストページ", value=self.url)
        embed.add_field(name="開始時刻", value=self.time)
        embed.add_field(name="コンテスト時間", value=self.duration)
        embed.add_field(name="レーティング変化", value=self.rating)

        return embed

    def __str__(self):
        return "<Contest title={0.title}, time={0.time}, url={0.url}, duration={0.duration}, rating={0.rating}>".format(
            self
        )


class AtCoder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.contests = {}

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    @tasks.loop(hours=24)
    async def get_contests(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, "https://atcoder.jp/contests/?lang=ja")

        soup = BeautifulSoup(html, "html.parser")
        mainbody = soup.find("div", id="contest-table-upcoming")
        contests_table = mainbody.find("tbody")
        contests = contests_table.find_all("tr")

        for contest_info in contests:
            contest = self._create_contest(contest_info)

            if contest.title not in self.contests:
                self.contests[contest.title] = contest
                contest.loop = self._create_loop(contest)
                contest.loop.start()

    def cog_unload(self):
        self.get_contests.cancel()

        for contest in self.contests.items():
            contest.loop.cancel()

    def _create_contest(contest):
        tds = contest.find_all("td")
        time = tds[0].find("time").text.split("+")[0]
        title = tds[1].find("a").text
        url = tds[1].find("a")["href"]
        duration = tds[2].text
        rating = tds[3].text

        return Contest(
            title=title, time=time, url=url, duration=duration, rating=rating
        )

    def _create_loop(self, contest):
        time = datetime.strptime(contest.time, "%Y-%m-%d %H:%M:%S") - timedelta(
            minutes=30
        )

        @tasks.loop(count=1, time=time)
        async def loop():
            user = self.bot.get_user(195816057926057994)
            await user.send(embed=contest.to_embed())

        @loop.after_loop
        async def after():
            del self.contests[contest.title]

        return loop


def setup(bot):
    bot.add_cog(AtCoder(bot))
