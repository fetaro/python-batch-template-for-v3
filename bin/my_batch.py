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