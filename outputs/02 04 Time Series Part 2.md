# 📊 Time Series Part 2: Comprehensive Study Notes



### Introduction

Time series analysis is a crucial area in data science, focusing on understanding, modeling, and forecasting data points collected over time. This part of the lecture dives deeper into advanced concepts like autocorrelation, forecasting methods, time series mining, similarity measures, and representations. The goal is to equip you with a thorough understanding of how to analyze and predict time-dependent data effectively.



### 1. 📈 Time Series Forecasting (Continued)

Forecasting involves predicting future data points based on historical data. It is essential in many fields like finance, weather, and sales.

#### Key Concepts:
- **Forecasting Methods:** Techniques used to estimate future values.
- **Evaluation:** Metrics and methods to assess forecast accuracy.



### 2. 🔄 Autocorrelation Revisited

Autocorrelation measures how a data point relates to previous points in the same series. It helps identify patterns like seasonality or trends.

#### What is Autocorrelation?
- It quantifies the degree to which current values are related to past values.
- For example, today's temperature might be correlated with yesterday's temperature.

#### How to Calculate Autocorrelation:
- For a lag `k`, autocorrelation is the correlation between the series and itself shifted by `k`.
- Formula:  
  \[
  \text{ACF}(k) = \text{corr}(X_t, X_{t-k})
  \]
- **Example:**  
  If `X = [1, 2, 3, 4, 5, 6, 7, 8]`, then for lag 1, compare `[1, 2, 3, 4, 5, 6, 7]` with `[2, 3, 4, 5, 6, 7, 8]`.

#### Autocorrelation Plot (ACF):
- Visualizes autocorrelation for different lags.
- Helps identify significant lags that influence current values.

#### Partial Autocorrelation (PACF):
- Measures the direct relationship between an observation and its lag, removing the effects of intermediate lags.
- Useful for identifying the order of AR models.



### 3. 🧮 Time Series Models

Different models help forecast and understand time series data, each suited for specific patterns like trend or seasonality.

#### Traditional Univariate Models:
- **ARIMA (AutoRegressive Integrated Moving Average):** Combines autoregression, differencing, and moving averages.
- **SARIMAX:** Extends ARIMA to include seasonality and exogenous variables.
- **Prophet & Neural Prophet:** Facebook's models designed for seasonal data with holidays.
- **Neural Networks:** Deep learning models for complex patterns.

#### Multivariate Models:
- **Vector AutoRegression (VAR):** Uses multiple variables to forecast each other.

#### Machine Learning Models:
- **Neural Network Regressor, CatBoost Regressor:** Use machine learning algorithms for prediction tasks.



### 4. ⚙️ Simple Forecasting Methods

These are basic, benchmark methods used for initial predictions:
- **Average Method:** Uses the mean of past data.
- **Naive Method:** Uses the last observed value.
- **Seasonal Naive:** Uses the last seasonal value.
- **Drift Method:** Extends the trend observed in data.

*Homework:* Explore these methods further as they serve as baseline comparisons.



### 5. 🚀 Exponential Smoothing

A popular forecasting technique that weights recent observations more heavily.

#### Types:
- **Simple Exponential Smoothing (SES):** Suitable when data has no trend or seasonality.
- **Double Exponential Smoothing (Holt):** Adds trend component.
- **Triple Exponential Smoothing (Holt-Winter):** Adds seasonality.

#### How It Works:
- Prediction is a weighted sum of past observations.
- Weights decline exponentially for older data, making recent data more influential.

#### Python Implementation:
```python
import pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing

## Load data
df = pd.read_csv('airline-passengers.csv', parse_dates=['Month'], index_col='Month')
df.index.freq = 'MS'
ts = df.iloc[:, 0]

## Simple Exponential Smoothing
ses = SimpleExpSmoothing(ts).fit(smoothing_level=0.2)
ts_pred = ses.predict(start=ts.index[0], end=ts.index[-1])

## Holt's Linear Trend
holt = ExponentialSmoothing(ts, trend='add').fit(smoothing_level=0.2, smoothing_trend=0.2)
ts_trend_pred = holt.predict(start=ts.index[0], end=ts.index[-1])

## Holt-Winter's Seasonal Model
hw = ExponentialSmoothing(ts, trend='add', seasonal='mul', seasonal_periods=12).fit(smoothing_level=0.2, smoothing_trend=0.2, smoothing_seasonal=0.2)
ts_seasonal_pred = hw.predict(start=ts.index[0], end=ts.index[-1])
```



### 6. 🧠 Autoregressive (AR) Models

AR models predict current values based on past values.

#### Concept:
- The current value is a linear combination of previous `p` values.
- Equation:  
  \[
  Y_t = c + \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \dots + \phi_p Y_{t-p} + \epsilon_t
  \]
- `\(\epsilon_t\)` is white noise.

#### Example:
- AR(2): Uses the last two observations to predict the current one.

