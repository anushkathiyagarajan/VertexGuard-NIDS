import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


print("Loading dataset...")

# Load UNSW dataset
train = pd.read_csv("dataset/UNSW_NB15_training-set.csv")

print("Dataset loaded successfully!")


# Remove useless column if exists
if "num_outbound_cmds" in train.columns:
    train.drop("num_outbound_cmds", axis=1, inplace=True)


# Detect target column
if "label" in train.columns:
    target = "label"
elif "class" in train.columns:
    target = "class"
else:
    raise Exception("Target column not found")


# Separate features and label
X = train.drop(target, axis=1)
y = train[target]


# Remove attack category column (only used for display later)
if "attack_cat" in X.columns:
    X = X.drop("attack_cat", axis=1)


print("Encoding categorical columns...")

# Encode categorical columns
for column in X.columns:
    if X[column].dtype == "object":
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column])


print("Splitting dataset...")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)


print("Training IDS model using Random Forest algorithm...")

# Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

print("Model trained successfully using Random Forest!")


print("Testing model...")

# Test model
pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("Model Accuracy:", accuracy)


# Save trained model
joblib.dump(model, "ids_model.pkl")

print("Model saved as ids_model.pkl")