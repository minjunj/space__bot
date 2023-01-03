FROM ubuntu:20.04
RUN apt update && apt install -y python3
RUN apt install -y python3-pip
RUN pip install requests
RUN pip install slack_bolt
ENV SLACK_BOT_TOKEN="xoxb-1234"
ENV SLACK_APP_TOKEN="xapp-1-1234"
ENV SPACE_TOKEN="abcd"
WORKDIR /app
COPY ["app.py", "."]
CMD ["python3", "app.py"]
