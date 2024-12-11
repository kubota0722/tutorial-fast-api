#!/bin/bash

# APIサーバーが起動していることを確認
curl -X POST "http://localhost:8000/items/" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "テスト商品",
        "price": 100.0,
        "tax": 0.1
    }'
