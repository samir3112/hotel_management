# kubernetes env

## To bring machine up
   carry on all instuctions on gitbash

   ensure Vagrant is setup

   ```
   git clone this repository
   cd kubernetes-env
   vagrant up
   ```
## To work with VSC
   on gitbash -> code.

   this will open VSC

   install the "Remote - SSH" extension on VSC

   on git bash type -

   vagrant ssh-config

   store the content of controlplane host only on some file like kube-vm-config.txt (change name of host to Docker)

   on VSC - ctrl + shift + P

   Remote-SSH: Open SSH Configuration File -> Settings -> add the previous created file

   again on VSC - ctrl + shift + P - > Remote SSH: Connect to Host

   connect to controlplane (host) and select Linux on pop-up

   VSC will be downloaded on vagrant machine (with till download finish)

## Import Docker-Kubernetes git repo now to work with
   ```
   git clone https://<git_user>:<git_password>@github.com/cbagade/py-docker-kubernetes-learnings.git
   on VSC - Explorer - Open /home/vagrant/py-docker-kubernetes-learnings/
   select linux platform when prompted
   Trust the author when prompted
   open app.py -> VSC might prompt to install python extension, install
   open Dockerfile -> VSC might prompt to install docker extension, install
   ```

## Ensure Kubernetes Setup
   ```
   open terminal
   kubectl get nodes
   ```   

## How to work
   building and pushing of docker images should be done from Docker host (vm)

   kubernetes related stuff should be done from controlplane host (vm)

## FOLLOWING INSTRUCTIONS MIGHT NOT BE NEEDED

## Original Readme file content is pasted below

## Vagrantfile and Scripts to Automate Kubernetes Setup using Kubeadm [Practice Environment for CKA/CKAD and CKS Exams]

A fully automated setup for CKA, CKAD, and CKS practice labs is tested on the following systems:

- Windows
- Ubuntu Desktop
- Mac Intel-based systems

If you are MAC Silicon user, Please use the follwing repo.

- [Vagrant Kubeadm Setup on MAC Silicon](https://github.com/techiescamp/vagrant-kubeadm-mac-silicon)

## CKA, CKAD, CKS, or KCNA Vouchers Codes

>**Important Note**: This extended Offer Ends Very Soon

As part of our commitment to helping the DevOps community save money on Kubernetes Certifications, we continuously update the latest voucher codes from the Linux Foundation

🚀  CKA, CKAD, CKS, or KCNA exam aspirants can **save 30%** today using code **30COMTECHIES** at https://kube.promo/devops. It is a limited-time offer from the Linux Foundation.

The following are the best bundles to **save 40% (up to $788)** with code **30COMTECHIES**

- KCNA + KCSA + CKA + CKAD + CKS ($788 Savings): [kube.promo/kubestronaut](https://kube.promo/kubestronaut)
- CKA + CKAD + CKS Exam bundle ($528 Savings): [kube.promo/k8s-bundle](https://kube.promo/k8s-bundle)
- CKA + CKS Bundle ($355 Savings) [kube.promo/bundle](https://kube.promo/bundle)
- KCNA + CKA ( $288 Savings) [kube.promo/kcka-bundle](https://kube.promo/kcna-cka)
- KCSA + CKS Exam Bundle ($229 Savings) [kube.promo/kcsa-cks](https://kube.promo/kcsa-cks)
- KCNA + KCSA Exam Bundle ($203 Savings) [kube.promo/kcna-kcsa](https://kube.promo/kcna-kcsa)

>**Note**: You have one year of validity to appear for the certification exam after registration

## Setup Prerequisites

- A working Vagrant setup using Vagrant + VirtualBox

## Documentation

Current k8s version for CKA, CKAD, and CKS exam: 1.29. 

The setup is updated with 1.29 cluster version.

Refer to this link for documentation full: https://devopscube.com/kubernetes-cluster-vagrant/


## Prerequisites

1. Working Vagrant setup
2. 8 Gig + RAM workstation as the Vms use 3 vCPUS and 4+ GB RAM

## For MAC/Linux Users

The latest version of Virtualbox for Mac/Linux can cause issues.

Create/edit the /etc/vbox/networks.conf file and add the following to avoid any network-related issues.
<pre>* 0.0.0.0/0 ::/0</pre>

or run below commands

```shell
sudo mkdir -p /etc/vbox/
echo "* 0.0.0.0/0 ::/0" | sudo tee -a /etc/vbox/networks.conf
```

So that the host only networks can be in any range, not just 192.168.56.0/21 as described here:
https://discuss.hashicorp.com/t/vagrant-2-2-18-osx-11-6-cannot-create-private-network/30984/23

## Bring Up the Cluster

To provision the cluster, execute the following commands.

```shell
git clone https://github.com/scriptcamp/vagrant-kubeadm-kubernetes.git
cd vagrant-kubeadm-kubernetes
vagrant up
```
## Set Kubeconfig file variable

```shell
cd vagrant-kubeadm-kubernetes
cd configs
export KUBECONFIG=$(pwd)/config
```

or you can copy the config file to .kube directory.

```shell
cp config ~/.kube/
```

## Install Kubernetes Dashboard

The dashboard is automatically installed by default, but it can be skipped by commenting out the dashboard version in _settings.yaml_ before running `vagrant up`.

If you skip the dashboard installation, you can deploy it later by enabling it in _settings.yaml_ and running the following:
```shell
vagrant ssh -c "/vagrant/scripts/dashboard.sh" controlplane
```

## Kubernetes Dashboard Access

To get the login token, copy it from _config/token_ or run the following command:
```shell
kubectl -n kubernetes-dashboard get secret/admin-user -o go-template="{{.data.token | base64decode}}"
```

Make the dashboard accessible:
```shell
kubectl proxy
```

Open the site in your browser:
```shell
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login
```

## To shutdown the cluster,

```shell
vagrant halt
```

## To restart the cluster,

```shell
vagrant up
```

## To destroy the cluster,

```shell
vagrant destroy -f
```

