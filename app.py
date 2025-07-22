import numpy as np
from PIL import Image, ImageFilter
import gradio as gr
import io
import os
import tempfile

TEST_IMG_DIR = "test_img"
os.makedirs(TEST_IMG_DIR, exist_ok=True)

def calculate_contrast(region):
    if len(region.shape) == 3:  
        gray = np.mean(region, axis=2)
    else:
        gray = region
    return np.std(gray)

def load_image(input_data):
   
    if input_data is None:
        return None
    if isinstance(input_data, str):
        if os.path.exists(input_data):
            return Image.open(input_data)
        return None
    elif isinstance(input_data, np.ndarray):
        return Image.fromarray(input_data)
    return input_data

def adaptive_grid_pixelate(input_data, base_size=16, contrast_thresh=20, min_size=4, 
                         blur_radius=2, edge_preserve=0.5, color_boost=1.0):

    img = load_image(input_data)
    if img is None:
        return None
        
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    if blur_radius > 0:
        img = img.filter(ImageFilter.GaussianBlur(blur_radius))
    
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    result = img_array.copy()
    
    def process_block(x, y, size):
        nonlocal result
        if size < min_size:
            return
        
        block = img_array[y:y+size, x:x+size]
        if block.size == 0:
            return
        
        contrast = calculate_contrast(block)
        edge_factor = 1.0 - edge_preserve
        adaptive_thresh = contrast_thresh * (1.0 + edge_factor * 2)
        
        if contrast > adaptive_thresh and size > min_size * 2:
            half = size // 2
            process_block(x, y, half)
            process_block(x + half, y, half)
            process_block(x, y + half, half)
            process_block(x + half, y + half, half)
        else:
            avg_color = np.mean(block, axis=(0, 1))
            if color_boost != 1.0:
                avg_color = 128 + (avg_color - 128) * color_boost
            avg_color = np.clip(avg_color, 0, 255).astype(np.uint8)
            result[y:y+size, x:x+size] = avg_color
    
    for y in range(0, height, base_size):
        for x in range(0, width, base_size):
            block_size = min(base_size, width - x, height - y)
            process_block(x, y, block_size)
    
    return Image.fromarray(result)

def process_image(input_data, base_size, contrast_thresh, min_size, 
                 blur_radius, edge_preserve, color_boost):
    result_img = adaptive_grid_pixelate(input_data, base_size, contrast_thresh, 
                                      min_size, blur_radius, edge_preserve, color_boost)
    if result_img is None:
        return None, None
    

    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    result_img.save(temp_file.name, "JPEG", quality=95)
    temp_file.close()
    
    return result_img, temp_file.name

with gr.Blocks(title="Pixel Art Generator") as demo:
    gr.Markdown("""
    # 🎮 Pixel Art Generator
    # Author: Yokai. My telegram @gfyly - contact me for cooperation and work)❤         
    *Automatically updates when settings change*
    """)
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Upload Image", type="filepath")
            
            with gr.Accordion("⚙️ Basic Settings", open=True):
                base_size = gr.Slider(4, 64, value=16, step=4, label="Block size (pixels)")
                contrast_thresh = gr.Slider(0, 50, value=20, label="Contrast sensitivity")
                min_size = gr.Slider(2, 16, value=4, step=2, label="Minimum block size")
            
            with gr.Accordion("🎨 Advanced Settings", open=False):
                blur_radius = gr.Slider(0, 10, value=2, step=0.5, label="Pre-processing blur")
                edge_preserve = gr.Slider(0, 1, value=0.5, step=0.1, label="Edge preservation (0=full pixelation)")
                color_boost = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Color boost")
        
        with gr.Column():
            output_image = gr.Image(label="Result", type="pil", interactive=False)
            download_btn = gr.DownloadButton(label="⬇️ Download Result", visible=False)

    inputs = [input_image, base_size, contrast_thresh, min_size, 
             blur_radius, edge_preserve, color_boost]
    
    def update_ui(*args):
        result_img, temp_path = process_image(*args)
        if result_img is None:
            return None, gr.update(visible=False)
        
        return result_img, gr.update(
            value=temp_path,
            visible=True
        )
    
    for component in inputs:
        component.change(
            fn=update_ui,
            inputs=inputs,
            outputs=[output_image, download_btn],
            show_progress="hidden"
        )

    #tests
    example_files = [
        os.path.join(TEST_IMG_DIR, "test_img_1.jpg"),
        os.path.join(TEST_IMG_DIR, "test_img_2.jpg")
    ]
    

    valid_examples = [f for f in example_files if os.path.exists(f)]
    
    if valid_examples:
        gr.Examples(
            examples=[[f] + [16, 20, 4, 2, 0.5, 1.0] for f in valid_examples],
            inputs=inputs,
            outputs=[output_image, download_btn],
            fn=update_ui,
            cache_examples=True,
            run_on_click=True,
            label="Example Images"
        )

if __name__ == "__main__":
    demo.launch()