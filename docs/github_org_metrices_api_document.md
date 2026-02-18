# Get Organization Copilot Metrics Report

## Overview

Retrieves the latest 28-day GitHub Copilot usage metrics report for an organization. This endpoint provides comprehensive insights into Copilot adoption, usage patterns, and engagement metrics across your organization.

## API Endpoint

```
GET https://api.github.com/orgs/sysarc-svn/copilot/metrics/reports/organization-28-day/latest
```

## Purpose and Use Case

This endpoint is designed for:

- **Organization Administrators**: Monitor Copilot adoption and ROI across teams
- **Team Leads**: Track usage trends and identify engagement opportunities
- **Analytics**: Generate reports on AI-assisted development metrics
- **Compliance**: Audit Copilot usage for license management and optimization

## Authentication Requirements

This endpoint requires authentication using a **Bearer token** in the `Authorization` header:

```
Authorization: Bearer YOUR_GITHUB_TOKEN

```

## Required Headers

### Accept

- **Value**: `application/vnd.github+json`
- **Purpose**: Specifies the GitHub API media type for the response format
- **Required**: Yes
- **Note**: This ensures you receive the response in GitHub's standard JSON format

### X-GitHub-Api-Version

- **Value**: `2022-11-28`
- **Purpose**: Specifies the GitHub API version to use
- **Required**: Recommended
- **Note**: Ensures consistent API behavior and response structure. Using a specific version prevents breaking changes from affecting your integration.

## Response Information

### Success Response (200 OK)

Returns a JSON object containing following fields:

{
"download_links": [
"https://copilot-reports-acc0engfa5gra7ha.b01.azurefd.net/organization-28-day-report/blue/v0/2026-02-16/213790859/54befd5f-4198-4f9d-8a4c-430f8aeea9d4_1_9dcab31735114c6d9149c0faeb01e8ad.json?rscd=attachment&rsct=application%2Foctet-stream&se=2026-02-18T01%3A16%3A27Z&sig=Bspa8QQ8OSnDTqb9oREaHGAdGdpR1LWdcF0X24GxURU%3D&ske=2026-02-18T01%3A16%3A27Z&skoid=6526645c-47ff-4ca0-9cd3-0c389ef43d92&sks=b&skt=2026-02-18T00%3A16%3A17Z&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skv=2026-02-06&sp=r&spr=https&sr=b&st=2026-02-18T00%3A16%3A17Z&sv=2026-02-06"
],
"report_end_day": "2026-02-16",
"report_start_day": "2026-01-20"
}

- **download_links**: Array of URLs to download the report in JSON format
- **report_end_day**: The last day included in the report (YYYY-MM-DD)
- **report_start_day**: The first day included in the report (YYYY-MM-DD)

use the `download_links` to retrieve the actual metrics data for analysis and reporting.

### Error Responses

- **401 Unauthorized**: Invalid or missing authentication token
- **403 Forbidden**: Token lacks required permissions or user doesn't have org access
- **404 Not Found**: Organization not found or no Copilot subscription
- **500 Internal Server Error**: GitHub API service issue

3. **Organization Scope**: Replace `sysarc-svn` in the URL with your organization name
4. **Privacy**: Individual user data may be aggregated depending on organization privacy settings
5. **Subscription Required**: Organization must have an active GitHub Copilot Business or Enterprise subscription

## API Documentation

For complete API reference, visit: [https://docs.github.com/en/rest/copilot/copilot-usage](https://docs.github.com/en/rest/copilot/copilot-usage)
