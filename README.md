# Sachi

A Discord bot designed to fetch and display osu! and osu!droid data, including player statistics, recent plays, beatmap information, and more.

## Features

- **osu! Data Fetching**: Retrieve player profiles, recent plays, top plays, and beatmap details from the osu! API.
- **osu!droid Support**: Compatible with osu!droid plays, allowing users to view and compare scores from the mobile version.
- **Easy Integration**: Seamlessly integrates into Discord servers for quick access to osu! statistics.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sachi.git
   cd sachi
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add your Discord bot token: `DISCORD_TOKEN=your_bot_token_here`
   - Add your osu! API key: `OSU_API_KEY=your_osu_api_key_here`

4. Run the bot:
   ```
   npm start
   ```

## Usage

Invite the bot to your Discord server and use the following commands:

- `/profile [username]`: Get a player's osu! profile information.
- `/recent [username]`: View a player's recent plays.
- `/top [username]`: Display a player's top plays.
- `/map [beatmap_id]`: Fetch details about a specific beatmap.
- `/droid [username]`: Get osu!droid specific statistics for a player.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
