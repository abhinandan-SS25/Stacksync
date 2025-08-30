FROM debian:bookworm-slim

# Install dependencies for building nsjail and Python
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    git make g++ pkg-config libprotobuf-dev protobuf-compiler libnl-route-3-dev \
    libtool automake autoconf bison flex \
    && rm -rf /var/lib/apt/lists/*

# Build and install nsjail from source
RUN git clone https://github.com/google/nsjail.git /tmp/nsjail \
    && make -C /tmp/nsjail \
    && cp /tmp/nsjail/nsjail /usr/bin/nsjail \
    && rm -rf /tmp/nsjail

# Set work directory and copy app files
WORKDIR /app
COPY server.py execution_wrapper.py run.python3.config.proto /app/

# Install Flask
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install flask
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8080
CMD ["python3", "server.py"]