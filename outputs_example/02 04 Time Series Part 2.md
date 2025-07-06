# 📊 Time Series Part 2: Comprehensive Study Notes



### Introduction

Time series analysis involves examining data points collected or recorded at successive points in time. This field is crucial for understanding patterns, making predictions, and discovering insights in data that change over time—like stock prices, weather data, or sales figures. This study note covers advanced concepts in time series forecasting, mining, and similarity measures, building on foundational knowledge to help you understand how to analyze, model, and extract meaningful information from time series data.



### 1. 🕰️ Time Series Forecasting (Continued)

Forecasting is about predicting future values based on historical data. It involves selecting appropriate models that capture the underlying patterns like trends, seasonality, and autocorrelation.

#### Autocorrelation Revisited

Autocorrelation measures how current data points relate to past data points. It helps identify repeating patterns or dependencies over time. For example, today's temperature might be correlated with yesterday's temperature.

- **Autocorrelation Function (ACF):** Shows the correlation between observations at different lags (time steps apart). It helps identify the presence of autocorrelation at various lags.
- **How to calculate ACF:** For a lag `k`, compute the correlation between the original series `X` and the series shifted by `k` steps (`Xlagk`). This is done using the correlation coefficient formula.

#### Partial Autocorrelation (PACF)

PACF measures the direct relationship between an observation and its lag, removing the influence of intermediate lags. It helps determine the order of autoregressive models (AR).

- **How to compute PACF:** Fit a linear regression of `Xt` on its previous `p` lags and examine the coefficient for each lag. The PACF at lag `k` indicates the direct effect of `Xt` on `Xt-k`.



### 2. 🧮 Traditional Time Series Models

These models are fundamental for forecasting and understanding time series data.

#### Univariate Models

- **ARIMA (AutoRegressive Integrated Moving Average):** Combines autoregression, differencing (to make data stationary), and moving averages.
- **SARIMAX:** Extends ARIMA to include seasonal effects and exogenous variables.
- **Prophet & Neural Prophet:** Facebook-developed models that handle seasonality and holidays effectively.
- **Simple Forecasting Methods:** Basic approaches like average, naive, seasonal naive, and drift methods serve as benchmarks.

#### Exponential Smoothing

A popular method that weights recent observations more heavily, suitable for data without strong trends or seasonality.

- **Simple Exponential Smoothing (SES):** Uses a smoothing level parameter to weigh recent data.
- **Double Exponential Smoothing (Holt):** Adds a trend component.
- **Triple Exponential Smoothing (Holt-Winters):** Adds seasonality adjustment.

**Python Example:**

```python
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

## Load data
df = pd.read_csv('airline-passengers.csv', parse_dates=['Month'], index_col='Month')
df.index.freq = 'MS'
ts = df.iloc[:, 0]

## Simple Exponential Smoothing
ses = SimpleExpSmoothing(ts).fit(smoothing_level=0.2)
ts_pred = ses.predict(start=ts.index[0], end=ts.index[-1])

## Holt-Winters (additive trend, seasonal)
hw = ExponentialSmoothing(ts, trend='add', seasonal='mul', seasonal_periods=12).fit()
ts_hw_pred = hw.predict(start=ts.index[0], end=ts.index[-1])
```



### 3. 🧠 Autoregressive and Moving Average Models

#### Autoregressive (AR) Model

- Uses past values of the series to predict future values.
- **AR(p):** The current value depends linearly on `p` previous values plus noise.

**Equation:**

\[ Y_t = c + \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \dots + \phi_p Y_{t-p} + \epsilon_t \]

- **Python Example:**

```python
from statsmodels.tsa.ar_model import AutoReg

model = AutoReg(train_data, lags=2)
model_fit = model.fit()
predictions = model_fit.predict(start=0, end=len(test_data)-1)
```

#### Moving Average (MA) Model

- Uses past forecast errors to model the series.
- **MA(q):** The current value depends on the past `q` errors.

**Equation:**

\[ Y_t = \mu + \epsilon_t + \theta_1 \epsilon_{t-1} + \theta_2 \epsilon_{t-2} + \dots + \theta_q \epsilon_{t-q} \]

- **Note:** Any stationary AR model can be expressed as an MA model of infinite order (MA(∞)).

#### ARMA and ARIMA

