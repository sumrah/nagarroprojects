# README - GenAI Chatbot for Prehab4Me

## Project Title: GenAI Chatbot for Prehab4Me


## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Installation](#installation)
4. [Model Selection](#model-selection)
5. [Running the Notebook](#running-the-notebook)
6. [Dependencies](#dependencies)
7. [Using Gradio](#using-gradio)
8. [Uploading Files to Google Cloud](#uploading-files-to-google-cloud)
9. [Fine-tuning the Model in Google Cloud](#fine-tuning-the-model-in-google-cloud)

---

## Overview

This project involves the development of a Generative AI chatbot designed for the Prehab4Me initiative. The chatbot utilizes Gemini models to enhance user interaction and provide prehabilitation guidance. The notebook leverages Google Vertex AI for model deployment and interaction.

The notebook outlines the following:

- Project Introduction and Goals
- Model Options (Gemini 1.5 Pro and Gemini 1.5 Flash)
- Setup and Installation
- Code for Model Interaction and API Calls

---

## Getting Started

The notebook provides a step-by-step guide to set up the environment and interact with Gemini models for Prehab4Me.

### Key Sections:

- **Installation of Vertex AI SDK**
- **API Authentication**
- **Code to Invoke the Chatbot Model**
- **Testing and Evaluation**

---

## Installation

To use the notebook, install the necessary dependencies by following the instructions in the "Getting Started" section:

```bash
pip install google-cloud-aiplatform
```

Additionally, ensure you have Jupyter Notebook or Jupyter Lab installed:

```bash
pip install notebook
```

---

## Model Selection

The notebook outlines two potential model options:

- **Gemini 1.5 Pro** – Higher accuracy, suitable for complex queries.
- **Gemini 1.5 Flash** – Faster and cost-effective, ideal for simpler tasks.

---

## Running the Notebook

1. Clone or download this repository.
2. Install dependencies as listed.
3. Open the notebook in Jupyter Lab or Jupyter Notebook:

```bash
jupyter notebook Prehab4MeGenAI.ipynb
```

4. Follow the notebook sections step by step to interact with the AI chatbot.

---

## Dependencies

- Python 3.x
- Google Cloud Vertex AI SDK
- Jupyter Notebook

---

## Using Gradio

Gradio is used to create a simple and interactive web interface for the chatbot. This allows users to interact with the model through a user-friendly web UI without needing to write code.

### Installation

Install Gradio using the following command:

```bash
pip install gradio
```

### Running Gradio Interface

Add the following code snippet to launch the Gradio interface:

```python
import gradio as gr

def chatbot_response(prompt):
    # Call to AI model here
    return "Chatbot response based on: " + prompt

iface = gr.Interface(fn=chatbot_response, inputs="text", outputs="text")
iface.launch()
```

Running this code will launch a local web interface where users can interact with the chatbot by entering text prompts.

---

## Uploading Files to Google Cloud

To upload PDF files and videos to Google Cloud for use with the chatbot, follow these steps:

### 1. Set Up Google Cloud Storage

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or select an existing one.
- Navigate to "Cloud Storage" and create a new bucket.
- Choose a globally unique name for your bucket.

### 2. Upload Files

- Click on the bucket you created.
- Select "Upload Files" and choose the PDF files or videos you wish to upload.

### 3. Access Files in the Chatbot

- In the Cloud Console, click on the uploaded file to open its details.
- Copy the **Public URL** or **gsutil URI** to access the file programmatically.
- If needed, adjust the file permissions to ensure public or restricted access, depending on your chatbot’s requirements.

### 4. Link Files to Chatbot

- Use the copied URLs to link the uploaded files directly within your chatbot for processing or display.

---

## Fine-tuning the Model in Google Cloud

Fine-tuning the Gemini model for specific use cases can be done using Google Cloud's supervised fine-tuning options. Follow these steps to fine-tune the model:

### 1. Access Vertex AI

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Navigate to "Vertex AI" from the left-hand menu.
- Select "Model Garden" and locate the Gemini model you wish to fine-tune.

### 2. Initiate Fine-tuning

- Click on the model and choose the "Fine-tune" option.
- Upload your labeled dataset in CSV or JSONL format. Ensure the dataset is well-structured and aligned with the task.
- Set the training parameters, including the number of epochs and learning rate.

### 3. Monitor Training

- The fine-tuning process will begin, and you can monitor the progress under the "Training" tab.
- After completion, Vertex AI will generate a fine-tuned version of the model.

### 4. Deploy the Fine-tuned Model

- Go to "Models" under Vertex AI and select the fine-tuned model.
- Deploy the model by creating an endpoint and specifying the resources (CPUs, GPUs) required.
- Once deployed, use the endpoint URL to integrate the fine-tuned model into your chatbot application.

---

