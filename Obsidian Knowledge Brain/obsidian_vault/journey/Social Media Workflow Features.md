# Content Scheduling & Publishing Workflow Overview

## 1. Content Scheduling & Publishing

- Schedule-based triggers (checks every 4 hours)  
- Google Sheets calendar management  
- Multi-platform posting:  
  - Twitter (API v2)  
  - Facebook Pages (Graph API)  
  - LinkedIn  
- Automatic status tracking  

## 2. Engagement Tracking

- Real-time metrics (checks every 2 hours):  
  - Likes/Reactions  
  - Comments  
  - Shares/Retweets  
- Platform-specific API calls  
- Automated data storage in Google Sheets  

## 3. Smart Notifications

- Slack alerts for:  
  - Successful posts  
  - High engagement (>10 interactions)  
- Email notifications via Gmail  
- Real-time team updates  

## 4. Manual Posting

- Webhook endpoint for on-demand posts  
- API-based manual triggers  
- Instant publishing  

---

## 📋 Setup Instructions

### Step 1: Google Sheets Setup  
Create a sheet with these columns:  
Row ID | Platform | Content | Media URL | Hashtags | Link  
Scheduled Date | Status | Post ID | Post URL | Posted At  
Likes | Comments | Shares | Total Engagement | Last Checked  

### Step 2: Get API Credentials  

- **Twitter API (Free Tier):**  
  - Go to [https://developer.twitter.com/en/portal/dashboard](https://developer.twitter.com/en/portal/dashboard)  
  - Create a new app  
  - Get API Key, API Secret, Access Token, Access Token Secret  
  - Enable OAuth 2.0  
  - Free tier: 1,500 tweets/month  

- **Facebook Graph API (Free Tier):**  
  - Go to [https://developers.facebook.com/](https://developers.facebook.com/)  
  - Create an app  
  - Add Facebook Login and Pages API  
  - Get Page Access Token from Graph API Explorer  
  - Token endpoint: [https://graph.facebook.com/v18.0/me/accounts](https://graph.facebook.com/v18.0/me/accounts)  
  - Free tier: Unlimited posts to your own pages  

- **LinkedIn API:**  
  - Go to [https://www.linkedin.com/developers/](https://www.linkedin.com/developers/)  
  - Create an app  
  - Request "Share on LinkedIn" permissions  
  - Get Client ID and Client Secret  
  - Free tier: Limited to your own profile/company page  

- **Slack API (Free Tier):**  
  - Go to [https://api.slack.com/apps](https://api.slack.com/apps)  
  - Create new app  
  - Add OAuth scope: chat:write  
  - Install to workspace  
  - Get Bot Token  
  - Free tier: 10,000 messages/month  

- **Gmail API (Free Tier):**  
  - Use Gmail OAuth in n8n  
  - Free tier: 500 emails/day  

### Step 3: Configure n8n Credentials  
In n8n, add these credentials:  
- Google Sheets OAuth2 (grant sheets read/write access)  
- Twitter OAuth2 API (add API Key and Secret, complete OAuth)  
- Gmail OAuth2 (standard setup)  
- Slack API (add Bot Token, select your channel)  

### Step 4: Update Placeholders  
Replace in the JSON:  
- YOUR_GOOGLE_SHEET_ID - Google Sheets URL ID  
- YOUR_PAGE_ID - Facebook Page ID  
- YOUR_FACEBOOK_PAGE_ACCESS_TOKEN - From Graph API Explorer  
- YOUR_TWITTER_CREDENTIAL_ID - n8n credential ID  
- YOUR_GOOGLE_SHEETS_CREDENTIAL_ID - n8n credential ID  
- YOUR_GMAIL_CREDENTIAL_ID - n8n credential ID  
- YOUR_SLACK_CREDENTIAL_ID - n8n credential ID  
- YOUR_SLACK_CHANNEL_ID - Slack channel ID  
- your-email@gmail.com - Your email  
- team@yourcompany.com - Team email  

### Step 5: Populate Content Calendar  
Add rows to your Google Sheet accordingly.
