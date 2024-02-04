# TensorFlow Extended Pipeline Plant Disease Detection

This project utilizes TensorFlow Extended (TFX) to implement a machine learning pipeline for detecting plant diseases. The pipeline includes data ingestion, preprocessing, model training, evaluation, and serving. It aims to provide a scalable and efficient solution for plant disease detection, which is crucial for enhancing crop production and management.

<div style="display: flex; flex-direction: row; justify-content: start; align-items: center;">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=TensorFlow&logoColor=white" alt="TensorFlow" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Keras-D00000?style=flat-square&logo=Keras&logoColor=white" alt="Keras" />
  <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Machine%20Learning-0078D4?style=flat-square&logo=azure-devops&logoColor=white" alt="Machine Learning" />
</div>
<br/>

## Dataset

The dataset used in this project is [New Plant Diseases](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset), which consists of leaf images of various plants, including healthy and diseased samples. The dataset includes:

- **Number of Classes:** 38 (including healthy and diseased conditions)
- **Total Images:** Approximately 87,000
- **Image Size:** 256x256 pixels
- **Split:** 80/20

## Model

I have fined tuned a convolutional neural network (CNN) model for plant disease detection. The model architecture is designed to extract and learn from the visual patterns of plant leaf images effectively.

### Model Features:

- **Input Size:** 256x256 pixels
- **Layers:** Customized layers including convolutional, pooling, and dense layers
- **Output:** Classification/Type of Disease

## TensorFlow Components

The project leverages several TensorFlow Extended (TFX) components to streamline the machine learning pipeline:

- **ExampleGen:** Ingests and imports data into the TFX pipeline.
- **StatisticsGen:** Computes statistics for data analysis and validation.
- **SchemaGen:** Infers a schema for the data.
- **ExampleValidator:** Identifies and highlights anomalies and missing values in the dataset.
- **Transform:** Performs feature engineering on the dataset.
- **Trainer:** Trains the model using TensorFlow.
- **Evaluator:** Evaluates the trained model against a test set.
- **Pusher:** Deploys the model to a production environment.

## Demo

![Step 1](./Assets/1.png)

![Step 2](image-url-web-interface)

![Step 3](image-url-web-interface)

This section details how to interact with the project through a web interface or API, showcasing the detection capabilities in real-time.

For a web-based demo:

- Navigate to `<demo-url>` to access the interactive web application built with React and Flask.
- Upload an image of a plant leaf to get an instant prediction of its health status.

```bash
# To run the demo locally, follow these steps:

# Clone the repository
git clone <repository-url>

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py

# In a separate terminal, start the React frontend
cd frontend
npm install
npm start
```
