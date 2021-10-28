docker build \
    --force-rm=true --rm=true  \
    --build-arg USER=$(whoami) \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    --build-arg NPROCS=$(cat /proc/cpuinfo | grep processor | wc -l) \
    --tag cryptofeed:1.1 .