# Machine-Learning-CH2-PS316
Repository team ML Capstone team Bangkit CH2-PS316

## Member
<ul>
  <li>(ML) M008BSY0807 – Krishna Laksheta – Universitas Gadjah Mada</li>
  <li>(ML) M004BSY0592 – Aryadanta Nugrahanjaya – Institut Teknologi Sepuluh Nopember</li>
  <li>(ML) M015BSY0037 – Ade Pengalasan – Universitas Negeri Yogyakarta</li>
</ul>

## Idea
Climate change, air pollution, and the transition to cleaner energy (fossil-based) have become global concerns. However, a significant challenge lies in accurately predicting and utilizing solar energy, which is crucial for achieving sustainable energy transition. The lack of accurate and location-specific information is a major obstacle to harnessing the potential of solar energy. This hinders individuals and professionals in planning, understanding, and optimizing the use of solar energy. Therefore, we aim to develop an application that can provide precise predictions of solar energy production using location-specific data and parameters to empower both personal and professional users. Creating such an application is essential to drive the transition towards cleaner and sustainable energy sources while addressing urgent issues like climate change and air pollution.

## Dataset
We are using NASA Power Data [dataset](https://power.larc.nasa.gov/data-access-viewer/) with parameters Clear Sky Surface Shortwave Downward Irradiance. We got around 14000 data in total with a distribution spanning from January 1, 1984, to June 30, 2023. Afterward, the dataset is processed using the windowed dataset technique.Dataset windowing is a method that involves dividing a time series dataset into overlapping or non-overlapping windows, enabling the model to learn patterns and relationships within a specified window size. This approach is useful for training models in time series prediction tasks.


## Model & Deploy
The model used in the product capstone is time series forecasting with tensorflow, the architecture of this model consists of four neural network layers consisting of three hidden layers and 1 output layer.  The trained model is encapsulated as an API using the Flask framework. The model is loaded, and predictions are generated based on the given input of longitude latitude. The results are then returned in JSON format, so that they can be accessed by external systems which are further processed by the Cloud Computing team.
