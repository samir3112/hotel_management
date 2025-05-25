FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y && \
    curl -fsSL https://get.docker.com | sh && \
    usermod -aG docker jenkins && \
    apt-get install -y python3 python3-pip python3.11-venv && \
    rm -rf /var/lib/apt/lists/*

USER jenkins
