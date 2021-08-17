#!/bin/bash
cd ~
cd ./NeuraInk_Backend
source neuraink/bin/activate
uvicorn backend:app --host 0.0.0.0 --reload
