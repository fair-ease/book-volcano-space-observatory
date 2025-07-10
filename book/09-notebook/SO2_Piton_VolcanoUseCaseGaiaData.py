# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Estimate SO2 flux emitted by Piton de la Fournaise volcano
# # using Sentinel-5P TROPOMI data
#
# ## This notebook demonstrates how to estimate SO2 (sulfur dioxide) flux emitted by Piton de la Fournaise volcano, using SO2 mass burdens from Sentinel-5P TROPOMI imagery.
#
# ## Mass burdens are extracted the VolcPlume portal (https://www.icare.univ-lille.fr/volcplume), and results are stored on the EaSy Data repository (https://doi.org/10.57932/235f8c42-142b-40ee-9948-518e83554a7d).
#
# ## The notebook shows how mass can be converted to SO2 flux using the method described in Grandin et al. (2024).
#
#
# #### Reference (JGR-Solid Earth)
#
# Grandin, R., Boichu, M., Mathurin, T., & Pascal, N. (2024).\
# Automatic estimation of daily volcanic sulfur dioxide gas flux from TROPOMI satellite observations: Application to Etna and Piton de la Fournaise.\
# Journal of Geophysical Research: Solid Earth, 129(6), e2024JB029309.\
# https://doi.org/10.1029/2024JB029309
#
# #### Algorithm source (ICARE GitLab)
#
# https://git.icare.univ-lille.fr/icare-public/so2-flux-calculator
#
# #### Dataset (EaSy Data repository)
#
# Grandin, R., Boichu, M., Mathurin, T., & Pascal, N. (2024b).\
# Sulfur Dioxide emissions from Etna and Piton de la Fournaise volcanoes (2021-2023)
# from Sentinel-5P/TROPOMI [Dataset].\
# https://doi.org/10.57932/235f8c42-142b-40ee-9948-518e83554a7d
#
# #### VolcPlume portal
#
# Boichu, M and Mathurin, T (2022)\
# "VOLCPLUME, an interactive web portal for the multiscale analysis
# of volcanic plume physico-chemical properties.".\
# [Interactive Web based Ressource]\
# Direct access: https://www.icare.univ-lille.fr/volcplume \
# https://doi.org/10.25326/362
#
# ### Author: Raphaël Grandin - March 2025 - grandin - at - ipgp.fr
#

# %% [markdown]
# ## Import packages

# %%
# For installation, please follow guidelines in https://gitlab.in2p3.fr/ForMaTer/gaia-data/use-case-volcan/so2-tropomi
from so2_tropomi import *
from so2_flux_calculator.command_line import read_mass_from_csv, read_cf_from_csv

# %% [markdown]
# ## Search for product in Easy Data repository

# %% [markdown]
# ### Setup search API

# %%
EASY_DATA_API_URL="https://www.easydata.earth/api/csw"

# %% [markdown]
# ### Search product and dataset using bounding box

# %%
string_search = "Piton de la Fournaise"
bbox = "151.09596,-33.609279,151.336939,-33.479914"
request_url = EASY_DATA_API_URL + "?REQUEST=GetRecords&SERVICE=CSW&VERSION=2.0.2&namespace=xmlns(csw=http%3A%2F%2Fwww.opengis.net%2Fcat%2Fcsw%2F2.0.2)&OUTPUTSCHEMA=http://www.isotc211.org/2005/gmd&constraintLanguage=CQL_TEXT&constraint_language_version=1.1.0&constraint=csw:title+LIKE+'" + string_search + "'&typeNames=csw:Record&resultType=results&ElementSetName=brief"
request_url

# %%
r = requests.get(request_url, allow_redirects=True, headers=headers)#.json()#['data']
root = ET.fromstring(r.text)
ET.dump(root)

# %% [markdown]
# ### The above search allows for identifying the product and dataset IDs

# %%
# ID of the product "Volcanic Sulfur Dioxide emissions from Sentinel-5P/TROPOMI (Etna and Piton de la Fournaise)"
PRODUCT_ID="b6d83680-00ac-4d7f-9651-5eac38c3c42f"
# Dataset ID (last part of the DOI)
DATASET_ID="235f8c42-142b-40ee-9948-518e83554a7d"

# %% [markdown]
# ### Search within product

# %%
request_url = EASY_DATA_API_URL + "?service=CSW&request=GetRecordById&version=2.0.2&id=%s" % PRODUCT_ID
display(request_url)

r = requests.get(request_url, allow_redirects=True, headers=headers)#.json()#['data']
root = ET.fromstring(r.text)
ET.dump(root)
#tree#.write("file.xml")

# %% [markdown]
# ### Search within dataset

# %%
request_url = EASY_DATA_API_URL + "?service=CSW&request=GetRecordById&version=2.0.2&id=%s&ElementSetName=full" % DATASET_ID
display(request_url)

# %%
r = requests.get(request_url, allow_redirects=True, headers=headers)#.json()#['data']
root = ET.fromstring(r.text)
ET.dump(root)

# %% [markdown]
# ## Download data

# %% [markdown]
# ### Dataset URL

# %%
data_in_SO2_mass_URL = "https://www.easydata.earth/back/public-api/v1/metadata/datasets/235f8c42-142b-40ee-9948-518e83554a7d/files/TROPOMI_SO2-7km_mass_25-50-75-100-150-200-250-300-400-500km_Fournaise-Piton-de-la_sza-90_tracks-7_du-0_qa-0_2021-09-15_2023-09-14.csv"
data_in_cloud_fraction_URL = "https://www.easydata.earth/back/public-api/v1/metadata/datasets/235f8c42-142b-40ee-9948-518e83554a7d/files/TROPOMI_CloudFraction_mean_25-50-75-100-150-200-250-300-400-500km_Fournaise-Piton-de-la_sza-90_tracks-7_qa-0_2021-09-15_2023-09-14.csv"


# %% [markdown]
# ### Read SO2 mass and cloud fraction

# %%
def filename_from_url(url):
    r = requests.get(url, headers=headers)
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    with open(filename, 'wb') as file:
        file.write(r.content)
    return filename   

# Save files locally
localfilename_so2 = filename_from_url(data_in_SO2_mass_URL)
localfilename_cf = filename_from_url(data_in_cloud_fraction_URL)

# Read CSV
df_so2_mass = read_mass_from_csv(localfilename_so2, utc_time=0)
df_cf = read_cf_from_csv(localfilename_cf, utc_time=0)

# Display result
display(df_so2_mass.head(), df_cf.head())

# %% [markdown]
# ### Compute SO2 flux with fixed wind speed

# %%
from so2_flux_calculator.command_line import run
run(csv_in_mass=localfilename_so2,
    cloud_fraction_file=localfilename_cf,
    output_directory='.',
    output_file="Piton_SO2_flux",
    wind_speed_fixed=6)


# %%
## Uncomment lines below to display PNG in cell
from IPython.display import Image
Image("Piton_SO2_flux.png")

# %% [markdown]
# ![title](Piton_SO2_flux.png)

# %% [markdown]
# ### Interactive version (opens in new tab)

# %%
run(csv_in_mass=localfilename_so2,
    cloud_fraction_file=localfilename_cf,
    output_directory='.',
    output_file="Piton_SO2_flux",
    wind_speed_fixed=6,
    interactive_figure=True)

# %%
