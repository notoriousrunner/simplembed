# How I did

## get ready
First head to https://vibeops.one/2025/10/10/embedding-part-3-from-zero-to-ai-hero-running-your-first-ai-model-with-docker-no-tech-degree-needed/ and do all the listed steps, this piece of work is going to do some further steps

## pull and run qdrant

> docker pull qdrant/qdrant
> docker run -p 6333:6333 -v ${path_on_drive}\qdrant:/qdrant/storage qdrant/qdrant

## build a new container with the necessary libraries
In the previous tutorial we created an image with numpy, now we need one with qdrant client, so build a local image using the provided dockerfile 

> docker build -t python-qdrant:latest .

## load the documents on qdrant
Once everything is setup we can run the embedding script to load data on qdrant

> docker run -it --rm -v "${pwd}:/usr/src/app" -w /usr/src/app python-qdrant:latest python embed.py

## chat with the loaded document
Now we can chat with our documents

> docker run -it --rm -v "${pwd}:/usr/src/app" -w /usr/src/app python-qdrant:latest python chat.py

***Find more details on https://vibeops.one/***