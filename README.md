# Pixel Art Generator

![Pixel Art Example](https://example.com/pixel-art-sample.jpg) *(replace with actual example image)*

## Description

A web-based tool that transforms regular images into pixel art using an adaptive grid algorithm. The application analyzes image contrast and applies intelligent pixelation while preserving important edges and details.

## Features

- **Adaptive Pixelation**: Automatically adjusts block size based on image contrast
- **Customizable Settings**:
  - Base block size (4-64 pixels)
  - Contrast sensitivity control
  - Minimum block size limitation
  - Edge preservation adjustment
  - Color enhancement
- **Pre-processing Options**: Includes image blurring for smoother results
- **Real-time Preview**: Instantly see changes as you adjust parameters
- **Download Support**: Save your pixel art creations

## How It Works

The algorithm:
1. Divides the image into blocks of the specified base size
2. Calculates contrast for each block
3. Recursively subdivides high-contrast areas while keeping smooth areas as larger blocks
4. Applies color averaging within each final block
5. Allows for edge preservation and color boosting

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RamazanShimardanov/PixelArtGenerator.git
   cd PixelArtGenerator
    ``` 
2. Install dependencies:
    ```bash
   pip install -r requirements.txt
    ``` 

## Usage
Run the application:
  ```bash
    python app.py
  ``` 
  Then access the web interface at http://localhost:7860

## Technology Stack
- **Python** (v3.7+) – Primary programming language

- **NumPy** – For numerical computations and image array manipulation

- **Pillow** (PIL Fork) – Image processing (loading, filtering, and saving images)

- **Gradio** – Web UI framework for creating interactive ML demos

## Support
I will be glad of your support:
- Email: yokai1076@gmail.com
- Telegram: @gfyly
- GitHub Issues: [https://github.com/RamazanShimardanov/PixelArtGenerator](https://github.com/RamazanShimardanov/PixelArtGenerator)

