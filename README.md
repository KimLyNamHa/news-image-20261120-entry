# news-image-20261120-entry

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/KimLyNamHa/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/KimLyNamHa/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A program that draws the world news of Friday 20 November 2026 into one 1024×1024 image — 35 stories on one newspaper front page, drawn programmatically with PIL (`draw_poster_v2.py`).

The page follows the day in order: overnight missiles hit three Kyiv bridges, Cyclone Akvan comes ashore near Gopalpur at 08:30, then Asia's markets sink in the AI sell-off. Below that are ten more stories — COP31's last day with no deal, the UK–EU reset, a Russian missile landing in Poland, Iraq's army entering Jurf al-Sakhar, Italy's general strike, Japan's 2.3% inflation, BepiColombo arriving at Mercury, China holding its lending rates, Kenya drilling its first oil well, and Glenn Phillips' 118 against India — plus 22 one-line briefs and a world map marking where each story happened.

A red DATE CHECK box lists the big Thursday 19 November stories that are deliberately left out as Friday news: the World Court ruling on Myanmar, the three-leader Shenzhen declaration, Anthropic's $83 IPO pricing, the Houthi strike on Riyadh's PIF Tower, the GTA VI launch and the $190.4m Van Gogh sale. Every story on the page happened, or was first reported, on Friday 20 November 2026, with its source named beside it. All drawings are original vector-style art made by the script; no photos or other entries' images are used.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To redraw the image after changing a story, run `python3 draw_poster_v2.py` first.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qmq06e6v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
