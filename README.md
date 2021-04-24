# Reducing R.I.S.C.

[GitHub Pages site for this project](https://wstoffers.github.io/codex/) is under construction.

**R**estaurant **I**nduced **S**ubstitution due to **C**aution (**RISC**) is a Champagne Problem in the eyes of many. But for establishments that emphasize the value of their quality offerings, guest uncertainty can make these businesses victims of their own success. Even high-value items present a prospective diner with stress when they perceive the stakes of their order as above average. This can lead to fatigue during collaborative planning, with an alternative restaurant being selected to avoid the prospect of a poor menu choice.

<p align="center">
    <b>Can machine learning reduce this sententia churn through a personalized reduction in the perceived order risk for each patron?</b>
</p>

Sententia churn is defined as the loss of a potential customer during their decision making process. It's a sort of thought attrition, occurring before they even become a customer. These would-be patrons are difficult for most businesses to identify, but a well-known brand has an advantage in this regard.

To prove this concept, the famous Death & Co. brand has offered their award-winning cocktail book, *Cocktail Codex*. Data from the book will be used to maximize the guest's ordering confidence. Some establishments accept 'returns' if a guest doesn't like their order, offering a replacement item for free. Others, like Grabowski's, omit descriptions from their menu so a guest is more likely to solicit advice from the staff. Each method requires the guest to commit time and money first; this proof of concept aims to increase ordering confidence whether the guest is four-deep at the bar or at home weighing their options.

## Road Map

*Cocktail Codex* postulates that all cocktails originate from six root (parent) templates. Each section of the book contains recipes (children) that are based on one root template. First, a Multinomial Naive Bayes classifier will be used on unseen recipes, to compute the match probability of each parent. Predictions will be made in stages, starting with a subset of the data and the simplest of vectorization/model combinations.

The corpus will be expanded to include *Modern Classic Cocktails*. Match probabilities for each parent will become features, and numerical features will be added, like quantities of ingredients/proportions of ingredients. The serverless Python backend will be served through a Flutter client for the user to interact with. Further down the road, these parent predictions will be combined with a proof-of-concept recommender to suggest the personalized, highest likelihood items off a given menu.

## Data: Six Root Cocktail Templates

### Initial Splitting

| **Family**       | Subset of Data | Hold-Out    | Initial Test | Initial Train   |
|:-----------------|---------------:|------------:|-------------:|----------------:|
| Old-Fashioned    | 26             | 6           | 4            | 16              |
| Daiquiri         | 21             | 4           | 4            | 13              | 
| Martini          | 21             | 4           | 3            | 14              |
| Whisky Highball  | 20             | 4           | 3            | 13              |
| Flip             | 17             | 4           | 3            | 10              |
| Sidecar          | 16             | 3           | 3            | 10              |
| **Total**        | **121**        | **25**      | **20**       | **76**          |

### Validation Splitting

| **Family**       | Subset of Data | Hold-Out    | Final Train  |
|:-----------------|---------------:|------------:|-------------:|
| Old-Fashioned    | 26             | 6           | 20           |
| Daiquiri         | 21             | 4           | 17           |
| Martini          | 21             | 4           | 17           |
| Whisky Highball  | 20             | 4           | 16           |
| Flip             | 17             | 4           | 13           |
| Sidecar          | 16             | 3           | 13           |
| **Total**        | **121**        | **25**      | **96**       |

### Initial processing (conducted with permission)
1. Photographs of book pages
2. Apache Beam pipeline on GCP Dataflow
3. ETL pipeline call to Google Cloud Vision
4. JSON output

#### Raw JSON example (shown with permission)
```
"image001": {
    "imageName": "image.jpg",
    "page": "10",
    "text": [
        "Golden Boy",
        "ALEX DAY AND DEVON TARBY,",
        "2013",
        "1 1/2 ounces Raisin-Infused Scotch",
        "(page 292)",
        "1/2 ounce Barbeito 5-year",
        "rainwater madeira",
        "1/4 ounce Busnel Pays d\\'Auge",
        "VSOP Calvados",
        "1/4 ounce B\\303\\251n\\303\\251dictine",
        "2 dashes Peychaud\\'s bitters",
        "Garnish: 1 lemon twist",
    ]
}
```

It is worth noting that unicode octal UTF-8 bytes must be decoded, lines must be combined, and the recipe title must be separated for fear of data leakage. In addition, words in the titles can be misleading: The Coffee Cocktail is named after its appearance and does not even utilize coffee as an ingredient. When this proof of concept is distributed to users, an input recipe should be checked against a database of known recipes before any machine learning is started. This means that the model would be more likely to see a title with an unrelated name than a classic title, since classic recipes would already be in the database.

#### Ingredients Processed Into String (fake data example)
```
"1 1/2 ounces Raisin-Infused Scotch (page 292) Singani 63 1/4 ounce Busnel Pays d'Auge VSOP Calvados 1/4 ounce Bénédictine 2 dashes Peychaud's bitters Garnish: 1 lemon twist"
```

Special attention should be given to the ingredient `Singani 63` in the above example. The numerical ending to the ingredient name defeats the regular expression tokenizer that is described below. This ingredient only appeared once in the subest of data used, but we will hopefully live in a future where this ingredient is used much more often. Prediction sensitivity to this ingredient will assessed in the near future.

## Measuring Success

Some cocktails are even difficult for human experts to classify. The Tom Collins, for example, is classified in *Cocktail Codex* as a Daiquiri, but some argue it should belong to the Whisky Highball family. To ease the algorithm's burden in situations like this, an accuracy scoring metric was selected such that a target matching either of the top two predicted classes will be considered a success. This also is helpful for interpretability, as a percentage accuracy is reported.

## Baseline Model

- Bag of Words vectorizer
    - Custom tokenization with regular expression that looks for:
        - Number of 'dashes' bigram
        - Fraction of ounces greater than one trigram
        - Fraction of ounces less than one bigram
        - Whole number ounces bigram
        - Unigram words longer than 2 characters otherwise
- Multinomial Naive Bayes classifier

## Results

- Initial test score: 85%
- Hold-out validation score: 92%

### Correct Predictions on Unseen Data
- 21 recipes were predicted correctly with top probability
    - 13 of these were above 99% certainty
    - 20 of these were above 90% certainty
- 2 recipes were predicted correctly with 2nd highest probability
    - 90.8% sure Cuba Libre was a Daiquiri
        - Whisky Highball target only 9.1%
    - 98.8% sure Cosmopolitan was a Daiquiri
        - Sidecar target only 1.2%

### Incorrect Predictions on Unseen Data
- 1 recipe was predicted incorrectly with 3rd highest probability
    - 85.5% sure Deadpan was a Flip
        - Old-Fashioned target only 4.4%
- 1 recipe was predicted incorrectly with 4th highest probability
    - 37.1% sure Traction was a Sidecar
        - Old-Fashioned target only 5.1%

### Predictions of Note
- New York Flip & Bean Me Up Biscotti scored with higher probability than Flip
- Pisco Sour & Southside scored higher than Daiquiri, but not Daiquiri (Less Sweetener)

## Future Work
Version beta of application
- More data
- Accent folding for user input
- Stop words
- Bigrams
- Lemmatization
- Other feature extractors
- Complement Naive Bayes and other models
- Creative ways to visualize results without word clouds
- Deploy with Flutter app
- Recommendation system and broadening to general palate