FROM postgres:16

# Install required packages
RUN apt-get update && \
    apt-get install -y git build-essential postgresql-server-dev-16 && \
    git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install && \
    cd .. && \
    rm -rf pgvector && \
    apt-get remove -y git build-essential && \
    apt-get autoremove -y && \
    apt-get clean
