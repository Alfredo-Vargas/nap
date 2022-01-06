#!/bin/bash
activate(){
  . ./venv/bin/activate
}

activate

nvim -S s1.vim
