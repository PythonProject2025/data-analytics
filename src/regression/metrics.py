"""
Metrics class is used for evaluating model performance.
"""

from sklearn.metrics import r2_score


def evaluate_model(model, dataobj): # x_test, y_test
    y_pred = model.predict(dataobj['split_data']['X_test'])
    return r2_score(dataobj['split_data']['y_test'], y_pred),y_pred