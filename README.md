# GeekSpaceBot

## 概要

GeekSpaceBot は Discord サーバー「[Geek-Space](https://discord.gg/e9TftCK)」用に作成された Bot です。  
他のサーバーでの使用も考慮して開発していますが、完全な保証をするものではありません。  
他のサーバーでの利用で問題が発生した場合、責任は負いかねますのでご了承ください。

## 特徴

- Discord のメッセージ URL から Embed を生成し、見やすくする。
- ボイスチャンネルと役職を紐づけ、VC 参加時に特定のサーバーで役職を付与する。

## 実行環境の構築

この Bot はパッケージ管理ツールとして Poetry を利用しています。  
まず最初にあなたの Python 環境に Poetry をインストールしてください。

```cmd
python3 -m pip install poetry
```

インストールを行ったら、クローンしたプロジェクトのルートディレクトリ(pyproject.toml が存在するディレクトリ)に移動し、以下のコマンドを実行してください。

```cmd
poetry install --no-dev
```

これで実行環境が整いました。

### 開発環境の構築

開発環境を構築したい際は以下のコマンドを実行してください。

```cmd
poetry install
```
