
**HealthSense AI**


**AI-Driven Multi-Agent Healthcare System**

The integration of Generative AI (GenAI) and Large Language Models (LLMs) has significantly transformed the healthcare sector by enabling advanced natural language processing, improving access to medical information, and streamlining patient interactions. AI-powered solutions can assist in diagnosing conditions, providing health recommendations, and offering 24/7 support to patients.

Despite the abundance of medical knowledge, accessing personalized and reliable health information remains a challenge. Many existing healthcare systems provide generic responses and lack contextual awareness. HealthSense AI is designed to bridge this gap by leveraging LLMs and the LangChain framework to offer intelligent, context-aware health information assistance.

**Business Problem Overview and Potential Impact**

Challenges in Healthcare Information Systems
Limited Personalization – Most healthcare information systems provide one-size-fits-all responses that lack user-specific relevance.
Lack of Context Awareness – Many AI assistants struggle to maintain conversation history and context over multiple interactions.
Fragmented Information Sources – Medical knowledge is scattered across multiple databases, making it difficult to consolidate accurate information efficiently.

**Key Problem Statement**

Develop an intelligent healthcare platform that streamlines medical service discovery and booking by analyzing hospital data, reviews, and healthcare metrics. 
The system will extract and compare key parameters to help users make informed healthcare decisions.
The solution will feature a comprehensive comparison engine for hospitals and diagnostic centers, an automated slot booking system, and detailed information about medical tests and procedures. The platform will incorporate a user-friendly chat interface to hospital comparisons, explore healthcare metrics, and facilitate seamless appointment scheduling.

**System Features**

Here's a structured breakdown of system features for HealthSense:

Data Processing & Analysis:
Load and process healthcare provider data, including hospitals, and
diagnostic info
Implement loading data from csv into mySQL
Healthcare Provider Comparison & Recommendation:
Generate comprehensive comparison metrics across healthcare facilities
Develop personalized recommendation system based on user preferences and requirements
Appointment Management System:
Real-time slot availability tracking
Diagnostic Services Information:
Maintain comprehensive test catalog with detailed descriptions
Provide preparation guidelines for various tests
Interactive UI & Dashboards:
Develop user-friendly interface for healthcare service exploration


**Dataset Overview**


To build an effective and reliable AI-driven healthcare assistant, HealthSense AI will use structured datasets stored in MySQL.

Hospital General Information Dataset
Contains hospital names, locations, specialties, capacity, and contact details.
Used for hospital comparisons and providing relevant hospital recommendations.
Source: Public healthcare directories and government datasets.
Hospital Information with Lab Tests Dataset

Includes details about available lab tests, diagnostic packages, and pricing.
Used for diagnostic services recommendations and health test comparisons.
Source: Aggregated medical lab datasets and public health data.
Hospitals Emergency Data Dataset

Contains hospital emergency department details, ambulance availability, and response times.
Used for emergency assistance and directing users to the nearest available emergency services.
Source: Public emergency response data and hospital records.
Doctor Availability Dataset

Contains doctor schedules, specializations, consultation availability, and hospital affiliations.
Used for doctor appointment recommendations and scheduling.
Source: Medical institutions and clinic appointment systems.
These datasets enable HealthSense AI to deliver accurate, data-driven healthcare recommendations.

**Architectural Diagram**
![image](https://github.com/user-attachments/assets/3a0ab872-8821-44b5-87e3-2439efffe319)

**Deployment**
![image](https://github.com/user-attachments/assets/00c33dd5-4484-4b29-b945-5f51fed0203e)


![image](https://github.com/user-attachments/assets/bde344e4-1e51-4b0f-9ad4-2f13e0e7d455)

![image](https://github.com/user-attachments/assets/de7543ea-d9e6-4d1f-b7a8-22268ba9e53f)


