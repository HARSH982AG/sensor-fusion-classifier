import numpy as np
import pandas as pd

def generate_sensor_fusion_dataset(n_samples: int = 1000) -> pd.DataFrame:
    """Generates synthetic chemical sensor calibration curves across fermentation phases."""
    np.random.seed(42)
    classes = ["Under-Fermented", "Optimal", "Over-Fermented", "Tainted"]
    class_probs = [0.25, 0.40, 0.25, 0.10]
    
    labels = np.random.choice(classes, size=n_samples, p=class_probs)
    data = []

    for label in labels:
        if label == "Under-Fermented":
            mq3 = np.random.normal(0.8, 0.1)
            mq135 = np.random.normal(1.1, 0.1)
            cond = np.random.normal(1.5, 0.15)
            hue = np.random.normal(45, 5) # Greenish / yellowish
        elif label == "Optimal":
            mq3 = np.random.normal(2.1, 0.15)
            mq135 = np.random.normal(1.8, 0.15)
            cond = np.random.normal(2.4, 0.2)
            hue = np.random.normal(25, 4) # Rich copper / amber
        elif label == "Over-Fermented":
            mq3 = np.random.normal(2.8, 0.2)
            mq135 = np.random.normal(2.6, 0.2)
            cond = np.random.normal(2.9, 0.2)
            hue = np.random.normal(10, 3) # Dull dark brown
        else: # Tainted
            mq3 = np.random.normal(1.2, 0.3)
            mq135 = np.random.normal(3.2, 0.3)
            cond = np.random.normal(3.5, 0.3)
            hue = np.random.normal(5, 2)

        data.append({
            "mq3_volts": max(0.1, mq3),
            "mq135_volts": max(0.1, mq135),
            "mq2_volts": max(0.1, mq3 * 0.7 + np.random.normal(0, 0.05)),
            "tgs_volts": max(0.1, mq135 * 0.8 + np.random.normal(0, 0.05)),
            "cond1_volts": max(0.1, cond),
            "cond2_volts": max(0.1, cond * 0.95),
            "hue_mean": max(0, hue),
            "saturation_mean": np.random.normal(140, 15),
            "label": label
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_sensor_fusion_dataset(500)
    df.to_csv("sensor_calibration_data.csv", index=False)
    print("Generated 500 calibration samples saved to sensor_calibration_data.csv")
