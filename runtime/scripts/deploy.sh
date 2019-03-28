#!/usr/bin/env bash
pcf_domain=$1
pcf_user_name=$USERNAME
pcf_password=$PASSWORD
pcf_org=$2
pcf_space=$3
manifest=$4
postgres_creds={\"uri\":\"$5\"}

echo "PCF api url: " ${pcf_domain}
echo "PCF user name: " ${pcf_user_name}
echo "PCF password: " ${pcf_password}
echo "PCF Org: " ${pcf_org}
echo "PCF Space: " ${pcf_space}
echo "manifest: " ${manifest}
echo "postgres creds: " ${postgres_creds}

echo ""
echo "  [Rails.AI] Login in target org ${pcf_org}"
echo -ne '\n' | cf login -a "api.${pcf_domain}" -u "${pcf_user_name}" -p "${pcf_password}" -o "${pcf_org}" --skip-ssl-validation

echo ''
cf spaces | grep -w "${pcf_space}" >> /dev/null
if [ $? -ne 0 ]; then
    echo "  [Rails.AI] Create space ${pcf_space}"
    cf create-space "${pcf_space}" -o "${pcf_org}"
else
    echo "  [Rails.AI] Re-use existing space ${pcf_space}"
fi
cf target -o "${pcf_org}" -s "${pcf_space}"

cf services | grep BROKER >> /dev/null
if [ $? -ne 0 ]; then
    echo "  [Rails.AI] create PCF native rabbitmq service"
    cf create-service p-rabbitmq standard BROKER
else
    echo "  [Rails.AI] Re-use service instance BROKER"
fi

cf services | grep BACKEND >> /dev/null
if [ $? -ne 0 ]; then
    echo "  [Rails.AI] create PCF native redis service"
    cf create-service p-redis shared-vm BACKEND
else
    echo "  [Rails.AI] Re-use service instance BACKEND"
fi

cf services | grep POSTGRES >> /dev/null
if [ $? -ne 0 ]; then
    echo "  [Rails.AI] create credhub for POSTGRES"
    cf create-service credhub default POSTGRES -c "${postgres_creds}"
else
    echo "  [Rails.AI] Re-use service instance BACKEND"
fi

cf configure-autoscaling task-engine ./runtime/manifests/manifest-autoscaler-sre.yml

echo ''
echo "  [Rails.AI] Push the micro-service"
cf push -f "${manifest}" task