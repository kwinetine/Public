
# Function to search for taxon_id by scientific name
def search_taxon_id_by_name(user_string, df):
    # Convert the scientific_name column to lowercase for comparison
    df["scientific_name_lower"] = df["scientific_name"].str.lower()
    scientific_name = user_string.lower()
    
    filtered_df = df[df["scientific_name_lower"].str.contains(scientific_name)]
    
    if not filtered_df.empty:
        taxon_ids = filtered_df["taxon_id"].tolist()
        return taxon_ids
    else:
        return []

def search_scientific_name_by_id(taxon_id, df):
    filtered_df = df[df["taxon_id"] == taxon_id]
    if not filtered_df.empty:
        scientific_names = filtered_df["scientific_name"].tolist()
        return scientific_names
    else:
        return []