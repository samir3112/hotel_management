FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y && \
    curl -fsSL https://get.docker.com | sh && \
    usermod -aG docker jenkins && \
    apt-get install -y python3 python3-pip python3.11-venv && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

# Install docker in controlplane k8
#  sudo apt-get update
# sudo apt-get install -y \
#     ca-certificates \
#     curl \
#     gnupg \
#     lsb-release

# sudo mkdir -m 0755 -p /etc/apt/keyrings
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
#     sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# echo \
#   "deb [arch=$(dpkg --print-architecture) \
#   signed-by=/etc/apt/keyrings/docker.gpg] \
#   https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) stable" | \
#   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# sudo apt-get update
# sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# sudo usermod -aG docker $USER
# newgrp docker  # Apply the group changes immediately
# docker --version

# cd ~/hotel_management/jenkins-docker
# docker build -t samir3112/jenkins-custom:v1 .
# docker push samir3112/jenkins-custom:v1

# docker run -d -p 8080:8080 -p 50000:50000 --name jenkins_custom samir3112/jenkins-custom:v1
