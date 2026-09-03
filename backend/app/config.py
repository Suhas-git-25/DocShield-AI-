"""
DocShield AI - Application Configuration
"""

import os

class Settings:
    PROJECT_NAME: str = "DocShield AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"
    
    # Base paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "storage", "uploads")
    HEATMAP_DIR: str = os.path.join(BASE_DIR, "storage", "heatmaps")
    SAMPLE_DIR: str = os.path.join(BASE_DIR, "sample_data")
    
    # Model Thresholds
    RISK_THRESHOLD_LOW: float = 0.35
    RISK_THRESHOLD_HIGH: float = 0.65
    
    # Weights for Risk Fusion Engine
    WEIGHT_VISUAL_FORGERY: float = 0.45
    WEIGHT_RULE_METADATA: float = 0.25
    WEIGHT_FONT_CONSISTENCY: float = 0.20
    WEIGHT_MATH_DATE_SANITY: float = 0.10

    # Redis configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.HEATMAP_DIR, exist_ok=True)
