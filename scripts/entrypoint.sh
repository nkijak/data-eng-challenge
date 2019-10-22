#!/bin/bash

main(){
  case "$1" in
    cli)
      shift
      python -m coin_market.backend.cli $@
      ;;
    api)
      shift
      FLASK_APP=coin_market.api.main.py python -m flask run
      ;;
    *)
      echo "Command is cli or api"
      break
      ;;
  esac
}

main $@
