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


