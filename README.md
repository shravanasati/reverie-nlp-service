# reverie-nlp-service

An NLP service for [reverie](https://github.com/shravanasati/reverie) written in FastAPI which hosts several pre-trained models for sentiment and emotion analysis, and keyword extraction for journals.

### setup

you'll need a `.env` file inside the `src/` directory.

```
API_KEY=
```

`API_KEY` is used to secure the service, ensuring only clients with the API key can access the server.

##### option 1: use pre built docker image (recommended)

```
docker compose up
```

This will pull the image from docker hub and run it on port 5000 locally. First time run of the image will take a lot of time since it downloads the models from hugging face.

Alternatively, 

```
docker run -d --name nlp-service -p 5000:8000 --env-file ./src/.env shravanasati/reverie-nlp-service
```

##### option 2: build your own docker image 

```
docker build -t name/reverie-nlp-service .
```

Run it using commands mentioned in option1. Ensure proper substitution of image name.

##### option 3: local setup 

1. `poetry install`

2. `poetry run fastapi dev ./src/main.py`