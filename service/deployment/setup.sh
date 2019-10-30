#!bin/sh
apt install ansible -y

echo "Setting up chromedriver"
ansible-playbook scripts/install_chrome.yml