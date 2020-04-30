## snapshotanalyzer30000
Demo project to manage EC2 isntances

## About

This is a demo project to demonstrate the use of boto3 to manage EC2 instance
snapshots

## Configuring

Create a profile "shotty" to maintain the instance snapshots using AWS CLI

'aws configure --profile_name'

## Running

'pipenv run python shotty/shotty.py <command>'

## Command = list, start, stop, terminate

## Added code to create snapshot
