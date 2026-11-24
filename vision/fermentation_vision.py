import cv2
import numpy as np

def extract_fermentation_color_features(image_bgr: np.ndarray) -> dict:
    """Extracts mean hue, saturation, and thearubigin/chlorophyll color ratio."""
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    h_channel = hsv[:, :, 0]
    s_channel = hsv[:, :, 1]
    v_channel = hsv[:, :, 2]

    # Mask out background glare or shadow
    valid_mask = (v_channel > 40) & (v_channel < 230) & (s_channel > 30)
    
    if np.sum(valid_mask) == 0:
        return {"hue_mean": 0.0, "saturation_mean": 0.0, "oxidation_score": 0.0}

    mean_hue = float(np.mean(h_channel[valid_mask]))
    mean_sat = float(np.mean(s_channel[valid_mask]))

    # Copper / amber hue (15 - 30 in OpenCV 0-180 scale) represents optimal oxidation
    oxidation_score = max(0.0, 1.0 - abs(mean_hue - 22.0) / 30.0)

    return {
        "hue_mean": round(mean_hue, 2),
        "saturation_mean": round(mean_sat, 2),
        "oxidation_score": round(oxidation_score, 4)
    }
