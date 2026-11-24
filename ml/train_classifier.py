import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
from .dataset_generator import generate_sensor_fusion_dataset

def train_sensor_model():
    df = generate_sensor_fusion_dataset(1200)
    features = [c for c in df.columns if c != "label"]
    X = df[features]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_split=4,
        random_state=42
    )

    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"Random Forest Classification Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    joblib.dump(clf, "sensor_fusion_rf.joblib")
    print("Model serialized to sensor_fusion_rf.joblib")
    return acc

if __name__ == "__main__":
    train_sensor_model()
