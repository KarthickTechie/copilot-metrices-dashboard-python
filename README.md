# 🚀 GitHub Copilot Metrics Dashboard

A Streamlit-based dashboard for visualizing GitHub Copilot organization metrics and usage statistics.

## 📊 Features

- **KPI Overview**: Track total code generated, accepted, acceptance rates, and active users
- **Daily Active Users Trend**: Monitor user engagement over time
- **Code Generation vs Acceptance**: Compare code generation and acceptance activities
- **Lines of Code Analysis**: Visualize LOC added vs deleted
- **Feature Usage Breakdown**: Understand which Copilot features are most used
- **IDE Usage Statistics**: See which IDEs are most popular among users

## 🛠️ Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd copilot-metrices-dashboard-python
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 📦 Requirements

- Python 3.7+
- streamlit
- pandas
- plotly

## 🚀 Usage

1. Ensure you have a `copilot_metrices.json` file in the project directory with your GitHub Copilot metrics data.

2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Open your browser and navigate to the URL displayed in the terminal (typically `http://localhost:8501`)

## 📄 Data Format

The dashboard expects a `copilot_metrices.json` file with the following structure:

```json
{
  "day_totals": [
    {
      "day": "2024-01-01",
      "daily_active_users": 100,
      "code_generation_activity_count": 500,
      "code_acceptance_activity_count": 400,
      "loc_added_sum": 1000,
      "loc_deleted_sum": 200,
      "totals_by_feature": [...],
      "totals_by_ide": [...]
    }
  ]
}
```

## 📈 Dashboard Sections

- **KPI Cards**: Quick overview of key metrics
- **Daily Active Users**: Line chart showing user engagement trends
- **Code Generation vs Acceptance**: Comparative line chart
- **LOC Analysis**: Grouped bar chart for lines added/deleted
- **Feature Breakdown**: Pie chart for latest day's feature usage
- **IDE Usage**: Bar chart showing IDE preferences

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.
