#!/bin/bash

#url="http://qubicrube.pwn.seccon.jp:33654/"
URLSTXT="./urls.txt"

SRC_DIR="./src_img/"
WRK_DIR="./wrk_dir/"
mkdir -p "${SRC_DIR}"
mkdir -p "${WRK_DIR}"

if [ -e "${URLSTXT}" ]
then
    URL=`cat "${URLSTXT}" | grep "^http"`
    grep "No. 50 / 50" "${URLSTXT}"
    if [ ${?} -eq 0 ]
    then
        exit
    fi
else
#    URL="http://qubicrube.pwn.seccon.jp:33654/02c286df1bbd7923d1f7"
    URL="http://qubicrube.pwn.seccon.jp:33654/504ded069e4db4e3bef9"
fi

rm -f ./wrk_img/*.png
CASENAME=`basename ${URL}`
./download.sh ${URL}
cp ./src_img/${CASENAME}_*.png "./wrk_img/"

python solve.py ${CASENAME}

exec bash ${0}
