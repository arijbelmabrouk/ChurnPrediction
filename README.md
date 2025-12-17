Arij Belmabrouk – \[GitHub](https://github.com/arijbelmabrouk)

# Convex Optimization for Churn Classification

Implements regularized logistic loss minimization across solvers: L-BFGS (quasi-Newton), SGD (stochastic gradient), Coordinate Descent (liblinear L1 sparsity). Complements tree ensembles with convergence analysis.

## Mathematical Formulation

$$\min_{\mathbf{w}} \mathcal{L}(\mathbf{w}) = -\frac{1}{N}\sum_{i=1}^N \left[ y_i \log \sigma(\mathbf{x}_i^T\mathbf{w}) + (1-y_i)\log(1-\sigma(\mathbf{x}_i^T\mathbf{w})) \right] + \lambda \|\mathbf{w}\|_p$$

where $\sigma(z) = (1+e^{-z})^{-1}$, $p\in\{1,2\}$ controls Lasso/Ridge regularization.

**Solver Trade-offs:**
- L-BFGS: $O(n)$ Hessian approximation, fastest smooth convergence
- SGD: Scales to $10^6$ samples, requires momentum for stability  
- Coordinate Descent: Native L1 sparsity, linear convergence guarantees

## Hyperparameter Optimization

Bayesian Optimization (Gaussian Process surrogate) vs Grid Search: 67 evaluations vs $10^4$ grid points.

## Project Structure

ChurnPrediction/
├── data_preparation_VF01.ipynb # Preprocess → Optimize → Evaluate
├── app.py # Prediction API
├── dash.py # Visualization dashboard
├── requirements.txt
├── results/ # Loss curves, convergence plots
└── models/ # Trained weights (gitignore)

text

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