#### Python Example:
```python
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg

train, test = x[:-7], x[-7:]
model = AutoReg(train, lags=2)
model_fit = model.fit()
predictions = model_fit.predict(start=0, end=len(train)+len(test)-1, dynamic=False)
```



### 7. 🎯 Moving Average (MA) Models

MA models use past forecast errors to predict future values.

#### Concept:
- The current value depends on past white noise errors.
- Equation:  
  \[
  Y_t = \mu + \epsilon_t + \theta_1 \epsilon_{t-1} + \theta_2 \epsilon_{t-2} + \dots + \theta_q \epsilon_{t-q}
  \]

#### Relationship with AR:
- Any AR(p) can be expressed as an MA(∞) through infinite series expansion.

#### Python Example:
```python
from statsmodels.tsa.arima_model import ARMA

model = ARMA(train, order=(0, 5))
model_fit = model.fit()
predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1)
```



### 8. 🔄 ARMA, ARIMA, and SARIMA

- **ARMA:** Combines AR and MA for stationary data.
- **ARIMA:** Adds differencing (`d`) to handle non-stationary data.
- **SARIMA:** Extends ARIMA with seasonal components.

#### SARIMA Model:
- Notation: \((p, d, q)(P, D, Q)_m\)
- Example: SARIMA(2,1,3)(1,1,2)_12

#### Python Example:
```python
from pmdarima import auto_arima

model = auto_arima(train, start_p=1, start_q=1, max_p=3, max_q=3, m=12, seasonal=True, d=1, D=1, trace=True)
forecast = model.predict(n_periods=len(test))
```



### 9. ⚖️ Model Assumptions & Evaluation

- **Constant Variance:** Variance of residuals should be stable.
- **No Trend or Seasonality (for some models):** Assumed in ARMA.
- **Residual Analysis:** Use ACF, PACF, histograms to check residuals.
- **Information Criteria:** AIC and BIC help compare models; lower is better.
- **Model Selection:** Choose models balancing accuracy and simplicity.



### 10. 🧩 Time Series Mining Tasks

Mining involves extracting meaningful patterns from large time series datasets.

#### Main Tasks:
- **Indexing:** Quickly find similar sequences.
- **Clustering:** Group similar time series.
- **Classification:** Assign labels based on patterns.
- **Prediction:** Forecast future points.
- **Summarization:** Create concise descriptions.
- **Anomaly Detection:** Find unusual patterns.
- **Segmentation:** Divide series into meaningful parts.



### 11. 🔍 Time Series Similarity Measures

Similarity measures quantify how alike two time series are, crucial for tasks like clustering and indexing.

#### Common Measures:
- **Euclidean Distance:** Straight-line distance; works only if sequences are same length.
- **Lp Norms:** Generalize Euclidean (p=2) and Manhattan (p=1).
- **Dynamic Time Warping (DTW):** Handles sequences that are similar but out of phase.
- **Longest Common Subsequence (LCS):** Measures similarity based on common subsequences.
- **Probabilistic Measures:** Use statistical models to compare sequences.

#### Dynamic Time Warping (DTW):
- Aligns sequences by stretching or compressing the time axis.
- Uses dynamic programming to find the optimal alignment.
- Suitable for speech, handwriting, and other applications where timing varies.



### 12. 🧬 Time Series Representations & Compression

Representations simplify data for analysis, while compression reduces storage needs.

#### Techniques:
- **Delta Encoding:** Stores differences between consecutive points.
- **Run-Length Encoding (RLE):** Compresses repeated values.
- **Dimensionality Reduction:** Techniques like PCA to reduce data dimensions.



### 13. 🔢 Matrix Profile & Motifs

**Matrix Profile** is a powerful data structure for time series mining, enabling fast motif discovery, anomaly detection, and more.

#### What is Matrix Profile?
- Stores the distance to the nearest neighbor for each subsequence.
- Helps identify:
  - **Motifs:** Repeated patterns.
  - **Discords:** Anomalies or unusual patterns.
  - **Anomalies:** Outliers in data.

#### Example:
- A high distance value indicates an anomaly.
- Repeated low-distance patterns suggest motifs.



### 14. 🧩 Summary & Additional Resources

- **Time series analysis** involves modeling, forecasting, and mining data collected over time.
- **Forecasting models** range from simple averages to complex ARIMA/SARIMA.
- **Similarity measures** like DTW are essential for pattern matching.
- **Matrix Profile** offers a scalable way to find motifs and anomalies.
- **Practical tools** include Python libraries like `statsmodels`, `pmdarima`, and visualization tools.

**Further Reading:**
- Section 3.5 of the referenced material for indexing.
- Book chapters on Time Series Mining.
- NeuralProphet for advanced neural network-based forecasting.



### Final Notes

Understanding these concepts provides a solid foundation for analyzing time series data effectively. Practice implementing these models and measures with real datasets to gain hands-on experience. Remember, choosing the right model depends on data characteristics like stationarity, seasonality, and noise.



**Happy analyzing!** 😊