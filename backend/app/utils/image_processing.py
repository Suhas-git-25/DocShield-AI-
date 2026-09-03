"""
DocShield AI - Image Processing & Forensics Utilities
Handles Error Level Analysis (ELA), Patch Feature Maps, Attention Rollout Simulation, and Heatmap overlays.
"""

import io
import os
from typing import Tuple, Optional
import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ImageFilter
import matplotlib

def compute_error_level_analysis(image: Image.Image, quality: int = 90, scale: int = 15) -> Tuple[np.ndarray, Image.Image]:
    """
    Computes Error Level Analysis (ELA) on an image.
    Returns: (ela_intensity_matrix, ela_pil_image)
    """
    rgb_img = image.convert("RGB")
    
    # Save temporary compressed version
    buf = io.BytesIO()
    rgb_img.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    compressed_img = Image.open(buf).convert("RGB")

    # Difference between original and recompressed
    diff = ImageChops.difference(rgb_img, compressed_img)
    
    # Enhance difference
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema]) if extrema else 1
    if max_diff == 0:
        max_diff = 1
    scale_factor = 255.0 / max_diff if max_diff < 50 else scale
    
    enhancer = ImageEnhance.Brightness(diff)
    ela_enhanced = enhancer.enhance(scale_factor)
    
    # Convert to grayscale intensity matrix (0.0 to 1.0)
    diff_arr = np.array(diff, dtype=np.float32)
    intensity = np.mean(diff_arr, axis=2) / 255.0
    # Normalize
    if intensity.max() > 0:
        intensity = intensity / intensity.max()
        
    return intensity, ela_enhanced


def generate_attention_rollout_heatmap(
    image: Image.Image,
    tamper_bbox: Optional[list] = None,
    grid_size: int = 14
) -> np.ndarray:
    """
    Generates or simulates a ViT Attention Rollout heatmap matrix (H x W)
    with high attention weights centered around detected anomaly regions or features.
    """
    w, h = image.size
    # Create base low-level attention across document structure (headers, text lines)
    gray = np.array(image.convert("L"), dtype=np.float32) / 255.0
    edges = np.abs(np.gradient(gray, axis=0)) + np.abs(np.gradient(gray, axis=1))
    
    heatmap = edges * 0.3
    
    if tamper_bbox and len(tamper_bbox) == 4:
        # If absolute coordinates
        bx1, by1, bx2, by2 = tamper_bbox
        # Normalize if needed
        if bx1 <= 1.0 and bx2 <= 1.0:
            bx1, by1, bx2, by2 = int(bx1 * w), int(by1 * h), int(bx2 * w), int(by2 * h)
        
        bx1, by1 = max(0, int(bx1)), max(0, int(by1))
        bx2, by2 = min(w, int(bx2)), min(h, int(by2))

        # Create Gaussian peak around tampered bbox
        y_grid, x_grid = np.ogrid[:h, :w]
        center_x = (bx1 + bx2) / 2.0
        center_y = (by1 + by2) / 2.0
        sigma_x = max(15.0, (bx2 - bx1) / 2.5)
        sigma_y = max(15.0, (by2 - by1) / 2.5)
        
        gaussian = np.exp(-(((x_grid - center_x) ** 2) / (2 * sigma_x ** 2) + ((y_grid - center_y) ** 2) / (2 * sigma_y ** 2)))
        heatmap += gaussian * 0.85
    
    # Clip and smooth
    heatmap = np.clip(heatmap, 0.0, 1.0)
    return heatmap


def overlay_heatmap_on_image(
    image: Image.Image,
    heatmap: np.ndarray,
    alpha: float = 0.55,
    colormap: str = "turbo"
) -> Image.Image:
    """
    Renders colormap on heatmap and alpha blends it onto the original PIL image.
    """
    rgb_img = image.convert("RGB")
    w, h = rgb_img.size

    # Ensure heatmap matches image size
    if heatmap.shape != (h, w):
        heat_pil = Image.fromarray((heatmap * 255).astype(np.uint8))
        heat_pil = heat_pil.resize((w, h), resample=Image.BICUBIC)
        heatmap = np.array(heat_pil, dtype=np.float32) / 255.0

    # Apply colormap (turbo / jet)
    try:
        cmap = matplotlib.colormaps[colormap]
    except Exception:
        cmap = matplotlib.colormaps["turbo"]

    colored_heatmap = cmap(heatmap) # RGBA (0.0 - 1.0)
    colored_rgb = (colored_heatmap[:, :, :3] * 255).astype(np.uint8)
    heat_overlay_img = Image.fromarray(colored_rgb)

    # Blend
    blended = Image.blend(rgb_img, heat_overlay_img, alpha=alpha)
    return blended


def calculate_iou(box_a: list, box_b: list) -> float:
    """
    Calculates Intersection over Union (IoU) between two bounding boxes [x1, y1, x2, y2].
    """
    xA = max(box_a[0], box_b[0])
    yA = max(box_a[1], box_b[1])
    xB = min(box_a[2], box_b[2])
    yB = min(box_a[3], box_b[3])

    inter_area = max(0, xB - xA) * max(0, yB - yA)
    boxA_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    boxB_area = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])

    union_area = float(boxA_area + boxB_area - inter_area)
    if union_area <= 0:
        return 0.0
    return inter_area / union_area
