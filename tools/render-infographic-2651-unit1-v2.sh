#!/bin/bash
# Re-render the tree-style Unit 1 infographic (HTML/SVG -> PNG via headless Chrome).
# Chrome Headless Shell 157 lives in ~/workspace/.chrome-headless-shell/
CH=~/workspace/.chrome-headless-shell/chrome-headless-shell-linux64/chrome-headless-shell
"$CH" --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1080,1840 \
  --screenshot=db/images/2651-unit1-bhasha-infographic.png \
  file://$PWD/tools/infographic-2651-unit1-v2.html
