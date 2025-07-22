# Telegram Registration Bot

This bot facilitates a multi-step user registration process, including channel subscription verification, data collection, field-specific questioning, and automated data export to CSV, GoogleSheet and Telegram.

## Setup and Installation

### 1. Prerequisites

-   Python 3.9+
-   Telegram Bot Token (from BotFather)

### 2. Environment Variables

Create a `.env` file in the project root directory with the following content:

```env
TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
```

### 3. Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 4. Configuration

Edit `config.py` to set up your specific parameters:

-   `CHANNEL_ID`: The Telegram channel ID for subscription checks and notifications.
-   `ADMIN_IDS`: A list of Telegram User IDs that will have access to admin commands.
-   `CSV_FILE`: The name of the CSV file where data will be saved (e.g., `registration_data.csv`).

If you want to configure your google credentials, go to google_credentials.json

### 5. Running the Bot

```bash
python main.py
```

### User Commands

-   `/start`: Initiates the registration process, language selection, and channel check.

### Admin Commands (for configured ADMIN_IDS only)

*Note: For field names with spaces (e.g., "Engineering"), please enclose them in double quotes.* 

-   `/admin_add_q `: 
    *Adds a new question for a specified field.*
-   `/admin_del_q <field> <index>`: Deletes a question. index is 1-based.
    *Example: /admin_del_q Economics 1*
-   `/admin_list_q <field>`: Lists all questions for a given field.

## Project Structure

```
.env
main.py
config.py
requirements.txt
questions.json
registration_data.csv

bot/
├── handlers/
│   ├── __init__.py
│   ├── admin.py
│   ├── registration.py
│   └── start.py
├── keyboards.py
├── localization.py
├── states/
│   ├── __init__.py
│   ├── admin.py
│   └── registration.py
└── utils.py
```
