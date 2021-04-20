ARG TAG=2.5.0rc1 #cannot be used after FROM
FROM tensorflow/tensorflow:$TAG
WORKDIR /home/sandbox
COPY . /home/sandbox
COPY --from=gcr.io/google.com/cloudsdktool/cloud-sdk:alpine /google-cloud-sdk /google-cloud-sdk
#ENTRYPOINT ["/home/data"]
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt