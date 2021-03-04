FROM  python:3.6
WORKDIR /opt/
ADD requirements.txt $WORKDIR

RUN apt-get update && apt-get install gcc && \
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -zxvf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
   ./configure --prefix=/usr && \
    make && \
    make install && \
    ldconfig && \
    cd /opt && \
    pip install -r requirements.txt


COPY ./ /opt/
COPY bot_trade.py /opt
ENTRYPOINT ["python","bot_trade.py"]