# mangatari-portal-assets

mangatari-portal(GASウェブアプリ)が参照する**公開静的アセット**の置き場。

このリポジトリは GitHub Pages(main / ルート)で配信され、公開URLで `.png` などを直接返す。
GASの `HtmlService.setFaviconUrl()` は「拡張子つき画像URLを直接配信」でないと例外になり、
Google Drive の共有URLでは弾かれるため、favicon等はここから配信している。

- `portal-favicon.png` … ポータルのブラウザタブfavicon(まんがたりロゴ風)。
  参照元: mangatari-portal `src/Config.gs` の `PORTAL_FAVICON_URL`。
  画像の正本は共有Drive(フォルダ 1_BFPjxXrfptobfg3_AcMlxLDsehdL5Pe / portal-favicon.png)。

公開URL例: https://mangatariyutamaeda.github.io/mangatari-portal-assets/portal-favicon.png
