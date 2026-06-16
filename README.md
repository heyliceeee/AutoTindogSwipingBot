# 🐶 Tindog Automation  
Python + Selenium automation to log into Tindog, handle popups, and swipe dogs automatically with a resilient retry system.

---

## 🚀 Features

- **Automatic login** via Facebark  
- **Popup handling** (permissions, cookies, match)  
- **Automatic swiping** (20 likes per run)  
- **Retry system** for robust execution  
- **Persistent Chrome profile**  

---

## 📦 Requirements

- Python 3.10+
- Selenium
- python-dotenv
- Chrome + matching ChromeDriver

Install dependencies:

```bash
pip install selenium python-dotenv
```

---

## 🔧 Configuration

Create a `.env` file:

```
TINDOG_URL=https://tindog.example.com
TINDOG_EMAIL=your_email
TINDOG_PASSWORD=your_password
```

A persistent Chrome profile will be created automatically in `./chrome_profile`.

---

## 🧠 How It Works

### 1. WebDriver Initialization
- Loads environment variables  
- Creates a dedicated Chrome profile  
- Opens the Tindog website  

### 2. Automatic Login
`login_automatically()`:

- Clicks **Log in**
- Selects **Facebark**
- Switches to the authentication window
- Fills email and password
- Submits the form
- Returns to the main window
- Closes initial popups
- Waits for the homepage (`main.tindog-swipe-container`)

### 3. Liking Dogs
`like_dog()`:

- Attempts to click the **Like** button  
- If a match popup appears → closes it  
- If the button isn’t available → waits for it  
- Repeats the process 20 times  

### 4. Retry System
`retry(func)`:

- Executes the function  
- Retries on timeouts, missing elements, or blocked clicks  
- Raises an error after repeated failures  

---

## ▶️ Running the Script

```python
retry(login_automatically, description="Login")
retry(like_dog, description="Like a dog")
```

---

## 📁 Project Structure

```
.
├── chrome_profile/      # Persistent Chrome profile
├── .env                 # Credentials and URL
├── script.py            # Main automation script
└── README.md            # This file
```

---

## 📝 Notes

- The script avoids unnecessary delays by relying on Selenium’s explicit waits.  
- The retry system ensures stability against popups and temporary failures.  
- The persistent Chrome profile keeps sessions and cookies between runs.