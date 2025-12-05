# Churn Prediction ML Project



A machine learning project to predict customer churn using classification algorithms. Includes data preprocessing, model training, and an interactive dashboard for predictions.



## Features

\* Data preprocessing and feature engineering

\* Multiple ML models (Logistic Regression, Random Forest, XGBoost, Neural Networks)

\* Model evaluation (accuracy, precision, recall, F1-score)

\* Interactive Dash dashboard for visualization and real-time predictions



## Installation



1\. Clone the repo:

```

git clone https://github.com/arijbelmabrouk/ChurnPrediction.git

cd ChurnPrediction

```



2\. Create a virtual environment:

```

python -m venv venv

source venv/bin/activate  # Windows: venv\\Scripts\\activate

```



3\. Install dependencies:

```

pip install -r requirements.txt

```



## Usage



\* Run the main app:

```

python app.py

```



\* Run the dashboard:

```

python dash.py

```



\* Train models:

```

jupyter notebook data\_preperation\_VF01.ipynb

```



Models are saved in `models/` but not included in the repo.



## Project Structure

```

ChurnPrediction/

├── app.py

├── dash.py

├── data\_preperation\_VF01.ipynb

├── requirements.txt

├── .gitignore

├── models/          # Trained models (not tracked)

└── README.md

```



## Dataset



Dataset is not included. Use your own CSV with customer features and a churn label.



## Contributing



1\. Fork the repo

2\. Create a branch: `git checkout -b feature/AmazingFeature`

3\. Commit: `git commit -m "Add feature"`

4\. Push: `git push origin feature/AmazingFeature`

5\. Open a Pull Request



## License



MIT License. See `LICENSE` for details.



## Author



Arij Belmabrouk – \[GitHub](https://github.com/arijbelmabrouk)

