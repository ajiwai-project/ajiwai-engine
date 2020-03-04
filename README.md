# AJIWAI - engine application
## 初期設定
### pipenvのインストール
pipenvをインストールする。

`$ brew install pipenv`

補完を有効にするためにbashrcやbash_profiles等に以下を記述しておく

`eval "$(pipenv --completion)"`

## 依存パッケージのインストール

`$ pipenv install`

## サーバの起動

```
$ pipenv shell
$ python main.py
(or)
$ pipenv run python main.py
```

