import pandas as pd

# List of source files names
catalunya_regions_name = "data_sources/Catalunya_region.csv"
sm_data_name = "data_sources/Fitxers_dades_obertes_sm_centres_2016_2019.xlsx"

cat_regions_df = pd.read_csv(catalunya_regions_name)
sm_data_df = pd.read_excel(sm_data_name, 'territori')

# sm_data_df.columns = sm_data_df.columns.astype('str')
# sm_data_df.columns = map(str.lower, sm_data_df.columns)
# cat_regions_df.columns = map(str.lower, cat_regions_df.columns)

com_col = "aga"
cat_region_col = "nom_comar"
patient_col = "Suma de pacients"

cat_regions_df["nom_comar"] = cat_regions_df["nom_comar"].str.lower()
sm_data_df[com_col] = sm_data_df[com_col].str.lower()

sm_data_pcsm_df = sm_data_df[(sm_data_df['pcsm']==1)|(sm_data_df['pccsm']==1)]


nom_comar_map = {
    "alt camp i conca de barberà": "alt camp",
    "alt maresme": "maresme",
    "alt pirineu i aran": "val d'aran",
    "altebrat": "",
    "aran": "val d'aran",
    "bages i solsonès": "bages",
    "baix camp i priorat": "priorat",
    "baix llobregat centre i fontsanta -l'h n": "baix llobregat",
    "baix llobregat litoral i sant boi": "baix llobregat",
    "baix llobregat litoral i viladecans": "baix llobregat",
    "baix llobregat nord": "baix llobregat",
    "baix montseny": "vallès oriental",
    "baix vallès": "vallès oriental",
    "barcelona": "barcelonès",
    "barcelona dreta": "barcelonès",
    "barcelona esquerra": "barcelonès",
    "barcelona litoral mar": "barcelonès",
    "barcelona nord": "barcelonès",
    "barcelonès nord i baix maresme": "barcelonès",
    "camp de tarragona": "tarragonès",
    "catalunya central": "anoia",
    "girona": "gironès",
    "gironès nord i pla de l'estany": "gironès",
    "gironès sud i selva interior": "gironès",
    "l'hospitalet sud i el prat de llobregat": "baix llobregat",
    "lleida": "segrià",
    "maresme central": "maresme",
    "pallars": "pallars jussà",
    "selva marítima": "selva",
    "terres de l'ebre": "baix ebre",
    "vallès occidental est": "vallès occidental",
    "vallès occidental oest": "vallès occidental",
    "vallès oriental central": "vallès oriental",
}

sm_data_pcsm_df[com_col] = sm_data_pcsm_df[com_col].map(nom_comar_map).fillna(sm_data_pcsm_df[com_col])
pcsm_patients_df = sm_data_pcsm_df.groupby(com_col)[patient_col].sum().reset_index()
final_regions_pcsm_df = pd.merge(cat_regions_df, pcsm_patients_df, left_on=cat_region_col, right_on=com_col, how='outer')
final_regions_pcsm_df.to_csv("CataloniaMap.csv", encoding='utf-8-sig')

sex_col = 'sexe'
year_col = 'Any'
sex_map = {
    0: "Mujer",
    1: "Hombre",
}
sm_data_df[sex_col] = sm_data_df[sex_col].map(sex_map).fillna(sm_data_df[sex_col])
sm_data_pcsm_df[sex_col] = sm_data_pcsm_df[sex_col].map(sex_map).fillna(sm_data_pcsm_df[sex_col])

category_col = sm_data_df.grup_edat.str.get_dummies().mul(sm_data_df[patient_col], 0)
bar_char_df = pd.concat([sm_data_df, category_col], axis=1)
grouped_bar_char_df = bar_char_df.groupby([year_col, sex_col])[category_col.columns].sum().reset_index()
# grouped_bar_char_df[sex_col] = grouped_bar_char_df[sex_col].map(sex_map).fillna(grouped_bar_char_df[sex_col])
grouped_bar_char_df.to_csv("BarChartWomenMen.csv", encoding='utf-8-sig')

proportion_df = sm_data_df.groupby(sex_col)[patient_col].sum().reset_index()
proportion_df['Pacientes base 100'] = (((proportion_df[patient_col] - 0) * (100 - 0)) / (proportion_df[patient_col].sum() - 0)) + 0
# proportion_df[sex_col] = proportion_df[sex_col].map(sex_map).fillna(proportion_df[sex_col])
proportion_df.to_csv("ProportionWomenMen.csv", encoding='utf-8-sig')

case_evolution_df = sm_data_df.groupby(year_col)[patient_col].sum().reset_index()
case_evolution_df.to_csv("CaseEvolution.csv", encoding='utf-8-sig')

pie_char_year_df = sm_data_pcsm_df.groupby([year_col, sex_col])[[patient_col]].sum().groupby(level=0).transform(lambda x: x/x.sum()) * 100
pie_char_year_df['Total'] = sm_data_pcsm_df.groupby([year_col, sex_col])[patient_col].sum()
pie_char_year_df.to_csv("PieChartTime.csv", encoding='utf-8-sig')