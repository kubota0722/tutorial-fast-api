## 最初のステップ
https://fastapi.tiangolo.com/ja/tutorial/first-steps/

シンプルなFastAPIのサンプル
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

```shell
uvicorn main:app --reload
```
で起動する

```shell
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
localhostの8000番ポートで起動する、デフォ？

```
curl localhost:8000
```
でjsonが返ってくることが確認できる

起動したurl+/docsにアクセスすると自動でOpenAPI規格のドキュメントを見れる
（langserveだと正常に見れなかったりする）

---
### path operation
#### - path

パスとは最初の`/`から始まるURL最後の部分

`https://example.com/items/foo`の`/items/foo`がパス

(エンドポイント、ルートともいう)

#### - operation

オペレーションはHTTPのメソッドの1つのこと
- GET
  - データの読み取り
- POST
  - データの作成
- PUT
  - データの更新
- DELETE
  - データの削除

(おまけ)
- OPTIONS
- HEAD
- PATCH
- TRACE

---  

### パスオペレーションのデコレーターを定義
`@app.get("/")`のようにデコレーターを定義する

直下の関数がリクエストの処理担当になることをfastapiに教えてあげる
- path
    - `/`
- operation
    - `GET`

---

### コンテンツの返信
`return {"message": "Hello World"}`

- dict
- list
- str
- int

とかを返すことができる

pydanticのモデルを返すこともできる

---
