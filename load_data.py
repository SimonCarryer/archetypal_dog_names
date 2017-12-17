import pandas as pd

to_replace = ['LAB', 'SHEPHERD', 'AM ESKIMO DOG', 'COLLIE', 
			'POODLE', 'MASTIFF', 'GOLDEN RETRIEV', 'YORKSHIRE TERR']
replacements = ['LABRADOR RETRIEVER', 'GER SHEPHERD', 'AM SPITZ', 
				'BORD COLLIE', 'POODLE STANDARD', 'ENGLISH MASTIFF', 'GOLDEN RETRIEVER',
				'YORKSHIRE TERRIER']


def load_dog_data(path_to_csvs='../dog_name_data/'):
	years = [pd.read_csv('%s%d.csv' % (path_to_csvs, year)) for year in range(2007, 2018)]
	df = pd.concat(years)
	df.DogName = df.DogName.apply(str.upper)
	df['breed_no_mix'] = df.Breed.str.rstrip(' MIX')
	df['breed_no_mix'] = df.breed_no_mix.replace(to_replace, replacements)
	return df
	
def get_main_breeds_df(df, breed_threshold=500, name_threshold=100):
	breed_counts = df.groupby('breed_no_mix')['DogName'].count()
	name_counts = df.groupby('DogName')['breed_no_mix'].count()
	main_breeds = df[(df.breed_no_mix.map(breed_counts.to_dict()) >= breed_threshold) 
	                 & ~(df.Breed.isin(['MIXED', 'OTHER']))
	                & (df.DogName.map(name_counts.to_dict()) >= name_threshold)]
	return main_breeds