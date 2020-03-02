#!/bin/bash

        # install for AWX Tower.
        if [ -d ~/.ansible ] 
        then
           echo "Installing into: ~/.ansible/collections/"
           cp -R awx_collection ~/.ansible/collections/
        fi
