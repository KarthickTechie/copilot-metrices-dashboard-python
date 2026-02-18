# Fetch and Run GitHub Copilot Dashboard

This script fetches the latest GitHub Copilot metrics and displays them in the dashboard.

## Quick Start

1. **Configure your token and organization**:
   - Open `.env` file
   - Set `YOUR_GITHUB_TOKEN` to your GitHub personal access token
   - Open `fetch_metrics.py` and update `ORG_NAME` if needed

2. **Fetch latest metrics**:

   ```bash
   python fetch_metrics.py
   ```

3. **Run the dashboard**:
   ```bash
   streamlit run app.py
   ```

## Token Requirements

Your GitHub token needs one of these scopes:

- `copilot` - Full Copilot access
- `manage_billing:copilot` - Billing and usage data
- `read:org` - Organization read access

### Creating a Token

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Click "Generate new token (classic)"
3. Select the required scopes mentioned above
4. Copy the token and add it to your `.env` file

## Troubleshooting

### 403 Forbidden Error

- Verify your token has the correct scopes
- Ensure you're a member/admin of the organization
- Check that the organization name in `fetch_metrics.py` is correct
- Verify the organization has an active Copilot subscription

### 401 Unauthorized Error

- Check that your token is correctly set in `.env` file
- Ensure there are no extra spaces or quotes around the token

### 404 Not Found Error

- Verify the organization name is correct
- Ensure the organization has GitHub Copilot Business or Enterprise

## Organization Configuration

To change the organization, edit `fetch_metrics.py`:

```python
ORG_NAME = "your-org-name"  # Change this line
```

## Automated Updates

You can set up a scheduled task to fetch metrics automatically:

**Windows (Task Scheduler)**:

- Create a new task
- Set trigger to daily/weekly
- Action: Run `python fetch_metrics.py` in your project directory

**Linux/Mac (Cron)**:

```bash
# Run daily at 8 AM
0 8 * * * cd /path/to/project && python fetch_metrics.py
```
