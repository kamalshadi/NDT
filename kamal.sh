#!/bin/bash
yum install git-core
easy_install bigquery
yum install emacs
easy_install pip
pip install networkx
pip install ipaddress
yum install numpy scipy python-matplotlib
yum -y install gcc gcc-c++ numpy python-devel scipy
easy_install -U scikit-learn

