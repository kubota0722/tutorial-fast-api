## リクエストボディ
参考: https://fastapi.tiangolo.com/ja/tutorial/body/

クライアント（ブラウザなど）からAPIに対してデータを送信する必要があるとき、データをリクエストボディをして送信する

- リクエストボディ
    - クライアントによってAPIへと送られる
- レスポンスボディ
    - APIからクライアントへと送られる

APIはほとんどの場合、レスポンスボディを送らなければならないが、クライアントは必ずしもリクエストボディを送らなくてもよい

リクエストボディを宣言するときにはPydanticモデルを使用する

```
データを送るときにはPOST、PUT、DELETE、PATCHメソッドを使うと良い
GETはFastAPIでサポートされているがユースケースが限られている
```

#### - PydanticのBaseModelをインポート
始めにpydanticのBaseModelをインポートする必要がある

```python
from pydantic import BaseModel
```

#### - データモデルの作成
BaseModelを継承したクラスとしてデータモデルを宣言する

すべての属性にpython標準の型を指定する

```python
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

クエリパラメータの宣言時と同様に、デフォルト値を宣言することもできる

ここではdescriptionとtaxにデフォルト値を宣言している

デフォルト値にNoneを指定しているので、これらの属性はオプショナルである

```json
{
    "name": "テスト商品",
    "description": "これはテスト商品です",
    "price": 100.0,
    "tax": 0.1
}
```
モデルItemは上のようなjson(pythonのdict)を宣言している

```json
{
    "name": "テスト商品",
    "price": 100.0,
}
```
これでもOK

#### - パラメータとして宣言
パスオペレーションに加えるために、パスパラメータやクエリパラメータと同様に対象の関数の引数として宣言する

```python
@app.post("/items/")
async def create_item(item: Item):
    return item
```

#### - 結果
この型宣言だけでFastAPIは以下のことを行う
- リクエストボディをjsonとして読み取る
- 適当な型に変換する（必要であれば）
- データのバリデーションを行う
  - データが無効な場合はエラーが返され、どこが間違っていたか示してくれる
- データをモデルに適用する

---
### モデルの使用
関数内部で、モデルの全ての属性にアクセスできる

```python
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```
tutorialでは.dict()を使用しているが、.model_dump()に変更

---
### リクエストボディ+パスパラメータ
パスパラメータとリクエストボディを同時に宣言できる

FastAPIが自動でパスパラメータはパスから受け取り、Pydanticモデルで宣言された引数はリクエストボディから受け取ってくれる

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}
```

---
### リクエストボディ+パスパラメータ+クエリパラメータ
もちろん、ボディ、パス、クエリのパラメータも同時に宣言できる

FastAPIがそれぞれをうまく認識して、それぞれのパラメータを適切に受け取ってくれる

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, q: Optional[str] = None
):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
```
---
関数パラメータが認識される仕組み
- パラメータがパスで宣言されている場合は、優先的にパスパラメータとして扱う
- パラメータが単数型（int, float, str, boolなど）で宣言されている場合は、クエリパラメータとして扱う
- パラメータがPydanticモデルで宣言されている場合は、リクエストボディとして扱う


