# ARG BASE_IMAGE=dustynv/nanoowl:r36.4.0
ARG BASE_IMAGE=fcollonval/jetson_gemma
FROM ${BASE_IMAGE}

LABEL maintainer="Frédéric Collonval <frederic.collonval@webscit.com>"

# ARG PIP_INDEX_URL=https://pypi.org/simple

# Install dependencies
# RUN apt update && apt install -y alsa-utils && \
#     apt clean && \
#     rm -rf /var/lib/apt/lists/* && \
#     pip3 install -U -i ${PIP_INDEX_URL} transformers torch torchvision accelerate optimum-quanto

RUN hf download "vikhyatk/moondream2" --revision "2025-06-21" && \
    hf download "moondream/starmie-v1"

COPY . /opt/curious_frame

RUN pip3 install -i https://pypi.org/simple --no-deps -e /opt/curious_frame

WORKDIR /opt/curious_frame

CMD ["python3", "-m", "curious_frame"]
