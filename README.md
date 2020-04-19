# AJIWAI - engine application
## 環境
* pipenv: version 2018.11.26
* python: 3.7系

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
(firebaseに接続)
$ pipenv run dev
(localのファイルを使用)
$ python run local
```

## レビューデータのマイグレート

```
$ pipenv run migrate
```