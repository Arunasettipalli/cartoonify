# Cartoonify Project - Overview and Technologies Used

## Project Summary
This Cartoonify project is a web app that transforms ordinary photos into cartoon-style images using image processing techniques. Users can upload images or take photos with their camera, apply different artistic effects like cartoon, pencil sketch, oil painting, sepia, or grayscale, and download the results.

## Key Features
- Upload images or use live camera input
- Multiple cartoonification styles and artistic filters
- Adjustable parameters for smoothing, edge detection, brightness, and contrast
- User-friendly web interface built with Streamlit
- Download processed images directly from the app

## Technologies and Libraries Used

- **Python 3.8+**: Programming language used for all code
- **Streamlit**: Framework to build the interactive web app UI
- **OpenCV (opencv-python-headless)**: Image processing library for filtering, edge detection, and effects
- **Pillow (PIL)**: Image handling and brightness/contrast adjustments
- **NumPy**: Numerical operations and array manipulation for images

## How It Works
The core cartoonification effect uses:
- Bilateral filtering for smoothing while preserving edges
- Adaptive thresholding for edge detection
- Bitwise operations to combine color and edges into a cartoon-like image

Additional filters like pencil sketch, oil painting effect, sepia tone, and grayscale are implemented using OpenCV and Pillow techniques.

## How to Run Locally
1. Clone the repository
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Run the app:  
   `streamlit run app.py`
4. Open the browser at the URL provided by Streamlit

---

