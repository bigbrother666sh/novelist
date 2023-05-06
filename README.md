# novelist
A series of data generation tools based on LLM...

## bing

use bing api to get data and writing data to file

usage:

```shell
python -m pip install EdgeGPT --upgrade
```

** sometime you need update prompt_toolkit manually **

```shell
python -m pip install prompt_toolkit --upgrade
```

for more information, see [EdgeGPT](https://github.com/acheong08/EdgeGPT/blob/master/docs/README_zh-cn.md)

```shell
python bing.py --input "input.txt" --output "output.txt" --cookie "cookie file path"
```

input file: prompts file, each line is a prompt, in a txt format

output file: result file,  in a txt format

cookie file: your cookie file, if you don't know what's it check here [EdgeGPT](https://github.com/acheong08/EdgeGPT/blob/master/docs/README_zh-cn.md)

--proxy  whether use proxy, (e.g. socks5://127.0.0.1:1080)

--style  Whether to specify a specific generation style, if not, then generate each prompt in three styles: creative, balanced, and strict
