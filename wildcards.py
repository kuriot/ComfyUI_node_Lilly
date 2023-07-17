import random
import re
import os
import chardet

if (
    __name__ == os.path.splitext(os.path.basename(__file__))[0]
    or __name__ == "__main__"
):
    from ConsoleColor import print, console, ccolor
else:
    from .ConsoleColor import print, console, ccolor


# ============================================================


class wildcards:
    # List of files to be imported
    directory = os.path.join(os.path.dirname(__file__), "..", "..", "wildcards")
    file_extension = "txt"

    print("wildcard files path : ", directory, style="bold CYAN")

    resub = re.compile(
        r"(\{)(((\d+)|(\d+)?-(\d+)?)?\$\$(([^\{\}]*?)\$\$)?)?([^\{\}]*)(\})"
    )

    # List of cards
    # is_card_Load = False
    cards = {}
    separator = ", "
    loop_max = 50

    # Fetch
    def sub(match):
        try:
            # m=match.group(2)
            separator = wildcards.separator
            s = match.group(3)
            m = match.group(9).split("|")
            p = match.group(8)

            if p:
                separator = p

            if s is None:
                return random.choice(m)
            c = len(m)
            n = int(match.group(4)) if match.group(4) else None
            if n:
                r = separator.join(random.sample(m, min(n, c)))

                return r

            n1 = match.group(5)
            n2 = match.group(6)

            if n1 or n2:
                a = min(int(n1 if n1 else c), int(n2 if n2 else c), c)
                b = min(max(int(n1 if n1 else 0), int(n2 if n2 else 0)), c)

                r = separator.join(random.sample(m, random.randint(a, b)))
            else:
                r = separator.join(random.sample(m, random.randint(0, c)))

            return r

        except Exception as e:
            console.print_exception()
            return ""

    # Repeat the process of retrieving from among the cards. Also handle the ones separated by |.
    def card_loop(text):
        bak = text
        for i in range(1, wildcards.loop_max):
            tmp = wildcards.resub.sub(wildcards.sub, bak)

            if bak == tmp:
                return tmp
            bak = tmp
        return bak

    # Execute
    def run(input_text, load=False):
        text = input_text

        if text is None or not isinstance(text, str):
            print("[red]text is not str : [/red]", text)
            return None

        matches = re.findall(r"__(.*?)__", text)

        for match in matches:
            card_file = f"{wildcards.directory}/{match}.{wildcards.file_extension}"
            try:
                with open(card_file, "rb") as f:
                    raw_data = f.read()
                    encoding = chardet.detect(raw_data)["encoding"]

                with open(card_file, "r", encoding=encoding) as f:
                    lines = [
                        line.strip()
                        for line in f
                        if line.strip() and not line.startswith("#")
                    ]
                    if lines:
                        random_line = random.choice(lines)
                        text = re.sub(f"__{match}__", random_line, text, count=1)

            except (FileNotFoundError, IOError) as error:
                print(f"Error reading file {card_file}: {error}")

        result = wildcards.card_loop(text)

        return result


# m = p.sub(sub, test)
# print(m)
# print(__name__)
# if __name__ == '__main__' :
# 테스트용
# test="{3$$a1|{b2|c3|}|d4|{-$$|f|g}|{-2$$h||i}|{1-$$j|k|}}/{$$l|m|}/{0$$n|}/{9$$-$$a|b|c}/{9$$ {and|or} $$a|b|c}"
# print("[green]wildcards test : [/green]",wildcards.run(test),style="reset")
# print("wildcards test : "+wildcards.run("{9$$a|b}"))
# print("[green]wildcards test : [/green]",wildcards.run("__my__"))
# print("wildcards test : "+wildcards.run("{9$$-$$a|b|c}"))
# print("wildcards test : "+wildcards.run("{9$$ {and|or} $$a|b|c}"))
# print("wildcards test : "+wildcards.run("{{slender,|} {nature,|} {curvy,|} {thin,|} {narrow,|} {slim,|} {mini,|} {little,|}| {|very }{-$$ $$thin|slender|narrow|slim|little|skinny|mini} body, }"))
