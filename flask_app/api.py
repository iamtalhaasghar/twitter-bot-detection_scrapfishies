from typing import Union

from fastapi import FastAPI

from twitter_funcs import bot_proba, bot_or_not, get_user_features

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/predict/{handle}')
def make_prediction(handle: str):

    # make predictions with model from twitter_funcs
    user_lookup_message = f'Prediction for @{handle}'

    if get_user_features(handle) == 'User not found':
        prediction = [f'User @{handle} not found', '']

    else:
        prediction = [bot_likelihood(bot_proba(handle)),
                      f'{bot_proba(handle)}%']

    return dict(prediction=prediction[0], probability=prediction[1], output=user_lookup_message)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def bot_likelihood(prob):
    if prob < 20:
        return 'Not a bot'
    elif prob < 35:
        return 'Likely not a bot'
    elif prob < 50:
        return 'Probably not a bot'
    elif prob < 60:
        return 'Maybe a bot'
    elif prob < 80:
        return 'Likely a bot'
    else:
        return 'Bot'



