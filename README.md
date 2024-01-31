# Hotel Reservation Cancellation Analysis

This repository contains an analysis of hotel reservation data with the goal of predicting the probability of a reservation being cancelled. The analysis aims to help businesses in the hotel industry optimize their revenue and make informed decisions regarding pricing and occupancy.

## Objective

The objective of this analysis is to develop predictive models using machine learning algorithms to determine the likelihood of a hotel reservation being cancelled. By accurately predicting cancellations, businesses can adjust their pricing strategies and promotional efforts to maximize revenue and achieve their occupancy goals. The models will be evaluated based on their accuracy and precision.

## Data and Process

The dataset used for this analysis consists of hotel reservation records gathered from a booking engine. Before conducting the analysis, the data has been anonymized to ensure the privacy of customers.

This analysis is conducted using Python programming language and various libraries. The code is divided into two separate files: a .py file for the Python code and an .ipynb file for the Jupyter Notebook containing the analysis steps. The results and findings are documented in a PDF report.

## Conclusions

The primary goal of this analysis was to predict the probability of reservation cancellations using machine learning models. The dataset provided consisted of 391,579 records, with a significant class imbalance. The majority of reservations (79%) were not cancelled, while 21% were cancelled. This class imbalance may impact the learning of our models, particularly when identifying cancellation patterns.

The analysis revealed limitations and risks associated with the models:

- The dataset covers a period from 2019 to 2023, which includes the impact of the Covid-19 pandemic. The pandemic caused a significant increase in cancellation rates, making it challenging to identify consistent cancellation patterns.
- The unpredictability of external events, such as mass cancellations due to unforeseen incidents, poses a challenge for our models. Although these events follow a clear pattern in the dataset, their occurrence is inherently unpredictable, which may affect the effectiveness of our models in future data.

Despite these limitations, the Random Forest Classifier model performed the best among the tested models. However, its precision and accuracy were still relatively low, indicating the need for further improvements.

To enhance the performance of future models, the following recommendations are suggested:

1. Training the model using incremental data starting from 2019 and progressing towards more recent years.
2. Incorporating additional variables such as the day of the week or month of the reservation while excluding exact dates to avoid overfitting.
3. Reducing the dimensionality of the dataset by removing irrelevant columns that do not contribute to the predictive power of the model.

## Usage

To replicate this analysis, follow these steps:

1. Clone this repository to your local machine.
2. Install the required Python libraries specified in the `.py` file.
3. Run the `.py` file to preprocess the data and prepare it for analysis.
4. Open the `.ipynb` file in Jupyter Notebook or any compatible environment to run the analysis steps.
5. Review the PDF report for detailed insights and conclusions.

Please note that the dataset used in this analysis has been anonymized and is not publicly available.
