import discord
from discord.ext import commands
from shodan import Shodan
import shodan
from utils import BaseClass
import os
import re

class ShodanAPICommands(BaseClass):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    def check_valid_ip(self, ip: str) -> bool:
        """
        Validates whether the provided string is a valid IPv4 address.

        :param ip: The IP address to validate as a string.
        :return: True if the IP address is valid, False otherwise.
        """
        # valid IPv4 address
        ipv4_pattern = re.compile(r"""
            ^
            (25[0-5]|              # Matches 250-255
            2[0-4][0-9]|           # Matches 200-249
            1[0-9][0-9]|           # Matches 100-199
            [1-9]?[0-9])           # Matches 0-99
            (\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}  # Match the next 3 octets
            $
        """, re.VERBOSE)
        
    
        return bool(ipv4_pattern.match(ip))

    def initalize_shodan(self):
        api_key = os.getenv("SHODAN_API_KEY", "")
        return Shodan(api_key)

    @commands.command(help="Searches IPv4 using Shodan API and gets info. Usage: $searchip (ip)")
    async def searchip(self, ctx, ip: str):
        #check if valid ipv4
        if self.check_valid_ip(ip):
            try:
                api = self.initalize_shodan()
                ipinfo = api.host(ip)
                ports = ipinfo.get("ports", "n/a")
                fields = [
                    {"name": "IP(str)", "value": ipinfo["ip_str"], "inline": True},
                    {"name": "Organization", "value": ipinfo.get("org", "n/a"), "inline": True},
                    {"name": "ISP", "value": ipinfo.get("isp", "n/a"), "inline": True},
                    {"name": "Ports", "value": ports, "inline": True},
                    {"name": "Domains", "value": ipinfo.get("domains", "n/a"), "inline": True},
                    {"name": "Country", "value": ipinfo.get("country_name", "n/a"), "inline": True},
                ]
                if 443 in ports:
                    fields.append({"name": "Website(Port)", "value": f"https://{ipinfo['ip_str']}/", "inline": True})
                elif 80 in ports:
                    fields.append({"name": "Website(Port)", "value": f"http://{ipinfo['ip_str']}/", "inline": True})
                await self.send_embed(
                    ctx,
                    title=f"Information Regarding IP: {ip}",
                    description="",
                    fields=fields
                )

            except shodan.APIError:
                await self.send_embed(
                    ctx,
                    title="SHODAN API ERROR",
                    description="Failed to retrieve IP information.",
                    colour=discord.Colour.red()
                )

        else:
            await self.send_embed(
                ctx,
                title="Invalid IP -> Use IPv4 ONLY!",
                description="Invalid argument, please try again with a valid IPv4 address.",
                colour=discord.Colour.red(),
            )

async def setup(bot):
    await BaseClass.setup(bot, ShodanAPICommands)
