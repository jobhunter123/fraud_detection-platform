from sklearn.ensemble import IsolationForest
import numpy as np
 
# Training data representing normal transaction patterns
X_train = np.array([
    [500, 2], [800, 2], [1000, 3], [1200, 2],
    [1500, 1], [2000, 2], [700, 3], [900, 2],
    [1100, 2], [600, 1], [1300, 3], [850, 2],
])
 
model = IsolationForest(contamination=0.15, random_state=42)
model.fit(X_train)
 
 
def get_anomaly_score(amount: float, frequency: int) -> int:
    """
    Returns additional risk points if the transaction is an ML-detected anomaly.
    Returns 0 for normal, 40 for anomaly.
    """
    data = np.array([[amount, frequency]])
    prediction = model.predict(data)
    return 40 if prediction[0] == -1 else 0