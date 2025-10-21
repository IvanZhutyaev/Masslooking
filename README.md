# Telegram Stories Automation Bot

An advanced Python script for automated viewing and reacting to Telegram stories with multi-account support and detailed analytics.

## 🚀 Features

- **Multi-Account Support**: Run with 1 to 1000+ accounts simultaneously
- **Smart Story Processing**: Views stories and sends reactions based on story count
- **Advanced Statistics**: Real-time analytics with efficiency metrics
- **Proxy Support**: MTProto and SOCKS5 proxy configuration for each account
- **Session Management**: Automatic session persistence
- **Error Handling**: Robust error handling with graceful recovery
- **Detailed Logging**: Comprehensive logging with emoji indicators

## 📊 Smart Reaction System

- **2+ stories**: Views all stories, reacts to the second story
- **1 story**: Views and reacts to the single story
- **Random reactions**: ❤, 🔥, 👍 (randomly selected)
- **Configurable delays**: Random delays between 3-7 seconds to avoid detection

## 🛠 Requirements

- Python 3.7 or newer
- Dependencies listed in `requirements.txt`

## 📦 Installation

1. Clone or download the project:
```bash
git clone https://github.com/IvanZhutyaev/Masslooking.git
cd Masslooking
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create necessary directories:
```bash
mkdir sessions
```

## ⚙️ Configuration

### Single Account Mode
Run the script and enter credentials when prompted:
```bash
python main.py
```

### Multi-Account Mode
Create `accounts.txt` file:

```
# Format: api_id|api_hash|phone|proxy_json
123456|abcdef123456|+79991234567|
789012|ghijkl789012|+79997654321|{"server": "proxy.server.com", "port": 443, "secret": "eeeeeeeeeeeeeeeeeeee"}
```

### Proxy Configuration Examples

**MTProto Proxy:**
```json
{"server": "proxy.server.com", "port": 443, "secret": "eeeeeeeeeeeeeeeeeeee"}
```

**SOCKS5 Proxy:**
```json
{"proxy_type": "socks5", "addr": "127.0.0.1", "port": 1080, "username": "user", "password": "pass"}
```

## 🎯 Usage

### First Run Setup
1. The script will create session files in `sessions/` directory
2. Enter verification code for each account (first time only)
3. Sessions are automatically saved for future runs

### Normal Operation
```bash
python main.py
```
The script will:
- Rotate through all configured accounts
- Process stories in all accessible groups and channels
- Display real-time statistics
- Handle errors gracefully

## 📈 Statistics Tracking

- Total stories viewed
- Total reactions sent
- New subscribers gained
- Efficiency percentage
- Reactions by type
- Stories by dialog
- Session duration

## 🔧 Advanced Features

### Account Rotation
- Automatic switching between multiple accounts
- Configurable delays between cycles
- Session persistence

### Error Handling
- Chat admin permission errors
- Network timeouts
- Invalid proxy handling
- Rate limiting protection

### Real-time Monitoring
```
📊 [REAL-TIME] | ⏱️ 0:15:30 | 👀 45 | ❤️ 28 | 📈 +5
```

## ⚠️ Important Notes

- **Rate Limiting**: Random delays help avoid Telegram limits
- **Account Safety**: Use proxies for mass operations
- **Permissions**: Admin rights required for participant lists in some chats
- **Legal Compliance**: Use in accordance with Telegram ToS

## 🛡️ Security Recommendations

1. Use different phone numbers for multiple accounts
2. Implement proxies for IP rotation
3. Monitor account activity regularly
4. Start with small delays and gradually increase

## 📁 Project Structure

```
Masslooking/
├── main.py                 # Main script
├── accounts.txt           # Account configurations
├── requirements.txt       # Python dependencies
├── sessions/             # Session storage
│   ├── +123456789.session
│   └── +987654321.session
└── README.md            # This file
```

## 🐛 Troubleshooting

### Common Issues
- **"pip not recognized"**: Use `python -m pip install -r requirements.txt`
- **Session errors**: Delete session files and re-authenticate
- **Proxy errors**: Verify proxy configuration and connectivity

### Getting API Credentials
1. Visit [my.telegram.org](https://my.telegram.org/)
2. Go to "API Development Tools"
3. Create new application
4. Copy api_id and api_hash

## 📄 License

This project is licensed under the MIT License.

## 🔄 Updates

For updates and additional configurations, check the project repository or contact the maintainer.

---

**Disclaimer**: Use this tool responsibly and in compliance with Telegram's Terms of Service. The developers are not responsible for any account restrictions or bans.
