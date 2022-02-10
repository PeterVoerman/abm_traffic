import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

br_params = {
    "max_speed": [90, 95, 100, 105, 110, 115, 120, 125, 130],
    "braking_chance": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "n_cars": [50, 75, 100, 125, 150, 175, 200, 225, 250],
    "sigma_pref_speed": [0, 0.05, 0.1, 0.15, 0.2, 0.25],
}

title_list = ["maximum speeds", "braking chances", "amounts of cars", "standard deviations of preferred speeds"]
xlabel_list = ["Maximum speed (km/h)", "Braking chance", "Amount of cars", "Standard deviation of preferred speeds (sigma * max_speed)"]

data = {}

for param in br_params:
    df = pd.read_csv(f"data/{param}.csv")
    data[param] = df

def plot_param_var_conf(df, var, param, i):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        var: variables to be taken from the dataframe
        param: which output variable to plot
    """
    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    plt.plot(x, y, c='k')
    plt.fill_between(x, y - err, y + err)

    plt.xlabel(xlabel_list[i])
    plt.ylabel("Average speed (km/h)")
    plt.title(f"Average speed for various {title_list[i]}")
    plt.show()

def plot_all_vars(df, param):
    """
    Plots the parameters passed vs each of the output variables.

    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """

    #f, axs = plt.subplots(4, figsize=(7, 10))
    
    for i, var in enumerate(br_params):
        plot_param_var_conf(data[var], var, param, i)


plot_all_vars(data, "Avg Speed")
