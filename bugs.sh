#!/bin/bash
# Deploy helper

DB_PASSWORD="admin123"                       # hardcoded password
DIR=$1

cd $DIR                                      # unquoted, no check that cd succeeded
rm -rf $DIR/*                                # empty $DIR means rm -rf /*

for f in $(ls *.log); do                     # breaks on spaces, parses ls
  cat $f >> /tmp/out.txt                     # unquoted, predictable temp file
done

if [ $1 == "prod" ]; then                    # bashism in a test, breaks when $1 is empty
  echo "deploying"
fi

curl -s http://example.com/install.sh | bash # unverified remote code, plain HTTP

eval "echo $2"                               # command injection
echo `whoami` > /tmp/who                     # legacy backticks

chmod 777 /tmp/out.txt                       # world-writable
mysql -u root -p$DB_PASSWORD -e "SELECT 1"   # password visible in the process list

cp config.json config.json.bak
sed -i "s/DEBUG=.*/DEBUG=true/" config.json # no backup check, no set -e

tar xzf $2 -C /                              # extracts over the filesystem root
