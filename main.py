import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', 'YOUR_BOT_TOKEN_HERE')
OSU_API_KEY = os.getenv('OSU_API_KEY', 'YOUR_OSU_API_KEY_HERE')
OSU_CLIENT_ID = os.getenv('OSU_CLIENT_ID', 'YOUR_CLIENT_ID_HERE')
OSU_CLIENT_SECRET = os.getenv('OSU_CLIENT_SECRET', 'YOUR_CLIENT_SECRET_HERE')

# API endpoints
OSU_API_BASE = "https://osu.ppy.sh/api/v2"
OSU_DROID_API = "https://osudroid.moe/api"

class SachiBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.osu_token = None
        self.session = None

    async def get_osu_token(self):
        """Get OAuth2 token from osu! API"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.post(
                "https://osu.ppy.sh/oauth/token",
                json={
                    "client_id": OSU_CLIENT_ID,
                    "client_secret": OSU_CLIENT_SECRET,
                    "grant_type": "client_credentials",
                    "scope": "public"
                }
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.osu_token = data.get('access_token')
                    return self.osu_token
        except Exception as e:
            print(f"Error getting osu! token: {e}")
        return None

    async def osu_api_request(self, endpoint, params=None):
        """Make a request to osu! API v2"""
        if not self.osu_token:
            await self.get_osu_token()
        
        if not self.session:
            self.session = aiohttp.ClientSession()

        headers = {
            "Authorization": f"Bearer {self.osu_token}",
            "Accept": "application/json"
        }

        try:
            async with self.session.get(
                f"{OSU_API_BASE}{endpoint}",
                headers=headers,
                params=params
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 401:
                    # Token expired, refresh it
                    await self.get_osu_token()
                    headers["Authorization"] = f"Bearer {self.osu_token}"
                    async with self.session.get(
                        f"{OSU_API_BASE}{endpoint}",
                        headers=headers,
                        params=params
                    ) as retry_resp:
                        if retry_resp.status == 200:
                            return await retry_resp.json()
                return None
        except Exception as e:
            print(f"Error making osu! API request: {e}")
            return None

    @app_commands.command(name="profile", description="Get a player's osu! profile information")
    @app_commands.describe(username="The osu! username")
    async def profile(self, interaction: discord.Interaction, username: str):
        """Fetch osu! player profile"""
        await interaction.response.defer()
        
        try:
            user_data = await self.osu_api_request(f"/users/{username}")
            
            if not user_data:
                await interaction.followup.send(f"User '{username}' not found.")
                return

            embed = discord.Embed(
                title=f"osu! Profile: {user_data['username']}",
                color=discord.Color.blue(),
                url=f"https://osu.ppy.sh/users/{user_data['id']}"
            )
            embed.set_thumbnail(url=user_data.get('avatar_url', ''))
            embed.add_field(name="Country", value=user_data.get('country', {}).get('name', 'N/A'), inline=True)
            embed.add_field(name="Rank", value=f"#{user_data.get('statistics', {}).get('global_rank', 'N/A')}", inline=True)
            embed.add_field(name="PP", value=f"{user_data.get('statistics', {}).get('pp', 'N/A'):.2f}", inline=True)
            embed.add_field(name="Accuracy", value=f"{user_data.get('statistics', {}).get('hit_accuracy', 0):.2f}%", inline=True)
            embed.add_field(name="Play Count", value=user_data.get('statistics', {}).get('play_count', 'N/A'), inline=True)
            embed.add_field(name="Total Hours Played", value=user_data.get('statistics', {}).get('play_time', 0) // 3600, inline=True)
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Error fetching profile: {str(e)}")

    @app_commands.command(name="recent", description="View a player's recent plays")
    @app_commands.describe(username="The osu! username")
    async def recent(self, interaction: discord.Interaction, username: str):
        """Fetch recent plays"""
        await interaction.response.defer()
        
        try:
            user_data = await self.osu_api_request(f"/users/{username}")
            if not user_data:
                await interaction.followup.send(f"User '{username}' not found.")
                return

            recent_scores = await self.osu_api_request(f"/users/{user_data['id']}/scores/recent", {"limit": 5})
            
            if not recent_scores:
                await interaction.followup.send(f"No recent plays found for {username}.")
                return

            embed = discord.Embed(
                title=f"Recent Plays: {username}",
                color=discord.Color.green()
            )

            for idx, score in enumerate(recent_scores, 1):
                beatmap = score.get('beatmap', {})
                embed.add_field(
                    name=f"{idx}. {beatmap.get('beatmapset', {}).get('title', 'N/A')}",
                    value=f"Score: {score.get('score', 'N/A')} | PP: {score.get('pp', 0):.2f} | {score.get('rank', 'N/A')}",
                    inline=False
                )

            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Error fetching recent plays: {str(e)}")

    @app_commands.command(name="top", description="Display a player's top plays")
    @app_commands.describe(username="The osu! username")
    async def top(self, interaction: discord.Interaction, username: str):
        """Fetch top plays"""
        await interaction.response.defer()
        
        try:
            user_data = await self.osu_api_request(f"/users/{username}")
            if not user_data:
                await interaction.followup.send(f"User '{username}' not found.")
                return

            top_scores = await self.osu_api_request(f"/users/{user_data['id']}/scores/best", {"limit": 5})
            
            if not top_scores:
                await interaction.followup.send(f"No top plays found for {username}.")
                return

            embed = discord.Embed(
                title=f"Top Plays: {username}",
                color=discord.Color.gold()
            )

            for idx, score in enumerate(top_scores, 1):
                beatmap = score.get('beatmap', {})
                embed.add_field(
                    name=f"{idx}. {beatmap.get('beatmapset', {}).get('title', 'N/A')}",
                    value=f"Score: {score.get('score', 'N/A')} | PP: {score.get('pp', 0):.2f} | {score.get('rank', 'N/A')}",
                    inline=False
                )

            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Error fetching top plays: {str(e)}")

    @app_commands.command(name="map", description="Fetch details about a specific beatmap")
    @app_commands.describe(beatmap_id="The beatmap ID")
    async def map(self, interaction: discord.Interaction, beatmap_id: int):
        """Fetch beatmap information"""
        await interaction.response.defer()
        
        try:
            beatmap_data = await self.osu_api_request(f"/beatmaps/{beatmap_id}")
            
            if not beatmap_data:
                await interaction.followup.send(f"Beatmap '{beatmap_id}' not found.")
                return

            embed = discord.Embed(
                title=f"{beatmap_data.get('beatmapset', {}).get('title', 'N/A')}",
                description=f"Difficulty: {beatmap_data.get('version', 'N/A')}",
                color=discord.Color.purple(),
                url=f"https://osu.ppy.sh/beatmapsets/{beatmap_data.get('beatmapset_id')}"
            )
            embed.add_field(name="Artist", value=beatmap_data.get('beatmapset', {}).get('artist', 'N/A'), inline=True)
            embed.add_field(name="Creator", value=beatmap_data.get('beatmapset', {}).get('creator', 'N/A'), inline=True)
            embed.add_field(name="Star Difficulty", value=f"{beatmap_data.get('difficulty_rating', 0):.2f}⭐", inline=True)
            embed.add_field(name="Drain Length", value=f"{beatmap_data.get('drain_time', 0) // 60}m {beatmap_data.get('drain_time', 0) % 60}s", inline=True)
            embed.add_field(name="BPM", value=beatmap_data.get('bpm', 'N/A'), inline=True)
            embed.add_field(name="Max Combo", value=beatmap_data.get('max_combo', 'N/A'), inline=True)
            embed.add_field(name="AR", value=beatmap_data.get('ar', 'N/A'), inline=True)
            embed.add_field(name="OD", value=beatmap_data.get('accuracy', 'N/A'), inline=True)
            embed.add_field(name="CS", value=beatmap_data.get('cs', 'N/A'), inline=True)

            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Error fetching beatmap: {str(e)}")

    @app_commands.command(name="droid", description="Get osu!droid specific statistics for a player")
    @app_commands.describe(username="The osu!droid username")
    async def droid(self, interaction: discord.Interaction, username: str):
        """Fetch osu!droid player statistics"""
        await interaction.response.defer()
        
        try:
            # osu!droid uses a different API endpoint
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(
                f"https://osutracker.com/api/players/{username}"
            ) as resp:
                if resp.status == 200:
                    droid_data = await resp.json()
                    
                    embed = discord.Embed(
                        title=f"osu!droid Profile: {droid_data.get('username', username)}",
                        color=discord.Color.red()
                    )
                    embed.add_field(name="Rank", value=f"#{droid_data.get('rank', 'N/A')}", inline=True)
                    embed.add_field(name="PP", value=f"{droid_data.get('pp', 0):.2f}", inline=True)
                    embed.add_field(name="Accuracy", value=f"{droid_data.get('accuracy', 0):.2f}%", inline=True)
                    embed.add_field(name="Play Count", value=droid_data.get('playcount', 'N/A'), inline=True)
                    
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send(f"osu!droid user '{username}' not found.")
        except Exception as e:
            await interaction.followup.send(f"Error fetching osu!droid profile: {str(e)}")

async def setup(bot):
    await bot.add_cog(SachiBot(bot))

# Main bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.setup_hook
async def setup_hook():
    await setup(bot)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)


