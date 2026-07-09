
# Automated Job Discovery Workflow Overview

## 1. Automated Job Discovery

- Scrapes Reddit's r/forhire and r/freelance_forhire every 6 hours  
- Uses free Reddit JSON API (no authentication needed)  
- Easily expandable to other free sources  

## 2. Intelligent Filtering

- Scores opportunities based on skill matches (customize to your expertise)  
- Filters out spam and irrelevant posts  
- Prioritizes posts with budget indicators  

## 3. Automated Tracking

- Stores all opportunities in Google Sheets  
- Tracks relevance scores, matched skills, and status  
- Maintains complete history for analysis  

## 4. Real-Time Notifications

- Slack alerts for high-priority opportunities (score ≥30)  
- Instant visibility into the best matches  
- Enables quick response times  

## 5. Personalized Pitch Generation

- Auto-creates tailored proposals based on job details  
- Ready-to-send messages that reference specific skills  
- Professional template you can customize  

## 6. Follow-up Automation

- Checks for unresponded leads every 3 days  
- Sends Slack reminders to follow up  
- Helps maintain persistence without being pushy  

---

# Setup Steps

- Import the JSON workflow into n8n  
- Create Google Sheet with the specified columns  
- Connect credentials (Google OAuth2, Slack API)  
- Customize skills array to match your expertise  
- Update pitch templates with your info and portfolio  
- Activate the workflow and start generating opportunities!  

---

# Pro Tips

- Respond fast: High scores = hot opportunities  
- Track conversions: Update status column (New → Sent → Won/Lost)  
- Refine skills: Adjust keywords based on what converts  
- Expand sources: Add more free job boards to the scraping nodes  
- Stay compliant: Respect rate limits and terms of service  
- This workflow is completely free to run and can generate real income by automating the tedious parts of freelance hunting while keeping you in control of the actual outreach!
