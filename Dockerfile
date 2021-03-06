FROM python:3.9.7


ENV WORKSPACE="/root/ws"
RUN mkdir ${WORKSPACE}
WORKDIR ${WORKSPACE}

# setup cryptofeed and other deps
RUN python -m pip install --upgrade pip
ADD . ${WORKSPACE}
RUN pip install -e . 

CMD [ "python", "-m", "scraper" ]