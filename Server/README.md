# TGR 17 - Server

This server is an upgraded version from the rally that also contains the MQTT integrated with this Docker container

Prerequisite:

1. Docker Engine

How to:

1. Build the FastAPI image by:

```
cd fastapi                              # change current directory to the /fastapi folder
docker build -t "tgr2023_fastapi" .     # don't forget dot (.)
```

2. Build the Streamlit image by:

```
cd streamlit                            # change current directory to the /streamlit folder
docker build -t "tgr2023_streamlit" .   # don't forget dot (.)
```

3. Compose the container by:

```
docker compose up -d                    # On the current top of server directory, which you will found the docker-compose.yml
```

4. Done!
