!/bin/bash

export GOOGLE_NUMBER="+18144086741"
export SIGNAL_VERSION="0.6.7"

# -- install java
sudo apt update
sudo apt install -y default-jre

# -- install signal-cli
wget https://github.com/AsamK/signal-cli/releases/download/v"${SIGNAL_VERSION}"/signal-cli-"${SIGNAL_VERSION}".tar.gz
sudo tar xf signal-cli-"${SIGNAL_VERSION}".tar.gz -C /opt
sudo ln -sf /opt/signal-cli-"${SIGNAL_VERSION}"/bin/signal-cli /usr/local/bin/
rm -f ./signal-cli-"${VERSION}".tar.gz

# -- install qrencode
sudo apt install -y qrencode


echo "Registering Signal with Google Voice Number: ${GOOGLE_NUMBER}"
# -- register signal to google voice
signal-cli -u "${GOOGLE_NUMBER}" register

# -- ask for verification code
read -p "ENTER VERIFICATION CODE: " code
signal-cli -u "${GOOGLE_NUMBER}" verify $code

# -- link signal to android
echo "Creating Signal Link for Andoird App"
signal-cli link -n `hostname` > /tmp/signal.txt&
sleep 2

echo "Generating QR Code"
qrencode -o /tmp/signal.png `cat /tmp/signal.txt`
qrencode -t ANSI `cat /tmp/signal.txt`
