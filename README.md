# Simple Human-like Telegram Bot

A lightweight, experimental Telegram bot built with Python (`pyTelegramBotAPI`) that realistically simulates human conversation patterns.

> **Note:** The conversational pattern engine and responses are specifically optimized for **Russian (RU)** natural dialogue.

---

## Key Features

- **Dynamic Typing & Reading Delays**  
  Calculates realistic pauses based on incoming message length (reading delay) and outgoing message length (typing delay at ~250–300 CPM).

- **Auto-Correction**  
  Randomly introduces typos based on adjacent keys on the JCUKEN keyboard layout, followed by a quick correction message (`*word` or `ой, word`).

- **Pattern Matching & Context Memory**  
  Utilizes regular expressions to match various topics (greetings, IT, gaming, movies, philosophy, mood) while keeping track of recent answers to prevent repetition.

- **Fault-Tolerant Polling**  
  Safely wraps Telegram API calls to prevent script crashes caused by users blocking the bot or deleting chats during delay intervals (`ApiTelegramException`).

---

## Quick Start

### 1. Requirements

- Python 3.8 or higher
- `pyTelegramBotAPI` library

### 2. Installation

Clone the repository and navigate to the project directory:

```bash
git clone [https://github.com/cookiegeek/simple-human-like-bot.git](https://github.com/cookiegeek/simple-human-like-bot.git)
cd simple-human-like-bot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Open `people.py` and replace the `TOKEN` variable with your Telegram Bot token from [@BotFather](https://t.me/BotFather):

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

### 5. Run

Start the bot:

```bash
python people.py
```

---

## Project Structure

```text
simple-human-like-bot/
├── people.py          # Main bot logic, typing simulation, and regex handlers
├── requirements.txt   # Required Python libraries
└── README.md          # Documentation
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).
