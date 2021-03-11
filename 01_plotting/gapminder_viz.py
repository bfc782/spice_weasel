#%%
#files saved in the data_path are sourced by World Banks via https://www.gapminder.org/data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import imageio

DATA_CREDIT = 'FREE TO USE! CC-BY GAPMINDER.ORG'

data_path = 'data/'
file_cont = data_path + 'continents.csv'
file_life = data_path + 'gapminder_lifeexpectancy.xlsx'
file_popn = data_path + 'gapminder_population.xlsx'
file_fert = data_path + 'gapminder_total_fertility.csv'

df_cont = pd.read_csv(file_cont, sep=";")
df_life = pd.read_excel(file_life, index_col=0)
df_popn = pd.read_excel(file_popn, index_col=0)
df_fert = pd.read_csv(file_fert, sep=",", index_col=0)

#Melting the DFs
df_fert.index.name = 'country'
df_fert = df_fert.reset_index()
df_fert = df_fert.melt(id_vars='country', var_name='year', value_name = 'fertility_rate')

df_popn.index.name = 'country'
df_popn = df_popn.reset_index()
df_popn = df_popn.melt(id_vars='country', var_name='year', value_name='population')

df_life.index.name = 'country'
df_life = df_life.reset_index()
df_life = df_life.melt(id_vars='country', var_name='year', value_name='life_expect')

#Building on df_life: 
##Filtering data for coincident years: life & fert
years_coinc = set(df_life[df_life['year'].isin(df_fert['year'])]['year'])

##Merging life with fert
df_fert = df_fert.astype({'year':'int64'}) #merge requires same data type on both 'years' column
df_life_fert = df_life.merge(df_fert,on=['country','year'])

##Merging life_fert with population
df_life_fert_popn = df_life_fert.merge(df_popn,on=['country','year'])

##Merging with cont - this is a modern country->continent mapping and thus removes the old names from the output
df_life_fert_popn_cont = df_life_fert_popn.merge(df_cont,on=['country'])

#Dropping ALL data rows that feature NaNs (no imputation happening here!)
df_plot = df_life_fert_popn_cont.dropna()

#Plotting line for some countries
#sns.set()
#some = ['France', 'Germany', 'Sweden']
#df_subset = df_plot.loc[df_plot['country'].isin(some)]
#sns.lineplot(x='year', y='life_expect', hue='country', data=df_subset)
#plt.show()

#%%
earliest = df_plot['year'].min()
latest = earliest
#latest = df_plot['year'].max()

#Colouring the continents, using one year to match country data points (not duplicating)
list_conts = ['Africa','Asia','Australia and Oceania','Europe','North America','South America']
list_cols = ['g','y','m','b','r','c']
cont_cols = df_plot[df_plot['year']==earliest]['continent'].replace(list_conts,list_cols)
#%%
j=0
for i in range(earliest, latest):
    plt.axis((20,85,0,9))
    plt.title('life expectancy vs fertility rate', loc='left')
    plt.title(f'year: {i}', loc='right')
    plt.xlabel('life expectancy in years')
    plt.ylabel('fertility rate')
    plot_test = df_plot[df_plot['year']==i]
    
    if plot_test.empty:
        j+=1
        plot = df_plot[df_plot['year']==i-j]
    else:
        j=0
        plot = df_plot[df_plot['year']==i]

    plt.scatter(plot['life_expect'],plot['fertility_rate'], s=plot['population']//1000000, c=cont_cols, alpha=0.9-(j/10))
    plt.savefig(f'./plots/life_fert{i}.png')
    plt.close() 
#%%
images = []
for i in range(earliest,latest):
    filename = f'./plots/life_fert{i}.png'
    images.append(imageio.imread(filename))
imageio.mimsave(f'./life_fert_from_{earliest}-{latest}.gif', images, fps=5)

