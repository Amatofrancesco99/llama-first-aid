<div align="center">

<img src="https://github.com/Amatofrancesco99/llama-first-aid/blob/main/presentation/logo/logo.png" width="210" /><br>

# **LLAMA First Aid Analytics Dashboard: Tracking Usage, Identifying Common Issues, Pinpointing High-Risk Areas, and Analyzing Performance in Response Times for Data-Driven Insights**

![Views](https://komarev.com/ghpvc/?username=FirstAid&label=Views&color=4285F4&style=for-the-badge)
[![Presentation](https://img.shields.io/badge/Presentation-%23DB4437.svg?style=for-the-badge&logo=read-the-docs&logoColor=white)](presentation/presentation.pdf)
<br>
![Meta](https://img.shields.io/badge/Meta-%23F4B400.svg?style=for-the-badge&logo=Meta&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%230F9D58.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/PYTHON-%234285F4?style=for-the-badge&logo=python&logoColor=white&color=4285F4)

> *This project secured second place in the LLaMA Impact Rome Hackathon 2024 ([lablab.ai](https://lablab.ai/hackathon-llama-impatto-roma)).*

</div>

## **Overview**

The **LLAMA First Aid Analytics Dashboard** is a powerful tool designed to provide real-time data insights, performance metrics, and historical trends related to the LLAMA First Aid application. This dashboard aggregates user interactions, session data, emergency scenarios, and medical classifications, enabling stakeholders to analyze the app's efficiency and make data-driven decisions to improve overall performance.

The primary goal of this dashboard is to support LLAMA First Aid’s continuous improvement by offering actionable insights into system performance, user engagement, and emergency response patterns. With detailed views of real-time data, emergency session analysis, and geographical trends, this tool allows LLAMA First Aid’s team to ensure the app is always ready to deliver timely, accurate, and effective assistance during critical situations.

## **Key Features**

- **Real-Time Monitoring**  
  The dashboard continuously updates with real-time user session data, giving immediate visibility into app usage, session distribution, and emergency activity. Whether you need to track how many users are interacting with the app or the current status of emergency scenarios, the real-time data monitoring feature provides instant, actionable insights.

- **Interactive Filters**  
  Customizable filters allow users to drill down into the data based on session details, app versions, medical classifications, and severity levels. This flexibility is essential for targeted analysis and helps uncover trends in specific user groups or types of emergencies.

- **Session Activity Analysis**  
  The dashboard presents side-by-side comparisons of this month's activity versus last month's, as well as insights into sessions with location data enabled versus those without. These comparisons help evaluate whether user behavior or app engagement is improving or if certain areas need attention.

- **Geographical Insights**  
  Integrated choropleth maps and heatmaps visualize the geographical distribution of user sessions and emergency incidents, highlighting areas with the highest frequency of emergencies. This geographic data can inform resource allocation, response strategies, and areas that may require targeted outreach or support.

  Additionally, **timelapse capabilities** in geographical insights allow users to visualize how emergency behavior and app usage patterns evolve over time. This dynamic feature makes it easier to identify trends, monitor shifts in activity, and adjust strategies accordingly based on historical data.

- **Performance Metrics**  
  Key performance indicators (KPIs) such as average response time, interactions per session, and time to identify and resolve issues are tracked and visualized. These metrics provide a clear picture of how efficiently the app responds to emergencies and where there might be room for optimization.

- **Medical Class and Severity Insights**  
  The dashboard offers a deep dive into the most frequent medical issues reported and their severity levels. This data is invaluable for prioritizing app updates, refining emergency response protocols, and ensuring the system is optimized for the most common situations users face.

- **Session History & Long-Term Trends**  
  All session data, including timestamps, app versions, severity, and medical classes, are stored in historical logs. This enables the team to analyze long-term trends, evaluate the accuracy of advice given, and identify opportunities for further improvement.

## **Dashboard Components**

### **1. Users Page**  
The Users Page is the heart of user session analysis. It provides an overview of key metrics, with a side-by-side comparison of monthly sessions, common medical classes, and severity levels. Here’s a breakdown of the key features:

- **This Month vs. Last Month**:  
  Compare the total number of sessions this month to last month's data to spot trends in user activity and identify any patterns or anomalies.
  
- **Medical Class Frequency**:  
  Visualize the most common medical classifications across sessions, helping to pinpoint the types of emergencies users encounter most often. This can guide app enhancements, ensuring users receive the most relevant advice based on frequent scenarios.

- **Severity Level Breakdown**:  
  Analyze the distribution of emergencies based on severity, from minor injuries to life-threatening conditions. By understanding severity trends, LLAMA First Aid can prioritize and improve the advice provided for the most critical situations.

- **Geographical Insights**:  
  The **Choropleth Map** and **Heatmap** provide detailed geographical representations of where sessions are taking place. This helps track the spread of emergency incidents and identify high-priority regions for potential resource allocation.

### **2. Performance Page**  
The Performance Page is designed to assess the effectiveness and speed of the app in real-time emergency situations:

- **Response Time Analysis**:  
  Track average response times across different sessions, identifying areas where response time can be improved. Time-sensitive emergencies need immediate assistance, so minimizing response delays is crucial.

- **Interactions Per Session**:  
  This metric measures how many interactions users have with the app during an emergency, indicating the level of engagement and the app's ability to maintain attention in critical moments.

- **Time to Solve**:  
  Evaluate how quickly users are receiving accurate advice to resolve their emergencies. This insight is key to ensuring LLAMA First Aid is optimizing its algorithms to offer timely solutions in every situation.

## **Geographical Insights**

- **Choropleth Map of Sessions**:  
  The choropleth map provides a heatmap-style visualization of sessions across different geographic locations, helping stakeholders identify high-traffic areas where emergency incidents are more common. This visual cue allows for better resource planning and targeted outreach.

- **Global Heatmap of Emergency Activity**:  
  The heatmap reveals patterns of emergency activity worldwide, showing where LLAMA First Aid is most frequently used. This global view is essential for understanding regional usage trends, which can inform app marketing efforts or emergency preparedness strategies.

- **Timelapse Capabilities**:  
  With timelapse capabilities, users can track changes in emergency behavior and app usage patterns over time. This feature allows for the visualization of evolving trends, providing insights into shifts in user behavior, emergency types, and geographic concentration. By analyzing these changes over days, weeks, or months, stakeholders can adjust their strategies and resources to match the current demands.

## **Data Insights**

- **Medical Class Distribution**:  
  View which medical classifications are most common and how frequently they occur across all sessions. Understanding the distribution of medical classes can drive improvements to app content and prioritize updates for conditions with higher occurrence rates.

- **Severity Level Insights**:  
  The severity levels of emergencies help highlight critical issues, giving a clear view of how many severe emergencies users face compared to more minor cases. This helps the team ensure that the most severe situations are handled with the utmost priority.

- **User Response Time Metrics**:  
  Analyze user response times and identify any delays in solving medical emergencies. This will be crucial for optimizing user experience and ensuring the app provides quick, actionable advice when every second counts.

## **Data-Driven Improvements**

The **LLAMA First Aid Analytics Dashboard** helps create a cycle of continuous improvement. By storing data in a centralized Google Cloud Platform (GCP) bucket, the app ensures every session is recorded and analyzed. This historical data is used to evaluate trends, monitor system performance, and guide updates and optimizations to the app’s algorithms.

The ability to examine this data over time provides a valuable feedback loop, enabling the LLAMA team to refine user experience, improve medical classifications, and respond to evolving user needs. This ongoing analysis ensures the app remains a trusted resource in emergency medical situations.

## **Why It Matters**

In emergency situations, every second counts. The **LLAMA First Aid Analytics Dashboard** is not just about collecting data — it's about leveraging that data to make the app more responsive, efficient, and reliable. By tracking key performance metrics, analyzing geographical trends, and examining real-time user sessions, LLAMA First Aid is equipped to deliver the best possible assistance when users need it the most.

With data-driven insights, the LLAMA team can enhance system performance, optimize user experience, and ensure that emergency situations are handled swiftly and effectively. The ultimate goal is to help save lives, and the dashboard plays a critical role in achieving that objective.

By continually monitoring system performance and making iterative improvements, LLAMA First Aid can maintain its position as a powerful, life-saving tool that provides users with the right advice at the right time — no matter where they are or what emergency they're facing.
