#!/bin/bash

# -- pull source
echo "fetching gmail..."
export MODULE="gmail-sender"
git clone https://github.com/paulc/"${MODULE}".git


# -- get python version
echo "determining python version..."
version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ -z "$version" ]]
then
     version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
fi
echo "Detected: Python "$version
binary="python"${version:0:1}

# -- install gmail-sender
echo "installing: ${MODULE}"
$binary -m "${MODULE}"/setup.py install

# -- configure gmail
printf %100s | tr " " "="
echo "\nNeed one-time password from  Gmail account..."
echo "  1. Enable 2-Step Verification [any method (ex: text message)]: https://myaccount.google.com/u/2/security"
echo "  2. Add a second step [any method (ex: Authenticator app)]: https://myaccount.google.com/u/2/signinoptions/two-step-verification"
echo "  3. Create and App Password: https://myaccount.google.com/u/2/apppasswords"
echo "     [Select app] = Mail"
echo "     [Select device] = <Other (Custom name)> === [HOSTNAME]" 
echo "  4. Click [\"GENERATE\"]"
printf %100s | tr " " "="
