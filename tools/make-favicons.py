#!/usr/bin/env python3
"""ツールごとの favicon を作る（2026-10-14・前田さんの依頼「各ツールに favicon 対応」）。

  python3 tools/make-favicons.py            # favicon/ を作り直す
  python3 tools/make-favicons.py --check    # 作り直さず、いまの PNG と同じになるかだけ見る（CI向け）

**絵の正本はこのスクリプト。** PNG は生成物なので、直したいときは下の TOOLS を直して回す。
手で画像を差し替えてもよいが、そのときはこのスクリプトを回さないこと（上書きされる）。

見た目（前田さんが選んだ案・2026-10-14）:
  ポータルと同じ角丸四角 + 白い1文字。**背景色は系統で分ける**
  （制作＝オレンジ / 会計＝緑 / 人事＝青 / その他＝灰）。
  16px まで縮むので **1文字だけ**。2文字にすると潰れて見分けがつかない。

フォントは macOS のヒラギノ（メインPC・サブPCともにある）。Linux では動かないので、
CI で回すなら `--check` も含めて動かさない。
"""
import argparse
import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(HERE), 'favicon')
FONT_PATH = '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'
SIZE = 256
RADIUS = 56  # portal-favicon.png と同じくらいの丸み

# 系統ごとの色。白文字とのコントラストは 4.5:1 以上（WCAG AA）を満たすものだけ使う
COLORS = {
    '制作': (240, 101, 34),   # #F06522 まんがたりのブランド色（ポータルと同じ）
    '会計': (22, 125, 80),    # #167D50
    '人事': (30, 86, 190),    # #1E56BE
    'その他': (90, 100, 115),  # #5A6473
}

# key（ポータル＝権限管理「ツール」タブのツール名）, 1文字, 系統, 日本語名（覚え書き）
TOOLS = [
    ('manpro-hyoshi',               '表', '制作', 'まんプロ 表紙依頼管理'),
    ('manpro-schedule',             '程', '制作', 'まんプロ スケジュール管理'),
    ('manpro-assign',               'ア', '制作', 'まんプロ 作家アサイン'),
    ('manpro-kickoff',              '立', '制作', 'まんプロ プロジェクト立ち上げ'),
    ('delay-notifier',              '遅', '制作', 'まんプロ 遅延通知'),
    ('manga_copyright_tool',        '著', '制作', '著作権表記 焼き込み'),
    ('manga-koshi-anken',           '講', '制作', 'マンガ講師派遣 案件管理'),
    ('aichara_gas',                 'キ', '制作', 'アイキャラ 案件管理'),
    ('letterpack-tracker',          'レ', '制作', 'レターパック伝票スキャナ'),
    ('mangatari-event-hub',         '催', '制作', 'イベント管理'),

    ('mangatari_accounting',        '会', '会計', '作品別 管理会計'),
    ('mangatari-zensha-accounting', '全', '会計', '全社 管理会計（PL）'),
    ('freee-tax-linker',            '証', '会計', 'freee 証憑未添付リスト'),
    ('sakibarai_gas',               '先', '会計', '先払い申請'),
    ('payment-checker',             '払', '会計', '支払いチェッカー'),

    ('mangatari-access-hub',        '権', '人事', 'ツール権限管理'),
    ('mangatari-people-hub',        '社', '人事', '社員情報ハブ'),
    ('mangatari_gift',              '贈', '人事', '作家 贈答管理'),
    ('まんがたり荘ポータル',          '荘', '人事', 'まんがたり荘ポータル'),
    ('FocusCraft',                  'F',  '人事', 'タスク・予実管理'),

    ('genko-size-checker',          '原', 'その他', '原稿サイズチェッカー'),
    ('gappon-checker',              '台', 'その他', '合本版 台割チェック'),
    ('gappon-maker',                '進', 'その他', '合本版 進行管理'),
    ('author_work_catalog',         '作', 'その他', '作家・作品カタログ'),
    ('partner_directory',           '協', 'その他', '協力パートナー名簿'),
    ('mangatari-business-hub',      '取', 'その他', '取引先・作品マスタ'),
    ('get_rank',                    'ラ', 'その他', '電子書店ランキング'),
    ('mangatari-tweet-gen',         'X',  'その他', 'X ツイート文面'),
    ('manga-b2b-archive',           'B',  'その他', 'マンガ業界B2Bアーカイブ'),
    ('slack-stale-alert',           '放', 'その他', 'Slack放置検知'),
]

# ファイル名に使えない・URLで困る文字を落とす（日本語キーは英字名に読み替える）
FILENAME = {'まんがたり荘ポータル': 'mangatarisou-portal'}


def filename_for(key):
    return FILENAME.get(key, key) + '.png'


def render(glyph, category):
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=RADIUS, fill=COLORS[category] + (255,))
    # 1文字が枠に対して大きすぎると潰れる。英数字は字面が小さいので少し大きくする
    ascii_only = all(ord(c) < 128 for c in glyph)
    font = ImageFont.truetype(FONT_PATH, 190 if ascii_only else 158)
    box = d.textbbox((0, 0), glyph, font=font)
    x = (SIZE - (box[2] - box[0])) / 2 - box[0]
    y = (SIZE - (box[3] - box[1])) / 2 - box[1]
    d.text((x, y), glyph, font=font, fill=(255, 255, 255, 255))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='作り直さず、いまの PNG と同じかだけ見る')
    args = ap.parse_args()

    keys = [t[0] for t in TOOLS]
    assert len(keys) == len(set(keys)), 'キーが重複しています'
    names = [filename_for(k) for k in keys]
    assert len(names) == len(set(names)), 'ファイル名が重複しています'

    os.makedirs(OUT_DIR, exist_ok=True)
    drift = []
    for key, glyph, category, label in TOOLS:
        path = os.path.join(OUT_DIR, filename_for(key))
        img = render(glyph, category)
        buf = io.BytesIO()
        img.save(buf, 'PNG')
        want = buf.getvalue()
        if args.check:
            have = open(path, 'rb').read() if os.path.exists(path) else b''
            if have != want:
                drift.append(filename_for(key))
            continue
        with open(path, 'wb') as f:
            f.write(want)
        print('%-34s %s  %s（%s）' % (filename_for(key), glyph, label, category))

    if args.check:
        if drift:
            print('スクリプトと中身が違う PNG: ' + ', '.join(drift), file=sys.stderr)
            return 1
        print('OK: %d 件ともスクリプトどおり' % len(TOOLS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
