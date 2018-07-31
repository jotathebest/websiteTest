#! /bin/bash
echo "127.0.0.1 api.mixpanel.com api-iam.intercom.io static.intercomcdn.com cdn.mxpnl.com widget.intercom.io" >> /etc/hosts
python3 check.py $@
