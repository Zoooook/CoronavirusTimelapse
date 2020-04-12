This uses [New York Times data](https://github.com/nytimes/covid-19-data) to build timelapse videos for various metrics of the Coronavirus spread across the U.S., using a map format modified from an old version of [their page](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html). The areas of the circles are proportional to the number of people represented, although the scale differs between different videos. The data of course only represent confirmed cases and deaths, not true cases and deaths.

To run this locally you'll need the [Chrome driver](https://chromedriver.chromium.org/downloads) and [ffmpeg](https://www.ffmpeg.org/download.html) on your path, and Chrome installed in the default location. It renders individual frames in html so it takes a while to run the first time. On subsequent runs it only updates frames with diffs. It should be safe to kill the script while it's working and then start it again later. You can comment out lines in `types` to skip generating particular videos.