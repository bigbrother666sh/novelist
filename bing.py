import os
import sys
import json
from pathlib import Path
import argparse
import asyncio
from EdgeGPT import Chatbot, ConversationStyle


async def novelist(args: argparse.Namespace) -> None:

    bot = await Chatbot.create(proxy=args.proxy, cookies=args.cookies)
    if args.style == "creative":
        generate_list = {"creative": ConversationStyle.creative}
    elif args.style == "balanced":
        generate_list = {"balanced": ConversationStyle.balanced}
    elif args.style == "precise":
        generate_list = {"precise": ConversationStyle.precise}
    else:
        generate_list = {"creative": ConversationStyle.creative, "balanced": ConversationStyle.balanced, "precise": ConversationStyle.precise}

    # load prompts
    with open(args.input, 'r') as f:
        prompts = [line.strip() for line in f.readlines() if line.strip()]

    # load existing data and generate
    print(f"prompts load success and start to generating...")

    f = open(args.output, 'w', encoding='utf-8')
    for prompt in prompts:
        print(f"Prompt in Use: {prompt}")
        f.write(prompt + "\n\n----------------------------------\n")
        for key, conversation_style in generate_list.items():
            f.write(f"style: {key}\n\n")
            result = await bot.ask(prompt=prompt, conversation_style=conversation_style, wss_link=args.wss_link)
            print("generate finished. cool down for 5 seconds...")
            await asyncio.sleep(5)

            if not result:
                print("generate failed, try again...")
                continue

            text = result['item']['messages'][1]['text']
            print(f"generate success: {text}")
            f.write(f"{text}\n\n")
    f.close()
    await bot.close()
    print("finished.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default="input.txt", help="Select the prompt file")
    parser.add_argument('--output', default="result.txt", help="Select the output file")
    # parser.add_argument('--repeat', default=1, help="Select how many times to generate for each example", type=int)
    parser.add_argument('--cookie', default="exported-cookies.json", help="Select the cookie file")
    parser.add_argument(
        "--proxy",
        help="Proxy URL (e.g. socks5://127.0.0.1:1080)",
        type=str,
    )
    parser.add_argument(
        "--wss-link",
        help="WSS URL(e.g. wss://sydney.bing.com/sydney/ChatHub)",
        type=str,
        default="wss://sydney.bing.com/sydney/ChatHub",
    )
    parser.add_argument(
        "--style",
        choices=["creative", "balanced", "precise"],
        default=None,
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"{args.input} not found")

    try:
        args.cookies = json.loads(Path(args.cookie).read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Could not open cookie file: {exc}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(novelist(args))


if __name__ == "__main__":
    main()
