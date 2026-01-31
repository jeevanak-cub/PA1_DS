#!/bin/bash

echo "Starting Product DB..."
python3 product_db.py &

echo "Starting Customer DB..."
python3 customer_db.py &

sleep 1

echo "Starting Seller Server..."
python3 seller_server.py &

echo "Starting Buyer Server..."
python3 buyer_server.py &

echo "All components started."
