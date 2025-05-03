# SECTION 1 : PROJECT TITLE
## Aegis AI: Simplifying Travel Insurance with Intelligent Recommendations

![Aegis AI Logo](https://github.com/DesmondChoy/IRS-PM-2025-05-02-GRP-40-Aegis_AI_RecSys/blob/74a9e4b90d90fb77dc18e2e5731bd877cd370960/Video/aegis_ai.png)

---

# SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
Singaporean travelers face significant challenges selecting suitable travel insurance due to policy complexity, lack of transparency, and comparison fatigue. This project introduces Aegis AI, an intelligent recommendation system designed to address these pertinent issues.

In this report, the team will share details on how it has successfully developed and evaluated an LLM-driven workflow applying **Intelligent Reasoning Systems** principles such as automated knowledge representation, hybrid reasoning models, and semantic evaluation to the complex domain of travel insurance recommendation.

Quantitative evaluations demonstrated strong performance: the system achieved high pass rates, ranging from 85% to 100%, in recommending appropriate policies across four distinct and challenging test scenarios designed to probe specific coverage nuances. Furthermore, it successfully covered a high percentage (87.5%) of valid customer requirements identified across 80 diverse test cases, verified through ground truth analysis.

The project showcased the significant advancements in multi-modal LLMs, specifically Gemini 2.5 Pro, for **accurate knowledge extraction** from notoriously complex and variably formatted PDF policy documents. This capability proved to be a critical enabler for the entire reasoning pipeline, ensuring that subsequent comparisons and recommendations were based on reliable, structured data. Additionally, the **hybrid recommendation approach, combining initial quantitative scoring with LLM-driven qualitative re-ranking informed by transcript context**, proved effective in balancing objective requirement matching with nuanced contextual understanding.

The system demonstrably addresses key consumer pain points like policy complexity and lack of transparency by automating the laborious analysis of fine print and presenting comparisons clearly, representing a valuable application of AI reasoning techniques to improve decision-making in the insurance domain.

The user-facing application for this system is named **Aegis AI**. The name draws inspiration from mythology: the Aegis was the legendary shield of protection carried by Zeus and Athena. This name reflects the project's goal of providing robust protection (like the shield) through intelligent, modern solutions (AI).

---

# SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Choy Yong Yi Desmond | A0315402W | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| A0315402W@nus.edu.sg |
| Kenny Lau Jia Xu | A0179912U | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| A0179912U@nus.edu.sg |
| Kevin Manuel | A0315373H | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| A0315373H@nus.edu.sg |
| Soon Fu Meng | A0140502B | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| A0140502B@nus.edu.sg |

---

# SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

## Promotion Video

[![Aegis AI Promotion Video](http://img.youtube.com/vi/-AiYLUjP6o8/0.jpg)](https://youtu.be/-AiYLUjP6o8 "Sudoku AI Solver")

## System Video

[![Aegis AI System Video](http://img.youtube.com/vi/-AiYLUjP6o8/0.jpg)](https://youtu.be/-AiYLUjP6o8 "Sudoku AI Solver")

---

# SECTION 5 : USER GUIDE

`Refer to project report at Github Folder: SystemCode`

## Getting Started

Follow these steps to set up the project environment for running the backend scripts:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/DesmondChoy/IRS-PM-2025-05-02-GRP-40-Aegis_AI_RecSys.git
    cd .\IRS-PM-2025-05-02-GRP-40-Aegis_AI_RecSys\SystemCode\
    ```

2.  **Set Up Python Environment**:
    This project requires **Python 3.11 or 3.12** due to specific dependencies (as noted in `pyproject.toml`). Please ensure you have a compatible version installed.

    It's highly recommended to use a virtual environment.

    ### Creating and Activating a Virtual Environment

    **For Windows Users:**

    To create a virtual environment named `.venv` using Python 3.11 (replace `3.11` with your desired version if needed):
    ```bash
    py -3.11 -m venv .venv
    ```
    To activate the virtual environment:
    ```bash
    .venv\Scripts\activate
    ```

    **For macOS and Linux Users:**

    To create a virtual environment named `venv` using Python 3.11 (replace `python3.11` with the command that invokes Python 3.11 on your system if needed):
    ```bash
    python3.11 -m venv venv
    ```
    To activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

Once the virtual environment is activated, install the Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up API Keys**:
    Create a `.env` file in the project root and add your API keys required for LLM interactions:
    ```dotenv
    GOOGLE_API_KEY="your_google_api_key_here"
    OPENAI_API_KEY="your_openai_api_key_here"
    # OPENAI_MODEL_NAME="gpt-4o" # Optional: Defaults to gpt-4o if not set for CrewAI/Extractor
    ```

    - [Documentation](https://ai.google.dev/gemini-api/docs/api-key) to get GOOGLE_API_KEY
    - [Documentation](https://help.openai.com/en/articles/8867743-assign-api-key-permissions) to get OPENAI_API_KEY



4.  **Install Node.js Dependencies (Optional - for Local Frontend Development)**:
    This project includes a frontend web application component (`ux-webapp/`). **This step is optional** as the application is already deployed and accessible online (see "Online Access" section below).

    If you wish to run or develop the frontend *locally*, navigate to the `ux-webapp/` directory and install the required Node.js dependencies:
    ```bash
    cd ux-webapp
    npm install
    cd .. 
    ```
    *Note: Ensure you have Node.js and npm installed if performing this optional step.*

## Online Access (Aegis AI Web Interface)

The user-friendly **Aegis AI** web application is deployed and accessible online at:
[https://aegis-recsys.netlify.app/](https://aegis-recsys.netlify.app/)

You can use this link to explore the Aegis AI interface and functionality without needing to run the backend scripts or frontend locally.

## How to Run the Demo Workflow (Backend)

For a quick way to see the entire backend recommendation system workflow in action, use the dedicated demo script. This script runs all the main steps automatically and creates a summary report showing what happened.

**1. Basic Run (No Specific Scenario):**

This command runs the workflow without focusing on a specific pre-defined test case. It will generate a conversation, process it, compare policies, and create a recommendation, but it will skip evaluations that require a specific scenario.

```bash
python scripts/run_recsys_demo.py
```

**2. Run with a Specific Scenario:**

You can test the system with specific situations (scenarios). Replace `<scenario_name>` with one of the available scenarios.

```bash
python scripts/run_recsys_demo.py --scenario <scenario_name>
```

*   **Available Scenarios:** `pet_care_coverage`, `golf_coverage`, `public_transport_double_cover`, `uncovered_cancellation_reason`
*   **Optional Flag:** You can add `--skip_scenario_eval` at the end of the command (even if you provided a scenario) to specifically skip the final scenario-based evaluation step if needed.

**What Happens When You Run It?**

*   The script creates a unique ID (UUID) for this specific run.
*   It simulates a customer conversation (or uses the specified scenario).
*   It processes the conversation, extracts needs, compares policies, and generates a final recommendation.
*   It performs various quality checks and evaluations along the way.
*   **Most importantly:** It creates a summary file named `demo_summary_{uuid}.md` in the main project folder.

**Important Cost Note:** Running this demo script involves multiple calls to LLM APIs. Expect approximate costs of **USD $3** for Google Gemini API usage and **a few cents (USD)** for OpenAI API usage per run. Costs may vary based on API pricing changes and specific run complexity.

**Checking the Results:**

*   Look for the `demo_summary_... .md` file in the project's main directory after the script finishes.
*   Open this file to see the status of each step, links to output files (transcript, requirements, comparisons, recommendation), and any errors.

---
# SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

*   Executive Summary
*   Introduction
    *   Background & Problem Statement
    *   Objectives & Success Criteria
*   Business Case / Market Research
    *   Industry & Stakeholder Analysis
    *   Pain Points & Opportunity Sizing
    *   Competitive / Alternative Solutions
    *   Value Proposition & ROI
*   System Design
    *   High-level Architecture Diagram
    *   Key Design Principles
    *   Integration with NUS-ISS Semester 1 Curriculum
        *   Decision Automation: Knowledge-Based Reasoning Techniques
        *   Business Resource Optimization: Informed Search Techniques
        *   Knowledge Discovery & Data Mining Techniques
        *   System Designed with Cognitive Techniques or Tools
*   System Development & Implementation
    *   Development Environment & Technologies
    *   Component Implementation Details
        *   Data Generation
        *   Data Processing Pipeline
        *   Report Generation
        *   Evaluation Framework
        *   Core Services
        *   Orchestration & Demonstration
        *   Frontend Application
    *   Development Process & Iteration
*   Findings & Discussion
    *   Implementation Challenges
    *   Structured Prompting + Advancements in LLMs for Knowledge Extraction
    *   Quantitative Evaluation
        *   Evaluation Methodology and Rationale
        *   Scenario-Based Recommendation Evaluation
        *   Ground Truth Coverage Evaluation
        *   Summary of Quantitative Findings
    *   Qualitative Feedback / Learning Outcomes
        *   Creation of PDF extraction & Policy Comparison Report Evaluation
        *   Creation of Ground Truth Coverage Evaluation
        *   Why Hybrid Recommendation Logic?
        *   Enhancing Report Reliability through Consensus Mechanisms
        *   Limitations of Whole-Document Embeddings for Granular Policy Matching
    *   Limitations & Risks
    *   Future Enhancements
*   Conclusion
*   References
*   Appendix
    *   Project Proposal
    *   Mapping of System Functions to Lesson Materials
        *   Machine Reasoning
        *   Reasoning System
        *   Cognitive System
    *   Installation and User Guide

---

## SECTION 7 : MISCELLANEOUS

`Refer to Github Folder: Miscellaneous`

To objectively assess the performance and reliability of the implemented recommendation system, a quantitative evaluation framework was established. This framework focuses on two key aspects: the correctness of the final policy recommendation for specific, challenging scenarios, and the granular coverage of individual customer requirements by the recommended policy. 

### Scenario-Based Recommendation Evaluation

This evaluation assesses the system's ability to recommend the correct final policy (or one of a set of acceptable policies) for predefined test scenarios, each designed to probe specific coverage nuances or complex requirement combinations. The system was tested against four distinct scenarios (golf_coverage, pet_care_coverage, public_transport_double_cover, uncovered_cancellation_reason), each with 20 generated customer cases.

The results can be found here: SystemCode\data\evaluation\scenario_evaluation\scenario_evaluation_results.md

### Ground Truth Coverage Evaluation

Beyond evaluating the final recommendation correctness, this evaluation assesses how well the recommended policy covers the individual requirements extracted from the customer transcript. This provides a more granular measure of the recommendation's quality and alignment with specific user needs. The evaluation uses an EmbeddingMatcher to compare extracted requirements against a curated ground truth knowledge base (`data/ground_truth/ground_truth.json`) defining which requirements are covered by which policy tiers.

The results can be found here: SystemCode\data\evaluation\ground_truth_evaluation\coverage_evaluation_summary.md

---
