# Jobinja Resume Downloader

This repository provides a Python script to automate downloading resumes from Jobinja. The script uses user-provided configuration data and interacts with Jobinja's web interface to fetch the resumes.

---

## Features

- Extracts resumes from Jobinja job ads.
- Supports custom configurations for cookies, tokens, and user-agent.
- Downloads resumes in their original format (PDF or otherwise).

---

## Prerequisites

Before running the script, ensure you have the following installed:

- **Python 3.8 or later**: Download and install Python from the [official website](https://www.python.org/downloads/).
- **Required Python libraries**: Install using `pip`.

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/faridfr/jobinja-resume-downloader.git
cd jobinja-resume-downloader
```

### Step 2: Install Dependencies

Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### Step 3: Configure the Script

1. Copy the sample configuration file:
   ```bash
   cp config-sample.json config.json
   ```
2. Open `config.json` in a text editor and fill in the required fields:

| Key            | Description                                                                                          |
|-----------------|------------------------------------------------------------------------------------------------------|
| `COOKIE`       | Your browser cookie for Jobinja.                                                                    |
| `JSESSID`      | Your `JSESSID` token from Jobinja.                                                                  |
| `XSRF-TOKEN`   | Your `XSRF-TOKEN` token from Jobinja.                                                               |
| `company_name` | Your Jobinja company username.                                                                      |
| `job_ad_id`    | The Jobinja ad ID for which you want to download resumes.                                           |
| `user_agent`   | Your browser’s user-agent string (default provided, but replace with your own if necessary).        |
| `max_pages`    | (Optional) Maximum number of pages to scrape. Default is 20.                                        |
| `delay`        | (Optional) Delay between requests to avoid being blocked. Default is 2 seconds.                     |

**Example `config.json`:**

```json
{
    "COOKIE": "your-browser-cookie",
    "JSESSID": "your-jsessid",
    "XSRF-TOKEN": "your-xsrf-token",
    "company_name": "your-company-username",
    "job_ad_id": "your-job-ad-id",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "max_pages": 20,
    "delay": 2
}
```

### Step 4: Run the Script

Execute the script using Python:

```bash
python JobinjaResumeDownloader.py
```

The script will process resumes from the specified job ad and save them to the designated folder.

---

## Notes

1. Ensure you have appropriate permissions to access and download resumes.
2. The script respects Jobinja’s terms of service; use it responsibly.

---

## Troubleshooting

- **Invalid or expired tokens**: Refresh the tokens from your browser session.
- **Connection issues**: Check your internet connection and Jobinja’s accessibility.
- **Dependency issues**: Ensure all required packages are installed with `pip install -r requirements.txt`.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
