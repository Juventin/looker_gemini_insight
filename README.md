# Looker Gemini Insight

## Overview

Looker Gemini Insight is a custom visualization designed to harness the power of Gemini for advanced data analysis within Looker. 

This visualisation takes the dimensions and measures (and their metadata) that you have selected from your Explore to generate summarised interpretations and predictive insights with a single click.

> With Gemini Insight on Looker, you can effortlessly summarise complex data sets and predict trends, empowering your business to make data-driven decisions.

### Key Features:
- **✏️ Summarization:** Gain clear, concise summaries and interpretations of your data based on chosen dimensions and measures.
- **🔮 Predictive Insights:** Utilize predictive analytics to forecast future trends and outcomes using the selected data dimensions and measures.

![Example Image](https://github.com/user-attachments/assets/b040cba4-68cb-4792-9bc1-f092edacd267)

### Requirements:
- Dimensions and measures must be **explicitly named** and ideally include **descriptions** for accurate interpretation.
- For time-based predictions, ensure your data includes a date or datetime dimension.

## Installation

To install Looker Gemini Insight, follow these steps:

### 1. Deploy the Cloud Run back-end

1. **Navigate to the `cloud_run` directory** in the project repository.
2. **Create a `.env.yaml` file** containing:
   ```yaml
   PROJECT_ID: <YOUR_PROJECT_ID>
   ```
2. **Deploy the Cloud Run service** on your GCP project. You can use the following command in your terminal:
   ```sh
   gcloud run deploy looker-gemini-insight  --allow-unauthenticated --env-vars-file=.env.yaml --source .
   ```
   Ensure you have the necessary permissions and billing is enabled on your GCP project.

### 2. Integrate the Custom Visualization into Looker

1. **Update your Looker manifest** to include the custom visualization by adding the block from `looker/manifest.lookml` in your Looker project manifest file. Replace `<YOUR_CLOUD_RUN_URL>` with the URL of your deployed Cloud Run service.

2. **Save and deploy** your changes in Looker.

## Usage

Once installed, you can start using the Looker Gemini Insight visualization in your Looker dashboards and explores.

1. **Select dimensions and measures** that you want to analyze.
2. **Select the "Visualization" tab**.
3. **Choose "Gemini Insight"** from the list of available visualizations.
4. *(Optional)* **Use the edit panel** to chose between Summary or Forecast.

The Looker Gemini Insight visualization will automatically provide summarized interpretations or predictive insights based on the selected data.

## Billing

The Looker Gemini Insight uses GCP services, and the billing is associated with your GCP project. Make sure to monitor your usage to manage costs effectively.

---

## FAQ

<details>
  <summary>Is there a way to verify the server is running correctly?</summary>

  Yes, you will get 'Hello, World!' message on `https://<YOUR_CLOUD_RUN_URL>.run.app/`.
</details>

<details>
  <summary>Does the server allow unauthenticated invocations?</summary>
  
  Yes
</details>

<details>
  <summary>How can we automatically roll back (clan up) the resources created by this repo?</summary>
  
  *The Terraform configuration will soon be available.*
  
  The resources created are :
   - looker-gemini-insight Cloud Run : https://console.cloud.google.com/run?project=<PROJECT_ID>
   - looker-gemini-insight Artifact : https://console.cloud.google.com/artifacts/docker/<PROJECT_ID>/europe-west1/cloud-run-source-deploy?project=<PROJECT_ID>
   - Cloud Build Storage bucket : https://console.cloud.google.com/storage/browser/<PROJECT_ID>_cloudbuild?project=<PROJECT_ID>
</details>

---

## 🔗 Links

- [Demo video](https://www.youtube.com/watch?v=mw-2q68RqFw)
- [Demo slides](https://docs.google.com/presentation/d/1j6oT0jyhlEQ-FOplNH7we63KS4N70ydpaqhiJ14St3c/edit?usp=sharing)
- [GitHub repository](https://github.com/Juventin/looker_gemini_insight)

---

*Developed for the ***Looker Hackathon (Vertex AI Edition)*** by ***Jeremy Juventin****