- **ARMA:** Combines AR and MA models for stationary data.
- **ARIMA:** Adds differencing to handle non-stationary data.
- **SARIMA:** Extends ARIMA with seasonal components.

**Model Fitting:**

```python
from statsmodels.tsa.arima_model import ARMA

model = ARMA(train_data, order=(p, q))
model_fit = model.fit()
```

#### SARIMA Example:

```python
from pmdarima import auto_arima

model = auto_arima(train, start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                   seasonal=True, d=1, D=1, trace=True)
model.fit(train)
forecast = model.predict(n_periods=len(test))
```



### 4. 🧪 Model Evaluation & Selection

Choosing the best model involves comparing their performance using metrics like:

- **AIC/BIC:** Penalize model complexity; lower values are better.
- **Residual Analysis:** Check residuals for randomness using ACF, PACF, histograms.
- **Error Metrics:** RMSE, MAE, MAPE on validation/test data.

**Visualization:** Plot residuals and autocorrelation to verify assumptions.



### 5. 🔍 Time Series Mining Tasks

Mining involves extracting patterns, similarities, and anomalies from large time series datasets.

#### Key Tasks:

- **Indexing:** Efficiently querying similar sequences.
- **Clustering:** Grouping similar time series.
- **Classification:** Assigning labels based on patterns.
- **Prediction:** Forecasting future data points.
- **Summarization:** Creating concise representations.
- **Anomaly Detection:** Finding unusual patterns or outliers.
- **Segmentation:** Dividing series into meaningful parts.



### 6. 🔎 Time Series Similarity Measures

Similarity measures quantify how alike two time series are, crucial for clustering, indexing, and anomaly detection.

#### Common Measures:

- **Euclidean Distance:** Straight-line distance; works best when sequences are aligned and of equal length.
- **Lp Norms:** Generalize Euclidean (p=2) and Manhattan (p=1) distances.
- **Dynamic Time Warping (DTW):** Handles sequences that are similar in shape but out of phase; allows stretching/compression along the time axis.
- **Longest Common Subsequence (LCSS):** Finds the longest matching subsequence, tolerant to noise.
- **Probabilistic Measures:** Use statistical models to compare sequences.

**DTW Example:**

```python
import numpy as np
from dtw import dtw

distance, path = dtw(series1, series2, keep_internals=True)
```



### 7. 🧩 Time Series Representations & Compression

Representing time series efficiently reduces storage and speeds up analysis.

#### Techniques:

- **Dimensionality Reduction:** Techniques like PCA or SAX (Symbolic Aggregate approXimation).
- **Delta Encoding:** Stores differences between consecutive points.
- **Run-Length Encoding (RLE):** Compresses consecutive repeated values.
- **Other methods:** Wavelet transforms, Fourier transforms.



### 8. 🔍 Motifs, Anomalies, and Matrix Profile

#### Motifs & Anomalies

- **Motifs:** Repeated patterns within the data.
- **Anomalies (Discords):** Unusual patterns that differ significantly from the rest.
- **Matrix Profile:** A data structure that efficiently finds motifs and discords.

#### Matrix Profile

- **Concept:** Stores the distance to the nearest neighbor for each subsequence.
- **Advantages:** Fast, scalable, and domain-agnostic.
- **Application:** Detecting anomalies, motifs, and repeated patterns.

**Example:**

- Large distances in the matrix profile indicate anomalies.
- Repeated low-distance regions suggest motifs.



### 9. 📝 Summary & Additional Resources

This overview covers advanced techniques for analyzing, modeling, and mining time series data. Key takeaways include understanding autocorrelation, selecting appropriate models (ARIMA, SARIMA, exponential smoothing), and leveraging similarity measures like DTW. The matrix profile is a powerful tool for motif and anomaly detection.

**Further Reading:**

- "Time Series Mining" chapters in data mining textbooks.
- Abdullah Mueen and Eamonn Keogh's work on matrix profiles.
- NeuralProphet for deep learning-based forecasting.



### Final Tips

- Always visualize your data before modeling.
- Use residual analysis to validate assumptions.
- Compare multiple models with error metrics and information criteria.
- Leverage similarity measures for efficient indexing and anomaly detection.
- Keep in mind the domain context to interpret patterns meaningfully.



**End of Study Notes**

Feel free to ask for clarifications or specific examples!