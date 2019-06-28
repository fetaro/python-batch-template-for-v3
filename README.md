この雛形では以下のことをしています。

* コマンドライン引数のパース
* 設定ファイル読み込み
* ログ出力
* ライブラリ読み込み

ファイルの配置

```
app_home/
       ├ bin/
       │   └  my_batch.py   #←実行するスクリプト
       ├ conf/
       │   └  my_batch.conf #←設定ファイル
       ├ lib/
       │   ├  __init__.py   #←モジュールをロードするのに必要
       │   └  my_lib.py     #←ライブラリ
       ├ tests/        
       │   └  test_my_lib.py#←単体テストコード
       └ log/               #←ログ出力先
```


my_batch.pyの内容

```py
import sys
import os
from configparser import ConfigParser
import click
import logging

# 親ディレクトリをアプリケーションのホーム(${app_home})に設定
app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
# ${app_home}/libをライブラリロードパスに追加
sys.path.append(os.path.join(app_home,"lib"))

# 自前のライブラリをロード
from my_lib import MyLib

# コマンドライン引数のハンドリング. must_argは必須オプション、optional_argは任意オプション
@click.command()
@click.option('--must_arg','-m',required=True)
@click.option('--optional_arg','-o',default="DefaultValue")
def cmd(must_arg,optional_arg):
    # 自身の名前から拡張子を除いてプログラム名(${prog_name})にする
    prog_name = os.path.splitext(os.path.basename(__file__))[0]

    # 設定ファイルを読む
    config = ConfigParser()
    conf_path = os.path.join(app_home,"conf", prog_name + ".conf")
    config.read(conf_path)

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

        # 設定値読み込み
        logger.info(config.get("section1","key1"))
        logger.info(config.getboolean("section2","key2"))

        # 例外が発生しても・・・
        raise Exception("My Exception")

    except Exception as e:
        # キャッチして例外をログに記録
        logger.exception(e)
        sys.exit(1)

if __name__ == '__main__':
    cmd()
        
```

my_batch.confの内容

```
[section1]
key1  = key1_value

[section2]
key2 = true
```

my_lib.pyの内容

```py
class MyLib(object):
    def get_name(self):
        return "my_lib"

```

実行結果

引数を指定しないとclickの機能によりマニュアルが出る

```
bash-3.2$ python bin/my_batch.py
Usage: my_batch.py [OPTIONS]
Try "my_batch.py --help" for help.

Error: Missing option "--must_arg" / "-m".
```

引数を指定して実行

```
bash-3.2$ python bin/my_batch.py -m SpecifiedValue
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

ログ(log/my_batch.log)の内容

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


単体テストコード`test_my_lib.py`の内容

```py
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

単体テストの実行結果

```
bash-3.2$ python tests/test_my_lib.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

tests以下の全テストコード`test_*.py`をまとめてテストする場合

```
bash-3.2$ python -m unittest  discover tests "test_*.py"
```


