FROM amazonlinux:2 as installer

# aws cli
RUN --mount=type=cache,target=/var/cache/yum \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    yum update -y && \
    yum install -y unzip && \
    unzip awscliv2.zip && \
    ./aws/install --bin-dir /aws-cli-bin/

# Download and install kubectl
RUN --mount=type=cache,target=/root/.cache \
    curl -O "https://s3.us-west-2.amazonaws.com/amazon-eks/1.25.6/2023-01-30/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

FROM jenkins/agent
# Copy kubectl binary to jenkins/agent image
COPY --from=installer /usr/local/bin/kubectl /usr/local/bin/kubectl
# Copy docker and aws binary to jenkins/agent image
COPY --from=docker /usr/local/bin/docker /usr/local/bin/
COPY --from=installer /usr/local/aws-cli/ /usr/local/aws-cli/
COPY --from=installer /aws-cli-bin/ /usr/local/bin/