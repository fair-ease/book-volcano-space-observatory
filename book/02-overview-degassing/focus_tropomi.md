# TROPOMI data

In this book, we will focus on estimating SO2 flux from data acquired by the TROPOMI sensor, onboard of Sentinel-5P.

<iframe src="https://www.esa.int/content/view/embedjw/489587" width="640" height="360" frameborder="0"></iframe>

## How is TROPOMI/Sentinel-5P data acquired?

Sentinel-5P evolves on a [polar orbit](https://en.wikipedia.org/wiki/Polar_orbit), around 824 km altitude. The main instrument carried by Sentinel-5P is TROPOMI, a UV-visible imaging spectrometer.
The TROPOMI sensor captures solar radiation backscattered by Earth and atmosphere.
TROPOMI generates images of the vertically-integrated concentration of SO2 («Column amount»), every day, at global scale.

```{image} content/tropomi_acquisition_geometry.jpg
:alt: tropomi_acquisition_geometry
:align: center
```

## Key facts about SO$_{2}$ data from TROPOMI:
* measurements are expressed in [Dobson Units](https://en.wikipedia.org/wiki/Dobson_unit)
* SO2 column amount is retrieved for a plume at altitude of 7 km (preferred retrieval ), or 1 km above the surface (anthropogenic emissions or emissions are low altitude), or at 15 km altitude (stratospheric eruptions)
* spatial coverage : global, daily
* pixel size: approximately 3 km $\times$ 5 km

```{image} content/tropomi_processing.jpg
:alt: tropomi_processing
:align: center
```
## Learn more about SO$_{2}$ products from Sentinel-5

Sentinel-5 Precursor mission concept : [Ingmann et al. (2012)](https://doi.org/10.1016/j.rse.2012.01.023)

[Sentinel-5P SO2 product documentation](https://sentiwiki.copernicus.eu/__attachments/1673595/S5P-BIRA-L2-400E-ATBD%20-%20Sentinel-5P%20TROPOMI%20SO2%20ATBD%202024%20-%202.7.0.pdf?inst-v=6fe3d1ec-7796-47a1-ac38-05617be0a23f)

Description of the SO2 product retrieval algorithm: [Theys et al. (2017), AMT](https://doi.org/10.5194/amt-10-119-2017) and [Theys et al. (2021), ACP](https://doi.org/10.5194/acp-21-16727-2021)

First detection of anthropogenic and volcanic SO2 emissions : [Fioletov et al. (2020)](https://doi.org/10.5194/acp-20-5591-2020)