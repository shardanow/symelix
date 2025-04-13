# AI Wellness Bot

AI Wellness Bot is a Telegram bot designed to help users track their emotions, health, and habits while providing personalized recommendations using GPT-based analysis. The bot integrates with various external APIs to gather data and offers a comprehensive summary of the user's day.

## Project Structure

```
├── main.py                      # Entry point, starts the bot
├── config.py                    # Configuration settings, tokens, paths, keys
├── requirements.txt             # Project dependencies
├── .env                         # Secrets: Telegram, OpenAI, Garmin
│
├── /bot/                        # Telegram bot interface
│   ├── handlers.py              # Commands, buttons, reactions
│   └── keyboards.py             # Custom keyboards, emojis, and buttons
│
├── /core/                       # Business logic
│   ├── mood.py                  # Emotion tracking
│   ├── health.py                # Health tracking
│   ├── habits.py                # Habit tracking
│   └── summary.py               # Daily data aggregation
│
├── /db/                         # Database operations
│   ├── models.py                # SQLAlchemy models
│   ├── crud.py                  # Queries: save, read, aggregate
│   └── database.py              # Database initialization and connection
│
├── /ai/                         # GPT analysis and recommendations
│   ├── analyzer.py              # Data collection + GPT queries
│   └── prompts.py               # Query examples, templates
│
├── /integrations/               # External APIs
│   ├── tracker.py               # Garmin data via python-garminconnect
│   ├── weather.py               # Weather and humidity (e.g., OpenMeteo)
│   └── geomagnetic.py           # Geomagnetic storms (e.g., NOAA or GeoStorms API)
│
└── /utils/                      # Utilities
    ├── helpers.py               # General helper functions
    └── time_utils.py            # Date handling, localization
```

## Features

- **Emotion Tracking**: Monitor and analyze your emotions.
- **Health Tracking**: Log and review your health metrics.
- **Habit Tracking**: Build and maintain healthy habits.
- **Daily Summary**: Get a comprehensive overview of your day.
- **GPT Recommendations**: Receive personalized advice based on your data.
- **API Integrations**: Seamlessly connect with Garmin, weather, and geomagnetic data sources.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd symelix
   ```

2. Configure the `.env` file with your secrets:
   ```env
   TELEGRAM_TOKEN=<your-telegram-token>
   OPENAI_API_KEY=<your-openai-api-key>
   GARMIN_API_KEY=<your-garmin-api-key>
   POSTGRES_USER=symelix
   POSTGRES_PASSWORD=root
   POSTGRES_DB=symelix
   ```

## Docker Setup

1. Build and start the services:
   ```bash
   docker-compose up --build
   ```

2. Access the database on port `5432`.

## Contributing

Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License.