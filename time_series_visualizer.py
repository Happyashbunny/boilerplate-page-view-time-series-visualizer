import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col= 'date', parse_dates=True)

# Clean data
lower_quantile = df['value'].quantile(0.025)
upper_quantile = df['value'].quantile(0.975)


df = df[(df['value'] >= lower_quantile) & (df['value'] <= upper_quantile)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize =(15,6))
    ax.plot(df.index, df['value'], df, color = 'red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Draw bar plot
    df_bar.reset_index(inplace=True)
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.month_name()

    
    df_bar_pivot = df_bar.pivot_table(index='year', columns='month', values='value', aggfunc='mean')
    
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    df_bar_pivot = df_bar_pivot.reindex(columns=months_order)

    fig, ax = plt.subplots(figsize=(10, 8))
    df_bar_pivot.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')
    



    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month_order'] = pd.Categorical(df_box['month'], categories=months_order, ordered=True)

    # Create the box plot
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
    sns.boxplot(x='year', y='value',hue='year', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month_order', y='value', hue='month_order',  data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
