
import pandas as pd
import time
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from scipy.stats import randint
import pickle

# Step 1: Load Dataset
try:
    df = pd.read_csv("Loan_default_dataset.csv")
    print(f"Dataset loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
except FileNotFoundError:
    print("Error: File not found. Make sure 'Loan_default_dataset.csv' is in the same directory.")
    exit()

# Step 2: Define Target & Features
TARGET = 'Default' #Target
DROP_COLS = ['LoanID', 'Loan Date (DD/MM/YYYY)', TARGET] #Drop columns

y = df[TARGET]
X = df.drop(columns=DROP_COLS)

# Step 3: Define Feature Groups
numerical_features = [
    'Age', 'Income', 'LoanAmount', 'CreditScore', 'MonthsEmployed', #Numerical Columns
    'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio'
]

categorical_features = [
    'Education', 'EmploymentType', 'MaritalStatus', 'HasMortgage', #Categorical Columns
    'HasDependents', 'LoanPurpose', 'HasCoSigner'
]

# Step 4: Preprocessing Pipeline
numeric_transformer = Pipeline(steps=[
    ('scaler', MinMaxScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='drop'
)

# Step 5: Full Pipeline with Feature Selection + Model
base_rf = RandomForestClassifier(random_state=42, class_weight='balanced', n_jobs=-1)

full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('feature_select', SelectFromModel(base_rf, threshold='median')),
    ('classifier', base_rf)
])

# Step 6: Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Data split into {X_train.shape[0]} training and {X_test.shape[0]} testing records.")

# Step 7: RandomizedSearch for Faster Hyperparameter Tuning
param_distributions = {
    'classifier__n_estimators': randint(100, 300),
    'classifier__max_depth': randint(8, 25),
    'classifier__min_samples_split': randint(2, 10),
    'classifier__min_samples_leaf': randint(1, 6),
    'classifier__max_features': ['sqrt', 'log2']
}

search = RandomizedSearchCV(
    full_pipeline,
    param_distributions=param_distributions,
    n_iter=10,  
    cv=3,
    n_jobs=-1,
    random_state=42,
    scoring='accuracy',
    verbose=2
)

print("\nStarting Randomized Search...")
start_time = time.time()
search.fit(X_train, y_train)
print(f"Randomized Search completed in {(time.time() - start_time) / 60:.2f} minutes.")

print("\nBest Parameters:")
print(search.best_params_)
print(f"Best CV Accuracy: {search.best_score_:.4f}")

# Step 8: Retrain Final Model
final_model = search.best_estimator_

print("\nTraining final model on full training data...")
start_full = time.time()
final_model.fit(X_train, y_train)
print(f"Final model trained in {(time.time() - start_full) / 60:.2f} minutes.")

# Step 9: Evaluate
y_pred = final_model.predict(X_test)

print("\nModel Evaluation:")
print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Step 10: Save Model
with open('loan_default_pipeline.pkl', 'wb') as file:
    pickle.dump(final_model, file)

print("\nModel saved as 'loan_default_pipeline.pkl'.")