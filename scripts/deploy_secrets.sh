#!/bin/bash

# Argument = -e environment -u user -p password -v

usage()
{
cat << EOF
usage: $0 options

This script deploys MySQL user and password to AWS SSM Param Store.

OPTIONS:
   -h      Show this message
   -e      Environment to store MySQL credentials
   -u      MySQL User
   -p      MySQL Password
   -v      Verbose
EOF
}

ENV=
USER=
PASS=
VERBOSE=
while getopts “he:u:p:v” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         e)
             ENV=$OPTARG
             ;;
         u)
             USER=$OPTARG
             ;;
         p)
             PASS=$OPTARG
             ;;
         v)
             VERBOSE=1
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [[ -z $ENV ]] && [[ -z $USER ]] && [[ -z $PASS ]]

    echo "Path for variables is /env/$ENV/"

    aws ssm put-parameter \
        --name "/env/$ENV/mysql/user" \
        --value "$USER" \
        --type SecureString \
        --region us-west-2 \

    aws ssm put-parameter \
        --name "/env/$ENV/mysql/password" \
        --value "$PASS" \
        --type SecureString \
        --region us-west-2 \
then
     usage
     exit 1
fi