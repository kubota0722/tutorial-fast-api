## クエリパラメータ
参考：https://fastapi.tiangolo.com/ja/tutorial/query-params/

パスパラメータではない関数パラメータを宣言すると、自動的にクエリパラメータとして扱われる

```python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```
クエリは`?`で始まる

example: 
`http://127.0.0.1:8000/items/?skip=0&limit=10`

このURLでのクエリパラメータは
 - skip=0
 - limit=10

これらはURLの一部なのでstrとして扱われるが、型宣言をすることで変換されバリデーションが行われる

---

### デフォルト

クエリパラメータはパスの固定部分ではないので、オプショナルにしたり、デフォルト値を持たせたりできる

上のコードではデフォルト値として`skip=0`と`limit=10`を設定している

そのため、`http://127.0.0.1:8000/items/`にアクセスすることと`http://127.0.0.1:8000/items/?skip=0&limit=10`にアクセスすることは同じ結果になる

しかし、`http://127.0.0.1:8000/items/?skip=100`のように指定することで関数内で扱われるパラメータを指定できる

---
### オプショナルなパラメータ

デフォルト値をNoneとすることで、オプショナルな（あってもなくてもかわらない）クエリパラメータを宣言できる

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
```

具体的にはqの部分がオプショナルなパラメータとなる

(item_idはパスパラメータ、qはクエリパラメータであるという判別も行ってくれる)

---
### クエリパラメータの型宣言

bool型を宣言することもできる

```python
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
```

bool値のクエリパラメータは以下のような値を受け取ることができる
- true
- True
- TRUE
- false
- False
- FALSE

---
### 必須のクエリパラメータ

デフォルト値を宣言した場合、そのパラメータは必須ではなくなる

特定のデフォルト値を与えずにただオプショナルにしたい場合はデフォルト値をNoneとする

必須にしたい場合は単にデフォルト値を宣言しなければよい

---
(パスパラメータと同様にEnumを使用することもできる)





