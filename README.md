# Price Watcher

A Python bot that tracks a product's price and sends a Discord alert when the price drops.

Built as a learning project to practice web scraping, databases, and automation.

## How it works

1. **Scrape** — fetches the product page and extracts the current price using `requests` + `BeautifulSoup`
2. **Store** — saves the price to a local SQLite database
3. **Compare** — checks the new price against the last known price
4. **Notify** — if the price dropped, sends a message to a Discord channel via webhook
5. **Repeat** — runs automatically on a schedule (every hour) using the `schedule` library

## Tech stack

- Python 3
- `requests` — fetching web pages
- `beautifulsoup4` — parsing HTML
- `sqlite3` — local database (built into Python)
- `python-dotenv` — loading secrets from a `.env` file
- `schedule` — running the check on a timer
- Discord Webhooks — sending notifications

## Setup

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/price-watcher.git
   cd price-watcher
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your own Discord webhook URL:
   ```
   DISCORD_WEBHOOK_URL=your_webhook_url_here
   ```
   (In Discord: Server Settings → Integrations → Webhooks → New Webhook → Copy Webhook URL)

4. Run the bot
   ```bash
   python main.py
   ```

   The bot will check the price immediately, then continue running and check every hour. Press `Ctrl+C` to stop it.

## Project structure

```
price-watcher/
├── main.py         # scraping logic, price comparison, and scheduler
├── database.py     # SQLite functions (create table, add/update/read products)
├── notifier.py     # sends Discord webhook messages
├── .env            # your secret webhook URL (not committed to Git)
├── .gitignore
└── requirements.txt
```

## Notes

- Currently tracks a single product (URL is hardcoded in `main.py`)
- Built and tested against [webscraper.io](https://webscraper.io/test-sites)'s practice product pages

## Authors

- Your Name
- Your Friend's Name
