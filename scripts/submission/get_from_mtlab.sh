#!/bin/bash

server='mtlab.itu.dk'
rem_results_dir='/home/elvis/quantify_linux_errors/results/'
loc_results_dir='results/'

scp -r "$server":"$rem_results_dir"* "$loc_results_dir"
