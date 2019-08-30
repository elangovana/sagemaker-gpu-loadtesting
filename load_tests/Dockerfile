FROM python:3.6

ENV source_path /opt/program/source
RUN mkdir -p ${source_path}



#Set up source
COPY ./  ${source_path}
RUN pip install -r ${source_path}/requirements.txt
RUN pip install  awscli --upgrade

#Set up working directory
WORKDIR ${source_path}
ENTRYPOINT  ["locust"]

#Default arguments to run test
CMD ["-f","stress.py", "-h"]