
## パスパラメータ
https://fastapi.tiangolo.com/ja/tutorial/path-params/

パスパラメータはpythonのformat文字列と同じように`{}`で表現する

---
### パスパラメータと型
対象の関数の引数に型を指定することで、関数に渡されるパスパラメータの型を宣言できる

`async def read_item(item_id: int)`

これにより`curl localhost:8000/items/123`とか送ったときにitem_idはstrではなくintとして扱われる

---
### データバリデーション
pythonの型宣言を使用することでfastapiはデータのバリデーションを行う

`/items/foo`のようにパスパラメータに文字列が含まれている場合

```json
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```
int型で宣言されているのにstr型で渡されたためエラーが発生している

**データのバリデーションはpydanticで行われる**

---
### 順序の重要性
path operationsを作成するときに、固定パスをもつ状況がある

これは先に宣言しておく必要がある

```python
@app.get("/users/me")
async def read_user_me():
    return {"username": "the current user"}

@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}
```
逆に宣言している場合は、/users/meのmeの部分をパスパラメータのusernameとして認識してしまう(/users/{username}は/users/meを受け入れられる形だから)

path operationは宣言した順番に評価されていく

---
### 定義済みの値
パスパラメータを受け取るpath operationを持ち、有効なパスパラメータを事前に定義したいとき、標準のpythonのEnumを使える

簡単にすると、Enumを使うとパスパラメータの値をこちら側が決めたものに制限できる


#### - Enumクラスの作成
```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
```
Enumをインポートして、strとEnumを継承したサブクラスを作成する

strを継承しているので、値がstr型でなければならないことを指定できる

#### - パスパラメータの宣言
```python
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
```
作成したenumクラスを使用して、型アノテーションをつける

ここでの例では、alexnet, resnet, lenetのみが許可される

`curl localhost:8000/models/what`とかを送るとそもそも内部のprintまで到達しない

--- 
### python列挙型の使用
パスパラメータの値は列挙型メンバとなる

#### - 列挙型メンバの比較
```python
if model_name == ModelName.alexnet:
    return {"model_name": model_name, "message": "Deep Learning FTW!"}
```
`print(model_name)`は`ModelName.alexnet`となった

#### - 列挙型メンバの値の取得
model_name.valueを使うと値を取得できる

実際の値を取り出すことができる、ここではstrで取得できる


#### - 列挙型メンバの返却
```python
return {"model_name": model_name, "message": "Deep Learning FTW!"}
```
ここ、直でmodel_nameを返しているが、クライアントに返される前に適切な値、ここではstrに変換される
`model_name.value`に変えても同じ結果だった

---
### パスを含んだパスパラメータ

`/files/{file_path}`となるpath operationがあるとする

file_pathは`/home/johndoe/myfile.txt`のようなパスを含む文字列となる

このときURLは`/files/home/johndoe/myfile.txt`のようになる

#### - パス変換
Starletteのオプションを直接使用することで、パスパラメータの宣言ができる
```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
```
パラメータ名はfile_pathで、:pathはパラメータがいかなるパスにもマッチすることを示している


