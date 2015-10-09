import numpy as np
import pandas as pd
from ggplot import *
import traceback

path = "C:/Users/kuligin/Downloads/turnstile_data_master_with_weather.csv"

def normalize_features(df):
	#Normalize the features in the data set.
	try:
		mu = df.mean()
		sigma = df.std()
		df_normalized = (df - df.mean()) / df.std()
		if (sigma == 0).any():
			raise Exception("Features with single value exists")
		return df_normalized, mu, sigma
	except:
		print "error: ", traceback.format_exc()


def compute_cost(features, values, theta):
	return np.square(np.dot(features, theta)-values).sum() / (2*len(values))

def gradient_descent(features, values, theta, alpha, num_iterations):
	m = len(values)
	cost_history = []
	for i in range(num_iterations):
		new_val = np.dot(features, theta)
		theta = theta - alpha/m * np.dot((new_val-values), features)
		cost = compute_cost(features, values, theta)
		cost_history.append(cost)
	return theta, pd.Series(cost_history)

def predictions(dataframe):
	# the complete turnstile weather dataframe can be downloaded hear:https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
	features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']]
	# Add UNIT to features using dummy variables
	dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
	features = features.join(dummy_units)
	values = dataframe['ENTRIESn_hourly']
	m = len(values)

	features, mu, sigma = normalize_features(features)
	features['ones'] = np.ones(m) # Add a column of 1s (y intercept)
	# Convert features and values to numpy arrays
	features_array = np.array(features)
	values_array = np.array(values)

	# Set values for alpha, number of iterations.
	alpha = 0.1
	num_iterations = 75
	
	# Initialize theta, perform gradient descent
	theta_gradient_descent = np.zeros(len(features.columns))
	theta_gradient_descent, cost_history = gradient_descent(features_array, 
	values_array, theta_gradient_descent, alpha, num_iterations)

	plot = None
	plot = plot_cost_history(alpha, cost_history)
	predictions = np.dot(features_array, theta_gradient_descent)
	return predictions, plot

def plot_cost_history(alpha, cost_history):
	cost_df = pd.DataFrame({
	'Cost_History': cost_history,
	'Iteration': range(len(cost_history))
	})
	return ggplot(cost_df, aes('Iteration', 'Cost_History')) + \
	geom_point() + ggtitle('Cost History for alpha = %.3f' % alpha )

def plot_residuals(turnstile_weather, predictions):
	plt.figure()
	(turnstile_weather['ENTRIESn_hourly'] - predictions).hist()
	return plt

def compute_r_squared(data, predictions):
	return 1- ((predictions-data)**2).sum() / ((data-data.mean())**2).sum()

if __name__ == "__main__":
	data = pd.read_csv(path)
	data = pd.DataFrame(data)
	predictions, plt = predictions(data)
	print plt
	ggsave(filename="cost_hist.jpg", width=4, height=4, units='in', plot=plt)
	#plot.show()
