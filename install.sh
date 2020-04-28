#!/bin/bash

read -p "enter your FQDN (example: sokotaro.hopto.org): " fqdn
echo 'openssl req -nodes -newkey rsa:2048 -keyout server.key -x509 -days 365 -out server.crt -subj "/C=US/ST=Delaware/L=Newark/O=/CN=$fqdn"'
openssl req -nodes -newkey rsa:2048 -keyout server.key -x509 -days 365 -out server.crt -subj "/C=US/ST=Delaware/L=Newark/O=/CN=$fqdn"

# echo 'openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes -subj "/C=US/ST=Delaware/L=Newark/O=/CN=$fqdn"'
# openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes -subj "/C=US/ST=Delaware/L=Newark/O=/CN=$fqdn"

# -- get python version
echo -e "\ndetermining python version..."
binary=$(which python3)
if [[ -z "$binary" ]]
then
    binary=$(which python2)
fi
if [[ -z "$binary" ]]
then
    binary=$(which python)
fi
echo -e "Found Python: ${binary}"

# -- pull source
echo "fetching gmail sources..."
export MODULE="gmail-sender"
if [ -d "${MODULE}" ]
then
    echo " sources already exist."
else
    git clone https://github.com/paulc/"${MODULE}".git
fi

# -- install gmail-sender
echo -e "\ninstalling: ${MODULE}"
cd "${MODULE}"
# $binary setup.py build --user
$binary setup.py install --user --prefix=
cd ..
rm -rf  "${MODULE}"

# -- testing python and import gmail
echo -e "\nPython import gmail test..."
error=$($binary -c "from gmail import GMail, Message")
if [[ -z $error ]]
then
    echo "Gmail module successfully loaded!"
else
    ehco "Gmail FAILED TO LOAD..."
fi

# -- configure gmail
$binary setup_gmail.py

echo -e "\nDEBUG NOTES"
echo "Command used to run test: ${binary} setup_gmail.py"

echo -e "\nTO RUN WEB SERVER:"
echo "${binary} server.py 4443"

