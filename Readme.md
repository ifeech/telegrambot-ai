# AI Telegram Bot (experiments)

Only open source projects are used.

Run:
1. Create an .env file from .env.example
2. Start with the desired model

## Whisper

https://github.com/openai/whisper

Whisper is a general-purpose speech recognition model.

Wisper requires the command-line tool **ffmpeg** to be installed on your system, which is available from most package managers.

## Ollama

https://github.com/jmorganca/ollama

1. Pull and run ollama/ollama docker image
2. Download model (e.g. mistral)
3. Run telegram chat

```
python3 main.py --client=ollama -u http://localhost:11434/api -m mistral
```

## GPT4All

https://github.com/nomic-ai/gpt4all

1. Clone gpt4all-api
2. Run the docker build (see GPT4All documentation)
   1. I recommend modifying the gpt4all_api/Dockerfile.buildkit file to remove the `RUN wget` command
   2. Add `volume` <local_path_to_dir_with_models>:/models in `docker-compose.yaml`
   3. Download some models to <local_path_to_dir_with_models>
3. Run the server (see GPT4All documentation)
   - Use your model for `model` var in environment `docker-compose.yaml`
4. Run telegram chat

```
python3 main.py --client=gpt4all --uri=http://localhost:4891/v1 --model=nous-hermes-llama2-13b.Q4_0.gguf
```

> `--client=gpt4all` is specified to use the `Completion` method for Gpt4All. Cause `ChatCompletion` doesn't work for me. You can add some logic to the /gpt4all-api/gpt4all_api/app/api_v1/routes/chat.py in the GPT4All repo. Then run bot-ai without --client=gpt4all.

Openapi doc: `http://localhost:4891/docs`

## Fastchat

https://github.com/lm-sys/FastChat

1. Clone repo
2. Install dependencies
3. Start the api server (see Fastchat documentation)

e.g.

```
python3 -m fastchat.serve.controller

python3 -m fastchat.serve.model_worker --model-path ../Models/vicuna-7b-1.5 --load-8bit --cpu-offloading

python3 -m fastchat.serve.openai_api_server --host localhost --port 4891
```

`../Models/vicuna-7b-1.5` - downloaded model

`--load-8bit` and `--cpu-offloading` parameters are used to reduce the load on the system.

4. Run telegram chat

```
python3 main.py -u http://localhost:4891/v1 -m vicuna-7b-1.5
```

Openapi doc: `http://localhost:4891/docs`