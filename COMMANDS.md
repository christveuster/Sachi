# Sachi Bot Commands

All commands are slash commands (use `/` to invoke them).

## Profile Command
**Usage:** `/profile [username]`
**Description:** Get a player's osu! profile information including rank, PP, accuracy, and play statistics.
**Example:** `/profile Peppy`

## Recent Command
**Usage:** `/recent [username]`
**Description:** View a player's 5 most recent plays with scores and PP values.
**Example:** `/recent Peppy`

## Top Command
**Usage:** `/top [username]`
**Description:** Display a player's top 5 plays sorted by performance points.
**Example:** `/top Peppy`

## Map Command
**Usage:** `/map [beatmap_id]`
**Description:** Fetch detailed information about a specific beatmap including difficulty rating, BPM, drain time, and map stats.
**Example:** `/map 221777`

## Droid Command
**Usage:** `/droid [username]`
**Description:** Get osu!droid specific statistics for a player, including droid rank and PP on the mobile version.
**Example:** `/droid ExGon`

## API References
- **osu! API v2 Documentation:** https://osu.ppy.sh/docs/index.html#introduction
- **osu!droid API Documentation:** https://gist.github.com/Rian8337/9f53d3a9c07804d648a17e7a4a0c36fa#file-droid-api-docs-md

## Setup
1. Copy `.env.example` to `.env`
2. Fill in your Discord bot token and osu! API credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot: `python main.py`
