# Marketing Mix Modeling
## Dataset
### Description
This is synthetic data, to emulate media expenses and their impact on sales.

### Format
A dataset with 156 observations, comprising various marketing exposure scenarios. Each observation represents a unique week, over the course of 3 years. The "sales" variable of the dataset is the target, which denotes the sales amount over the period, in USD. The next columns are the covariates:

- date: Week (starting with Friday)
- adwords_spending: Amount spent on AdWords advertising
- facebookads_spending: Amount spent on Facebook Ads
- awin_spending: Amount spent on Awin advertising
- tiktok_spending: Amount spent on TikTok advertising
- snapchat_spending: Amount spent on Snapchat advertising

### Why this data?
This dataset is of significant relevance for marketing mix modeling. It provides a valuable resource for studying the effectiveness of different marketing strategies, particularly in influencing online sales.

The primary focus of this dataset is to assess the impact of various marketing types of spending per channel. By comparing scenarios with different marketing exposures, you can analyze the impact of each marketing element on sales outcomes while considering other covariates.

This dataset enables you to investigate whether specific marketing activities, such as AdWords, Facebook Ads, or events like Black Friday, have a statistically significant and meaningful effect on online sales. Moreover, it allows for the evaluation of the interaction effects between different marketing channels and events, providing insights into the most effective marketing mix for driving online sales.

### Source
The code to generate that data is available under `data_generation.py`
