# Telegram Stories Reader

This script allows you to automatically view stories of users in Telegram groups and channels where you have access.

## Features

- Iterates through all dialogs (chats and channels)
- Finds users with available stories
- Automatically marks stories as viewed
- Handles permission errors
- Logs the process

## Requirements

- Python 3.7 or newer
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/IvanZhutyaev/Masslooking.git
cd Masslooking
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your API ID and API HASH from [my.telegram.org](https://my.telegram.org/)

## Usage

1. Run the script:
```bash
python main.py
```

2. Enter your API ID and API HASH when prompted

3. On first run, you'll need to enter your phone number and verification code

## Configuration

The script works with default settings:
- Delay between viewing stories: 5 seconds
- Delay between checking dialogs: 5 seconds

## Limitations

- Admin privileges required to view participants in some chats
- Telegram may rate limit requests
- Some stories may not be marked as viewed due to API restrictions

## License

This project is licensed under the MIT License.
