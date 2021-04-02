# Reducing R.I.S.C.

**R**estaurant **I**nduced **S**ubstitution due to **C**aution (**RISC**) is a Champagne Problem in the eyes of many. But for establishments that emphasize the value of their quality offerings, guest uncertainty can make these businesses victims of their own success. Even high-value items present a prospective diner with stress when they perceive the stakes of their order as above average. This can lead to fatigue during collaborative planning, with an alternative restaurant being selected to avoid the prospect of a poor menu choice.

<p align="center">
    <b>Can machine learning reduce this sententia churn through a personalized reduction in the perceived order risk for each patron?</b>
</p>

Sententia churn is defined as the loss of a potential customer during their decision making process. It's a sort of thought attrition, occurring before they even become a customer. These would-be patrons are difficult for most businesses to identify, but a well-known brand has an advantage in this regard.

To prove this concept, the famous Death & Co. brand has offered their award-winning cocktail book, *Cocktail Codex*. Data from the book will be used to maximize the guest's ordering confidence. Some establishments accept 'returns' if a guest doesn't like their order, offering a replacement item for free. Others, like Grabowski's, omit descriptions from their menu so a guest is more likely to solicit advice from the staff. Each method requires the guest to commit time and money first; this proof of concept aims to increase ordering confidence whether the guest is four-deep at the bar or at home weighing their options.

## Road Map

*Cocktail Codex* postulates that all cocktails originate from six root (parent) templates. Each section of the book contains recipes (children) that are based on one root template. First, a Multinomial Naive Bayes classifier will be used on unseen recipes, to compute the match probability of each parent. Predictions will be made in stages, starting with a subset of the data and the simplest of vectorization/model combinations.

The corpus will be expanded to include *Modern Classic Cocktails*. Match probabilities for each parent will become features, and numerical features will be added, like quantities of ingredients/proportions of ingredients. The serverless Python backend will be served through a Flutter client for the user to interact with. Further down the road, these parent predictions will be combined with a proof-of-concept recommender to suggest the personalized, highest likelihood items off a given menu.

## Data

### Six Root Cocktail Templates

#### Initial Splitting

| **Family**       | Subset of Data | Hold-Out    | Initial Test | Initial Train   |
|:-----------------|---------------:|------------:|-------------:|----------------:|
| Old-Fashioned    | 26             | 6           | 4            | 16              |
| Daiquiri         | 21             | 4           | 4            | 13              | 
| Martini          | 21             | 4           | 3            | 14              |
| Whisky Highball  | 20             | 4           | 3            | 13              |
| Flip             | 17             | 4           | 3            | 10              |
| Sidecar          | 16             | 3           | 3            | 10              |
| **Total**        | **121**        | **25**      | **20**       | **76**          |

#### Validation Splitting

| **Family**       | Subset of Data | Hold-Out    | Final Train  |
|:-----------------|---------------:|------------:|-------------:|
| Old-Fashioned    | 26             | 6           | 20           |
| Daiquiri         | 21             | 4           | 17           |
| Martini          | 21             | 4           | 17           |
| Whisky Highball  | 20             | 4           | 16           |
| Flip             | 17             | 4           | 13           |
| Sidecar          | 16             | 3           | 13           |
| **Total**        | **121**        | **25**      | **96**       |