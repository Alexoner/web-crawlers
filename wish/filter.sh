#!/bin/bash

egrep -nv $'((.*\5){17}[!\5]*)' products/products.csv
          #$'((.*\5){17}[!\5]*)'
