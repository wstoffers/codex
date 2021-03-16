#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import joblib

#define:
def awaken(ingredients):
    model, extractor = joblib.load('trained.joblib')
    x = extractor.transform(ingredients)
    probabilities = model.predict_proba(x)
    return {f: f'{p*100:0.2f}%' for f, p in zip(model.classes_,
                                                probabilities[0])}

#run:
if __name__ == '__main__':
    pass
