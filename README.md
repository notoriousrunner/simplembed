# How I did

## get ready
go to https://www.docker.com/ and install docker desktop for your operating system

## get the docker images for the model and the dev container
> docker model pull ai/smollm2
> docker model run ai/smollm2
> docker model pull ai/nomic-embed-text-v1.5
> docker model run ai/nomic-embed-text-v1.5
> docker pull python:3

> docker model pull is not mandatory as run should already download and run

## start some tests with python image 
> docker run -it --rm --name my-running-script python:3 python -c "print('hello world')"

> docker run -it --rm --name myrunningscript -v ${pwd}:/usr/src/app -w /usr/src/app python:3 python helloworld.py

## see how to run python with an external library
> docker run -it --rm --name myrunningscript -v ${pwd}:/usr/src/app -w /usr/src/app python:3 python hellojson.py

*this test should fail*

> docker run -it --rm --name myrunningscript -v ${pwd}:/usr/src/app -w /usr/src/app python:3 bash -c "pip install numpy && python hellojson.py"

*this one dowloads numpy and then runs the hellowworld*

## build a new container with the necessary libraries
running pip install every time is going to be a pain, let's do it once, build a new container with new libraries specified in the Dockerfile 

> docker build -t python-numpy:latest .

## keep testing
Now we created the new docker, the import script runs smoothly

> docker run -it --rm --name my-running-script -v "${pwd}:/usr/src/app" -w /usr/src/app python-numpy:latest python hellojson.py

## test smollm2 model
in powershell run the below

> Invoke-WebRequest -Uri "http://localhost:12434/engines/llama.cpp/v1/chat/completions" `
>  -Method POST `
>  -ContentType "application/json" `
>  -InFile "myrequest.txt"

if you are using cmd use the below syntax

> curl http://localhost:12434/engines/llama.cpp/v1/chat/completions -H “Content-Type: application/json” -d @myrequest.txt

## test the embedding model
powershell

>Invoke-WebRequest -Uri "http://localhost:12434/engines/llama.cpp/v1/embeddings" `
>   -Method POST `
>   -ContentType "application/json" `
>   -InFile "myembed.txt"

cmd
> curl http://localhost:12434/engines/llama.cpp/v1/embeddings -v -H "Content-Type: application/json" -d @myembed.txt

# finally
now we have everything is needed, let's run the complete script:

> docker run -it --rm --name my-running-script -v "${pwd}:/usr/src/app" -w /usr/src/app python-numpy:latest python embed.py

***Find more details on https://vibeops.one/***