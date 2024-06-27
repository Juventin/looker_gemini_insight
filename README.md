# Looker Gemini Insight

## Overview

Looker Gemini Insight is a custom visualization designed to harness the power of Gemini for advanced data analysis within Looker. This visualization aims to provide summarized interpretations and predictive insights based on selected dimensions and measures from your data.

### Key Features:
- **Summarization:** Gain clear, concise summaries and interpretations of your data based on chosen dimensions and measures.
- **Predictive Insights:** Utilize predictive analytics to forecast future trends and outcomes using the selected data dimensions and measures. 🔮

### Requirements:
- Dimensions and measures must be explicitly named and ideally include descriptions for accurate interpretation.
- For time-based predictions, ensure your data includes a date or datetime dimension.

## Installation

To install Looker Gemini Insight, follow these steps:

### 1. Deploy Cloud Run

1. **Navigate to the `cloud_run` directory** in the project repository.
2. Create a `.env.yaml` file containing:
   ```yaml
   PROJECT_ID: <YOUR_PROJECT_ID>
   ```
2. **Deploy the Cloud Run service** on your GCP project. You can use the following command in your terminal:
   ```sh
   gcloud run deploy looker-gemini-insight  --allow-unauthenticated --env-vars-file=.env.yaml --source .
   ```
   Ensure you have the necessary permissions and billing is enabled on your GCP project.

### 2. Integrate into Looker

1. **Modify your Looker manifest** to include the custom visualization by adding the block from `looker/manifest.lookml` in your Looker project manifest file. Replace the url with the URL of your deployed Cloud Run service.

2. **Save and deploy** your changes in Looker.

## Usage

Once installed, you can start using the Looker Gemini Insight visualization in your Looker dashboards and explores.

1. **Select dimensions and measures** that you want to analyze.
2. **Select the "Visualization" tab**.
3. **Choose "Gemini Insight"** from the list of available visualizations.
4. **Use the edit panel to chose between Summary or Forecast** and explore Gemini analytics capabilities to get useful insight or forecast future trends based on your data.

The Looker Gemini Insight visualization will automatically provide summarized interpretations or predictive insights based on the selected data.

## Billing

The Looker Gemini Insight uses GCP services, and the billing is associated with your GCP project. Make sure to monitor your usage to manage costs effectively.

---

*Sunrise Team*