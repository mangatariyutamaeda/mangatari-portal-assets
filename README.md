# mangatari-portal-assets

まんがたりの各ツール(GASウェブアプリほか)が参照する**公開静的アセット**の置き場。

このリポジトリは GitHub Pages(main / ルート)で配信され、公開URLで `.png` などを直接返す。
GASの `HtmlService.setFaviconUrl()` は「拡張子つき画像URLを直接配信」でないと例外になり、
Google Drive の共有URL(uc?export=view / thumbnail / lh3)はリダイレクト・拡張子なしで
**全滅する**(実測)ため、favicon はここから配信している。

## 置いてあるもの

- `portal-favicon.png` … ツールポータルのfavicon(アプリランチャー風の2×2グリッド)。
  参照元: mangatari-portal `src/Config.gs` の `PORTAL_FAVICON_URL`。
  画像の正本は共有Drive(フォルダ 1_BFPjxXrfptobfg3_AcMlxLDsehdL5Pe / portal-favicon.png)。
- `favicon/<ツール名>.png` … **ツールごとのfavicon**(2026-10-14・前田さんの依頼)。
  ポータルと同じ角丸四角に白い1文字。**背景色は系統で分ける**
  (制作=オレンジ `#F06522` / 会計=緑 `#167D50` / 人事=青 `#1E56BE` / その他=灰 `#5A6473`)。
  タブを何本も開いたときに見分けられるようにするため、1文字は重複させない。
  ファイル名は権限管理「ツール」タブのツール名と同じ(日本語キーの
  `まんがたり荘ポータル` だけ `mangatarisou-portal.png` に読み替え)。

## 絵を直したいとき

**正本は `tools/make-favicons.py`**(PNGは生成物)。文字・色・ツールの追加はこのスクリプトを直して回す。

```
python3 tools/make-favicons.py          # favicon/ を作り直す
python3 tools/make-favicons.py --check  # いまのPNGがスクリプトどおりか見るだけ
```

フォントは macOS のヒラギノ角ゴシック W6 を使うので、**MacでしかPNGを作り直せない**
(Linux・GitHub Actions では動かない。見張りたいだけなら `--check` もMacで回す)。

手で描いた画像に差し替えてもよいが、そのときは **TOOLS からその行を外す**こと
(残したままスクリプトを回すと上書きされる)。

## 各ツールからの参照のしかた(GAS)

共通の `Favicon.gs`(正本: `mangatari-ci-common/tools/gas-favicon/Favicon.gs`)を各GASプロジェクトに
置き、`TOOL_FAVICON_URL` にこのリポジトリのURLを入れて `applyFavicon_(out)` を通す。
`setFaviconUrl` は画像を取得できないと **doGet ごと例外にする**ので、必ず共通関数の
try/catch を通すこと(素で呼ぶと画面が真っ白になる)。

公開URL例:
- https://mangatariyutamaeda.github.io/mangatari-portal-assets/portal-favicon.png
- https://mangatariyutamaeda.github.io/mangatari-portal-assets/favicon/manpro-hyoshi.png
