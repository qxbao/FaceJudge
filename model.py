from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

class Model:
    def __init__(self):
        self.model = None
        self.X = []
        self.y = []
        
    def load_model(self, filename='model.pkl'):
        """Load a pre-trained model from a file."""
        import pickle
        try:
            with open(filename, 'rb') as file:
                self.model = pickle.load(file)
        except FileNotFoundError:
            raise ValueError(f"Model file '{filename}' not found. Please ensure the model is trained and saved before loading.")
        
    def set_model(self, kernel="rbf", C=1.0, epsilon=0.1):
        """Set the model to be used for predictions."""
        from sklearn.svm import SVR
        self.model = make_pipeline(
            StandardScaler(),
            SVR(kernel=kernel, C=C, epsilon=epsilon)
        )
        
    def tune_model(self):
        """Tune the model using the provided data."""
        if self.model is None:
            raise ValueError("Model not set. Please set the model before tuning.")
        
        if not self.X or not self.y or len(self.X) == 0:
            raise ValueError("Training data not loaded or empty. Please load training data before tuning.")
        
        from sklearn.model_selection import GridSearchCV
        import numpy as np
        
        n_splits = min(5, len(self.X))
        if n_splits < 2:
            n_splits = 2  # Minimum for cross-validation
            
        param_grid = {
            'svr__kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'svr__C': [0.1, 1.0, 10.0],
            'svr__epsilon': [0.01, 0.1, 1.0]
        }
        
        grid_search = GridSearchCV(self.model, param_grid, cv=n_splits)
        grid_search.fit(np.array(self.X, dtype=float), np.array(self.y))
        print(f"Best parameters found: {grid_search.best_params_}")
        self.model = grid_search.best_estimator_
    
    def load_training_data(self, features, ages, scores):
        """Load training data from images and corresponding ages and scores."""
        if not features or not ages or not scores:
            raise ValueError("Features, ages, and scores must be provided.")
        
        import numpy as np
        self.X = []
        for i in range(len(features)):
            # Check if features[i] is a list or array that can be flattened
            feature_vector = np.array(features[i], dtype=float).flatten()
            # Append age as another feature
            feature_age = np.append(feature_vector, ages[i])
            self.X.append(feature_age)
        
        self.y = [score/100 for score in scores]
        
    def train(self):
        """Train the model using the loaded training data."""
        import numpy as np
        if not self.X or not self.y:
            raise ValueError("Training data not loaded. Please load training data before training.")
                
        self.model.fit(np.array(self.X, dtype=float), np.array(self.y))
        
    def predict(self, feature, age):
        """Predict the score for a given feature and age."""
        if self.model is None:
            raise ValueError("Model not set. Please set the model before predicting.")
        
        if feature is None or age is None:
            raise ValueError("Feature and age must be provided for prediction.")
        
        import numpy as np
        # Flatten the feature and append the age
        feature_vector = np.array(feature, dtype=float).flatten()
        feature_age = np.append(feature_vector, age)
        
        return self.model.predict([feature_age])[0] * 100
    
    def save_model(self, filename='model.pkl'):
        """Save the trained model to a file."""
        import pickle
        if self.model is None:
            raise ValueError("Model not set. Please set the model before saving.")
        with open(filename, 'wb') as file:
            pickle.dump(self.model, file)