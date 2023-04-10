import pandas as pd

# read in files
gisaid_metadata = pd.read_csv('~/Downloads/wa-sequences.tsv', sep='\t', index_col=['Virus name'])
doh_metadata = pd.read_csv('~/PycharmProjects/scripts/data/metadata_2023-04-07.csv')

# rename county column
doh_metadata = doh_metadata.rename(columns={'COUNTY_NAME': 'County',
                                            'SEQUENCE_ACCESSION_NUMBER': 'Virus name'})

# set index for doh metadata
doh_metadata = doh_metadata.set_index('Virus name')

# drop duplicates in index
doh_metadata = doh_metadata[~doh_metadata.index.duplicated(keep='first')]

# create a new column called "location with the desired format
# e.g. North America / USA / Washington / King County
doh_metadata['Location'] = 'North America / USA / Washington / ' + doh_metadata['County'] + ' County'

# merge the dataframes on a common column
merged_df = pd.merge(gisaid_metadata, doh_metadata, on='Virus name')

# update the location column in the gisaid dataframe
merged_df['Location_x'] = merged_df['Location_y']

# drop the extra column (Location_y)
merged_df.drop(['Location_y'], axis=1, inplace=True)

# rename the original Location column (Location_x)
merged_df.rename(columns={'Location_x': 'Location'}, inplace=True)

# fill nas in the location column
merged_df['Location'] = merged_df['Location'].fillna('North America / USA / Washington')

# write out to tsv file
merged_df.to_csv('~/Downloads/wa-metadata.tsv', sep='\t')

