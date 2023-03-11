#!/bin/bash

if [[ $# -eq 0 ]]; then
  echo "No arguments provided."
  exit 1
fi

cleanup_and_delete () {
  echo "Cleaning up and deleting all rec-* directories..."
  find ./shared -type d -name 'rec-*' -exec rm -rf {} +
  find ./shared -type d -name 'gif-*' -exec rm -rf {} +
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    "-d" | "--delete" )
      cleanup_and_delete
      ;;
    "-s" | "--start" )
      echo "Starting docker-compose up in detached mode..."
      docker-compose up -d
      ;;
    "-r" | "--stop" )
      echo "Stopping docker-compose and removing containers..."
      docker-compose down
      ;;
    "-b" | "--build" )
      echo "Building docker-compose..."
      docker-compose build
      ;;
    * )
      echo "Invalid argument: $1"
      exit 1
      ;;
  esac
  shift
done
