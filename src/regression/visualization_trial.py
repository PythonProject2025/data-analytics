import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
    
def regression_plot(x, y, x_label, y_label, data=None, ax=None):
    if ax is None:
        ax = plt.gca()
        plt.figure(figsize=(10, 6), dpi=600)  # Adjust size and set DPI
    sns.regplot(
        x=x, y=y, data=None, ax=ax,
        scatter_kws={"s": 60, "alpha": 0.8},  # Customize scatter points
        line_kws={"color": "crimson", "lw": 2},  # Customize regression line
    )
    for patch in ax.collections:
        patch.set_alpha(0.5)  # Darkens the shaded portion
    ax.set_xlabel(x_label, fontsize=12, weight='bold')
    ax.set_ylabel(y_label, fontsize=12, weight='bold')
    ax.set_title('Linear Regression Fit', fontsize=14, weight='bold') 
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)    
    
def residual_plot(x, y, ax=None):
    if ax is None:
        ax = plt.gca()
        plt.figure(figsize=(10, 6), dpi=600)  # Adjust size and set DPI
    sns.residplot(
        x=x, y=y, scatter_kws={"s": 60, "alpha": 0.8}, ax=ax,
        color="teal"
    )
    ax.set_title('Residual Plot', fontsize=14, weight='bold')
    ax.set_xlabel('Predicted Values', fontsize=12, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
def polynomial_plot(x_scatter, y_scatter, y_poly, x_label, y_label, degree):
    # Set figure size and seaborn style
    plt.figure(figsize=(12, 7), dpi=120)
    sns.set_theme(style="ticks")  # Clean and modern theme
    
    # Scatter plot for actual data
    sns.scatterplot(
        x=x_scatter, y=y_scatter,
        color='#1f77b4',  # Matplotlib's default blue
        label='Actual Data', s=100, alpha=0.9,
        edgecolor='black', linewidth=0.7
    )
    
    # Line plot for polynomial regression
    sns.lineplot(
        x=x_scatter, y=y_poly,
        color='#ff5733',  # Vibrant orange-red
        label='Polynomial Regression Line',
        linewidth=2.5
    )
    
    # Add labels and title with better styling
    plt.xlabel(x_label, fontsize=14, weight='semibold', labelpad=12)
    plt.ylabel(y_label, fontsize=14, weight='semibold', labelpad=12)
    plt.title(
        f'Polynomial Regression Fit (Degree: {degree})', fontsize=16, weight='bold', pad=20, loc='center',
        color='#333333'  # Dark gray title color
    )
    
    # Legend styling - fixed at lower left corner
    plt.legend(
        fontsize=12, loc='lower left', frameon=True, shadow=False,
        fancybox=True, borderpad=1, framealpha=0.9
    )
    
    # Customize the grid and spines
    plt.grid(
        which='major', linestyle='--', linewidth=0.6, color='gray', alpha=0.7
    )
    plt.minorticks_on()
    plt.tick_params(
        which='both', direction='in', length=6, width=1, colors='black',
        grid_alpha=0.5
    )
    sns.despine(top=True, right=True)  # Remove top and right spines
    
    # Tight layout for better spacing
    plt.tight_layout()
    plt.show()    

def ridge_plot(results_ridge,best_params):
    # Extract the relevant results
#    results = data.results_ridge
#    best_degree_mask = (results['param_polynomial_features__degree'] == data.best_degree_ridge)
#    alphas = results['param_ridge_regression__alpha'][best_degree_mask]
#    mean_scores = results['mean_test_score'][best_degree_mask]

#    results = data.results_ridge
    best_degree_mask = (results_ridge['param_polynomial_features__degree'] == best_params['best_degree_ridge'])
    alphas = results_ridge['param_ridge_regression__alpha'][best_degree_mask]
    mean_scores = results_ridge['mean_test_score'][best_degree_mask]

    # Set the figure size and style
    plt.figure(figsize=(10, 6), dpi=120)
    sns.set_theme(style="whitegrid")  # Clean background with gridlines
    
    # Plot the lineplot
    sns.lineplot(
    x=alphas, y=mean_scores,
    marker='o', linestyle='-', color='#1f77b4',  # Line color and marker style
    label=f'Best Degree = {best_params["best_degree_ridge"]}\nBest Alpha = {best_params["best_alpha_ridge"]}', 
    linewidth=2.5, markersize=8
)
    
    # Add labels and title with improved styling
    plt.xlabel('Alpha (Regularization Strength)', fontsize=14, weight='bold', labelpad=15)
    plt.ylabel('Cross-Validation Score (R2 Score)', fontsize=14, weight='bold', labelpad=15)
    plt.title('Alpha vs Model Performance (Ridge Regression)', fontsize=16, weight='bold', pad=20)
    
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.gca().yaxis.get_offset_text().set_visible(False)
    
    # Customize the legend
    plt.legend(
        fontsize=12, loc='center right', frameon=True, fancybox=True, shadow=True, borderpad=1
    )
    
    # Add gridlines and customize tick params
    plt.grid(which='major', linestyle='--', linewidth=0.7, color='gray', alpha=0.7)
    plt.minorticks_on()
    plt.tick_params(
        which='both', direction='in', length=6, width=1, colors='black', grid_alpha=0.5
    )
    
    # Remove top and right spines for a clean look
    sns.despine(top=True, right=True)
    
    # Ensure the plot looks neat with tight layout
    plt.tight_layout()
    plt.show()
    
def lasso_plot(results_lasso,best_params):
    # Extract the relevant results
#    results = data.results_lasso
#    best_degree_mask = (results['param_polynomial_features__degree'] == data.best_degree_lasso)
#    alphas = results['param_lasso_regression__alpha'][best_degree_mask]
#    mean_scores = results['mean_test_score'][best_degree_mask]

    best_degree_mask = (results_lasso['param_polynomial_features__degree'] == best_params['best_degree_lasso'])
    alphas = results_lasso['param_lasso_regression__alpha'][best_degree_mask]
    mean_scores = results_lasso['mean_test_score'][best_degree_mask]

    # Set the figure size and style
    plt.figure(figsize=(10, 6), dpi=120)
    sns.set_theme(style="whitegrid")  # Clean background with gridlines
    
    # Plot the lineplot
    sns.lineplot(
        x=alphas, y=mean_scores,
        marker='o', linestyle='-', color='#e74c3c',  # Line color and marker style
        label=f'Best Degree = {best_params["best_degree_lasso"]}\nBest Alpha = {best_params["best_alpha_lasso"]}', 
        linewidth=2.5, markersize=8
    )
    
    # Add labels and title with improved styling
    plt.xlabel('Alpha (Regularization Strength)', fontsize=14, weight='bold', labelpad=15)
    plt.ylabel('Cross-Validation Score (R2 Score)', fontsize=14, weight='bold', labelpad=15)
    plt.title('Alpha vs Model Performance (Lasso Regression)', fontsize=16, weight='bold', pad=20)
    
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.gca().yaxis.get_offset_text().set_visible(False)
    
    # Customize the legend to remove the line
    plt.legend(
        fontsize=12, loc='upper left', frameon=True, fancybox=True, shadow=True, borderpad=1, handlelength=0
    )
    
    # Add gridlines and customize tick params
    plt.grid(which='major', linestyle='--', linewidth=0.7, color='gray', alpha=0.7)
    plt.minorticks_on()
    plt.tick_params(
        which='both', direction='in', length=6, width=1, colors='black', grid_alpha=0.5
    )
    
    # Remove top and right spines for a clean look
    sns.despine(top=True, right=True)
    
    # Ensure the plot looks neat with tight layout
    plt.tight_layout()
    plt.show()