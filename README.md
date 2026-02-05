# NFL Playoff Fantasy Tracker 🏈

A modern, auto-updating fantasy football tracker for NFL playoff games. Features real-time score updates via ESPN API with a sleek sports broadcast-inspired design.

![Preview](https://via.placeholder.com/1200x600/0A0E27/FF6B35?text=NFL+Playoff+Fantasy+Tracker)

## Features

✅ **Real-time ESPN API Integration** - Automatically fetches live game stats  
✅ **Head-to-Head Matchups** - Track fantasy scores between two teams  
✅ **Detailed Player Stats** - QB passing, RB rushing, WR receiving, K field goals, D/ST performance  
✅ **Top Performers Dashboard** - Highlights the weekend's best players  
✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile  
✅ **Auto-updating** - Configure GitHub Actions to update scores automatically  

---

## Quick Start

### 1. Clone This Repository

```bash
git clone https://github.com/YOUR-USERNAME/nfl-playoff-tracker.git
cd nfl-playoff-tracker
```

### 2. Install Dependencies

```bash
pip install requests --break-system-packages
```

### 3. Configure Your Teams

Edit `championship_matchup.py` and update your team rosters:

```python
self.team1 = {
    'name': 'YOUR TEAM NAME',
    'roster': [
        ('Player Name', 'Position', 'TEAM'),
        ('Tom Brady', 'QB', 'TB'),
        ('Derrick Henry', 'RB', 'TEN'),
        # ... add all your players
    ]
}
```

### 4. Generate Data

```bash
python generate_website_data.py
```

This creates `championship_results.json` that powers the website.

### 5. View Website Locally

```bash
# Python 3
python -m http.server 8000

# Then open: http://localhost:8000
```

---

## File Structure

```
nfl-playoff-tracker/
├── index.html                    # Main website
├── styles.css                    # Styling
├── script.js                     # Frontend logic
├── championship_matchup.py       # ESPN API integration
├── generate_website_data.py      # Data generator script
├── championship_results.json     # Generated data (auto-created)
└── README.md
```

---

## Deployment to GitHub Pages

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository → **Settings** → **Pages**
2. Under "Source", select: **Deploy from a branch**
3. Select branch: **main** and folder: **/ (root)**
4. Click **Save**
5. Your site will be live at: `https://YOUR-USERNAME.github.io/nfl-playoff-tracker/`

### Step 3: Set Up Auto-Updates (GitHub Actions)

Create `.github/workflows/update-data.yml`:

```yaml
name: Update Fantasy Data

on:
  schedule:
    # Run every 15 minutes during game days
    - cron: '*/15 * * * *'
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install requests
      
      - name: Generate website data
        run: |
          python generate_website_data.py
      
      - name: Commit and push if changed
        run: |
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          git add championship_results.json
          git diff --quiet && git diff --staged --quiet || (git commit -m "Update fantasy data" && git push)
```

This automatically updates your data every 15 minutes during games!

---

## Custom Domain Setup

### Step 1: Buy a Domain

Purchase a domain from:
- Namecheap
- Google Domains
- Cloudflare

### Step 2: Configure DNS

Add these records to your domain's DNS settings:

```
Type    Name    Value
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
CNAME   www     YOUR-USERNAME.github.io
```

### Step 3: Configure GitHub

1. Go to repository → **Settings** → **Pages**
2. Under "Custom domain", enter: `yourdomain.com`
3. Check "Enforce HTTPS"
4. Wait 10-15 minutes for DNS propagation

---

## Customization

### Change Colors

Edit `styles.css`:

```css
:root {
    --color-primary: #FF6B35;     /* Main accent color */
    --color-secondary: #00D9FF;   /* Secondary accent */
    --color-bg-dark: #0A0E27;     /* Background */
}
```

### Update Scoring Rules

Edit `championship_matchup.py`:

```python
self.scoring = {
    'passing_yards_per_point': 25,  # 1 pt per 25 yards
    'passing_td': 8,                 # 8 pts per TD
    'rushing_yards_per_point': 10,  # 1 pt per 10 yards
    # ... customize your scoring
}
```

### Add More Weeks

The script works for any playoff weekend! Just update:

```python
# In championship_matchup.py
def fetch_playoff_games(self):
    url = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    params = {
        'seasontype': 3,  # Playoffs
        'week': 4,        # Conference Championships (change to 3 for Divisional, 5 for Super Bowl)
        'year': 2026
    }
```

---

## Troubleshooting

### "Data Not Available" Error

**Problem:** Website shows error message  
**Solution:** Run `python generate_website_data.py` to create the JSON file

### Scores Not Updating

**Problem:** GitHub Actions not running  
**Solution:**
1. Check `.github/workflows/update-data.yml` exists
2. Go to **Actions** tab → Enable workflows
3. Click **Run workflow** to test manually

### Players Not Found

**Problem:** Script can't find your players  
**Solution:** Check player name spelling matches ESPN exactly:
- ✅ "Patrick Mahomes" 
- ❌ "Pat Mahomes"

### CORS Errors (Local Testing)

**Problem:** Can't load JSON file locally  
**Solution:** Use a local server:
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` (not `file://`)

---

## API Reference

### ESPN API Endpoints

**Scoreboard:**
```
http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
?seasontype=3&week=4&year=2026
```

**Game Details:**
```
http://site.api.espn.com/apis/site/v2/sports/football/nfl/summary
?event={game_id}
```

### JSON Data Structure

`championship_results.json`:

```json
{
  "generated_at": "2026-01-26T15:30:00",
  "weekend": "Conference Championships - Jan 25-26, 2026",
  "team1": {
    "name": "TEAM 1",
    "total_points": 150.54,
    "roster": [
      {
        "position": "QB",
        "name": "Patrick Mahomes",
        "team": "KC",
        "stats": "320 pass yds, 3 TD",
        "points": 38.8
      }
    ]
  },
  "team2": { ... },
  "top_performers": [ ... ]
}
```

---

## Advanced Features

### Add Multiple Matchups

Create separate pages for each matchup:

```
index.html           → Championship Game
semifinals.html      → Divisional Round
wildcard.html        → Wild Card Round
```

### Add Historical Data

Save JSON files by week:

```bash
cp championship_results.json data/week4_results.json
```

Then create a "Previous Weeks" section showing historical matchups.

### Email Notifications

Use GitHub Actions to send email updates:

```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{secrets.MAIL_USERNAME}}
    password: ${{secrets.MAIL_PASSWORD}}
    subject: Fantasy Update - Team 1 vs Team 2
    body: file://email_template.html
```

---

## Support

### Issues?

Open an issue on GitHub: [Create Issue](https://github.com/YOUR-USERNAME/nfl-playoff-tracker/issues)

### Want to Contribute?

Pull requests welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a PR

---

## License

MIT License - feel free to use this for your own fantasy leagues!

---

## Credits

**Created by:** Your Name  
**ESPN API:** ESPN's public API (no key required)  
**Design:** Sports broadcast-inspired aesthetic  
**Fonts:** Bebas Neue, Rajdhani, Barlow Condensed (Google Fonts)

---

## Changelog

### v1.0.0 (Jan 2026)
- Initial release
- Championship Weekend support
- ESPN API integration
- Responsive design
- GitHub Actions auto-updates
