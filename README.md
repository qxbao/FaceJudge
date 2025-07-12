# FaceJudge ML

A machine learning-based facial attractiveness rating system that collects, processes, and analyzes facial images to train a predictive model for attractiveness scoring.

## Overview

FaceJudge is a comprehensive system that:
- Collects facial images and attractiveness scores via a web interface
- Processes images using computer vision techniques
- Trains machine learning models to predict attractiveness ratings
- Provides a REST API for real-time predictions
- Includes data cleaning and validation tools

## Features

- **Web Interface**: Flask-based web application for image collection and rating
- **Face Detection**: Automatic face detection and validation using OpenCV and face_recognition
- **Machine Learning**: SVR (Support Vector Regression) model for attractiveness prediction
- **Data Management**: SQLite database for storing profiles and image metadata
- **Image Processing**: Automated face extraction and feature encoding
- **Data Cleaning**: Tools to remove corrupted images and maintain data integrity
- **Browser Extension**: JavaScript extension for Bumble integration

## Project Structure

```
FaceJudge/
├── app.py                 # Flask web application
├── database.py           # Database operations and schema
├── model.py              # Machine learning model implementation
├── image_processing.py   # Image processing and face detection
├── train.py              # Model training script
├── predict.py            # Prediction script for single images
├── cleaner.py            # Data cleaning utilities
├── bumble.js             # Browser extension for Bumble
├── templates/
│   └── index.html        # Web interface template
└── data/
    ├── swipes.db         # SQLite database
    └── images/           # Profile image storage
```

## Installation

### Prerequisites

- Python (3.12)
- OpenCV
- face_recognition library
- Flask
- scikit-learn
- SQLite

### Setup

1. Clone the repository:
```bash
git clone https://github.com/qxbao/FaceJudge.git
cd FaceJudge
```

2. Create virtual environment (optional):
    ```bash
    python -m venv .venv
    ```
    Then activate it
    ```
    ./.venv/Scripts/activate
    ```

3. Install required packages:
```bash
pip install -R requirements.txt
```

4. Initialize the database and folders:
```bash
python app.py
```

## Usage

### 1. Data Collection

Start the Flask web application:
```bash
python app.py
```

The server will run on `http://localhost:5000` and provide:
- `/judge` endpoint for submitting images and ratings

### 2. Data Cleaning

Clean corrupted images and maintain data integrity:
```bash
python cleaner.py
```

This will:
- Remove empty or corrupted images
- Remove images without detectable faces
- Clean empty directories
- Synchronize database with filesystem

### 3. Model Training

Train the machine learning model:
```bash
python train.py
```

Parameters:
- --tune (optional): tuning model before train 

### 4. Making Predictions

Predict attractiveness for a single image:
```bash
python predict.py
```
Parameters:
- --image (default=input.jpg)
- --age (required)
- --model (default=model.pkl)

### 5. Browser Extension

Use the `bumble.js` script as a browser extension to collect data from Bumble profiles.

## API Reference

### POST /judge

Submit profile images and attractiveness score.

**Request Body:**
```json
{
    "images": ["base64_encoded_image1", "base64_encoded_image2"],
    "age": 25,
    "score": 8.5
}
```

**Response:**
```json
{
    "profile_id": 123,
    "profile_folder": "uuid-string"
}
```

## Database Schema

### profiles
- `id`: Primary key
- `age`: Person's age
- `num_images`: Number of images in profile
- `profile_folder`: UUID folder name
- `score`: Attractiveness rating

### profile_images
- `id`: Primary key
- `profile_id`: Foreign key to profiles
- `image_order`: Image order in profile

## Model Details

The system uses a Support Vector Regression (SVR) model with:
- **Input**: 128-dimensional face encodings from face_recognition library
- **Features**: Mean facial features across all profile images
- **Target**: Attractiveness scores (continuous values)
- **Preprocessing**: StandardScaler normalization

## Data Flow

1. **Collection**: Images and scores submitted via web interface
2. **Storage**: Images saved to filesystem, metadata to database
3. **Cleaning**: Remove invalid/corrupted data
4. **Processing**: Extract face encodings and features
5. **Training**: Train ML model on processed features
6. **Prediction**: Use trained model for new image scoring

## Configuration

Key configuration options in the code:
- Database path: `data/swipes.db`
- Images path: `data/images/`
- Model parameters: Configurable in `model.py`
- Server settings: Port 5000, debug mode in `app.py`

## Contributing

1. Ensure all images contain exactly one detectable face
2. Maintain data quality through regular cleaning
3. Validate model performance after retraining
4. Follow privacy guidelines for image data

## License

This project is for educational and research purposes. Ensure compliance with applicable privacy laws and platform terms of service when collecting data.

## Troubleshooting

### Common Issues

1. **"Unsupported image type" error**: Ensure images are valid and readable by OpenCV
2. **No face detected**: Use the cleaner script to remove invalid images
3. **Model not found**: Train the model before making predictions
4. **Database errors**: Check if database file exists and is accessible

### Performance Tips

- Regularly run the cleaner script to maintain data quality
- Monitor disk space as image collections can grow large