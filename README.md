# python3系のバッチスクリプトの雛形 

### 概要

この雛形では以下のことをしています。

* コマンドライン引数のパース(clickの利用)
* 設定クラスの読み込み
* ログ出力(loggingの利用)
* ライブラリ読み込み
* ライブラリの単体テスト
 
### ファイルの配置

```
app_home/
       ├ bin/
       │   └  my_batch.py   #←実行するスクリプト
       ├ conf/
       │   └  my_batch_conf.py #←設定クラス
       ├ lib/
       │   ├  __init__.py    #←モジュールをロードするのに必要
       │   └  my_lib.py      #←ライブラリ
       ├ tests/        
       │   └  test_my_lib.py #←単体テストコード
       ├ log/                #←ログ出力先
       └ Pipfile             #←使うライブラリを列挙
```

### 内容

本体`my_batch.py`の内容

```python
import sys
import os
import click
import logging

# 親ディレクトリをアプリケーションのホーム(${app_home})に設定
app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
# ${app_home}をライブラリロードパスに追加
sys.path.append(os.path.join(app_home))

# 自前のライブラリをロード
from lib.my_lib import MyLib

# 設定クラスのロード
from conf.my_batch_conf import MyBatchConf

# コマンドライン引数のハンドリング. must_argは必須オプション、optional_argは任意オプション
@click.command()
@click.option('--must_arg','-m',required=True)
@click.option('--optional_arg','-o',default="DefaultValue")
def cmd(must_arg,optional_arg):
    # 自身の名前から拡張子を除いてプログラム名(${prog_name})にする
    prog_name = os.path.splitext(os.path.basename(__file__))[0]

    # ロガーの設定

    # フォーマット
    log_format = logging.Formatter("%(asctime)s [%(levelname)8s] %(message)s")
    # レベル
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # 標準出力へのハンドラ
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(log_format)
    logger.addHandler(stdout_handler)
    # ログファイルへのハンドラ
    file_handler = logging.FileHandler(os.path.join(app_home,"log", prog_name + ".log"), "a+")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # 処理開始
    try:
        # ログ出力
        logger.info("start")

        # コマンドライン引数の利用
        logger.error(f"must_arg = {must_arg}")
        logger.error(f"optional_arg = {optional_arg}")

        # ライブラリ呼び出し
        mylib = MyLib()
        logger.info(mylib.get_name())

        # 設定値の利用
        logger.info(MyBatchConf.key1)
        logger.info(MyBatchConf.key2)

        # 例外が発生しても・・・
        raise Exception("My Exception")

    except Exception as e:
        # キャッチして例外をログに記録
        logger.exception(e)
        sys.exit(1)

if __name__ == '__main__':
    cmd()        
```

設定クラス`conf/my_batch_conf.py`の内容

```python
class MyBatchConf(object):
    key1 = "key1_value"
    key2 = True

```
※）以前はconfigParserを利用していましたが、設定クラスの方がパースする必要が無いですし、IDEによる補完が効くため、今は利用しなくなりました。


ライブラリ`my_lib.py`の内容

```python
class MyLib(object):
    def get_name(self):
        return "my_lib"

```

ライブラリの単体テストコード`test_my_lib.py`の内容

```python
import sys,os
import unittest

# ../libをロードパスに入れる
app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(app_home,"lib"))

# ../テスト対象のライブラリのロード
from my_lib import MyLib

class TestMyLib(unittest.TestCase):

    def test_get_name(self):
        ml = MyLib()
        self.assertEqual("my_lib", ml.get_name())

if __name__ == '__main__':
    unittest.main()
```

### 実行

引数を指定しないで実行

```
$ python bin/my_batch.py
```

実行結果（clickの機能によりマニュアルが出る）

```
Usage: my_batch.py [OPTIONS]
Try "my_batch.py --help" for help.

Error: Missing option "--must_arg" / "-m".
```

引数を指定して実行

```
$ python bin/my_batch.py -m SpecifiedValue
```

実行結果

```
2019-06-28 16:42:53,335 [    INFO] start
2019-06-28 16:42:53,335 [   ERROR] must_arg = SpecifiedValue
2019-06-28 16:42:53,335 [   ERROR] optional_arg = DefaultValue
2019-06-28 16:42:53,335 [    INFO] my_lib
2019-06-28 16:42:53,336 [    INFO] key1_value
2019-06-28 16:42:53,336 [    INFO] True
2019-06-28 16:42:53,336 [   ERROR] My Exception
Traceback (most recent call last):
  File "bin/my_batch.py", line 62, in cmd
    raise Exception("My Exception")
Exception: My Exception
```

ログ(log/my_batch.log)にも同じ内容が出力される

```
2019-06-28 16:42:53,335 [    INFO] start
2019-06-28 16:42:53,335 [   ERROR] must_arg = SpecifiedValue
2019-06-28 16:42:53,335 [   ERROR] optional_arg = DefaultValue
2019-06-28 16:42:53,335 [    INFO] my_lib
2019-06-28 16:42:53,336 [    INFO] key1_value
2019-06-28 16:42:53,336 [    INFO] True
2019-06-28 16:42:53,336 [   ERROR] My Exception
Traceback (most recent call last):
  File "bin/my_batch.py", line 62, in cmd
    raise Exception("My Exception")
Exception: My Exception
```

### テスト

単体テストの実行

```
bash-3.2$ python tests/test_my_lib.py
```

実行結果

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

tests以下の全テストコード`test_*.py`をまとめて実行する

```
$ python -m unittest  discover tests "test_*.py"
```
