docker run \
    -it \
    --detach \
    --name cryptofeed1.1 \
    -v ~/repos/plab:/home/imourad/ws \
    -p 2222:22 cryptofeed:1.1

    #-v ~/repos/kerndev/.vscode-server:/home/imourad/.vscode-server \
