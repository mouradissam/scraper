docker run \
    -it \
    --detach \
    --name scraper0.1 \
    -v ~/repos/plab:/home/imourad/ws \
    -p 2222:22 scraper:0.1

    #-v ~/repos/kerndev/.vscode-server:/home/imourad/.vscode-server \
