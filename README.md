# python3系のバッチスクリプトの雛形 

### 概要

これはPython3系(3.3以降)でバッチ処理を書く場合のテンプレートです。

以下の機能を提供しています。

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
       │   └  my_lib.py      #←ライブラリ
       ├ tests/        
       │   └  test_my_lib.py #←単体テストコード
       ├ log/                #←ログ出力先
       └ Pipfile             #←使うライブラリを列挙
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
$ python tests/test_my_lib.py
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
