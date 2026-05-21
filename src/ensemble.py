import numpy as np

class EnsembleModel:
    """Ensemble logic for predictions."""
    def __init__(self, weight_prophet=0.35, weight_xgb=0.65):
        self.weight_prophet = weight_prophet
        self.weight_xgb = weight_xgb
        
    def predict(self, pred_prophet, pred_xgb):
        """Combine predictions."""
        return self.weight_prophet * pred_prophet + self.weight_xgb * pred_xgb
