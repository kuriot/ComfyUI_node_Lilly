import glob, sys
import random
import re
import os

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
    card_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "wildcards", "**", "*.txt"
    )

    print(f"wildcards card_path : ", card_path, style="bold CYAN")

    resub = re.compile(
        r"(\{)(((\d+)|(\d+)?-(\d+)?)?\$\$(([^\{\}]*?)\$\$)?)?([^\{\}]*)(\})"
    )
    recard = re.compile(r"(__)(.*?)(__)")

    # List of cards
    is_card_Load = False
    cards = {}
    seperator = ", "
    loop_max = 50

    # Fetch
    def sub(match):
        try:
            # m=match.group(2)
            seperator = wildcards.seperator
            s = match.group(3)
            m = match.group(9).split("|")
            p = match.group(8)
            if p:
                seperator = p

            if s is None:
                return random.choice(m)
            c = len(m)
            n = int(match.group(4)) if match.group(4) else None
            if n:
                r = seperator.join(random.sample(m, min(n, c)))

                return r

            n1 = match.group(5)
            n2 = match.group(6)

            if n1 or n2:
                a = min(int(n1 if n1 else c), int(n2 if n2 else c), c)
                b = min(max(int(n1 if n1 else 0), int(n2 if n2 else 0)), c)

                r = seperator.join(random.sample(m, random.randint(a, b)))
                # n1=int(match.group(5)) if not match.group(5) is None
                # n2=int(match.group(6)) if not match.group(6) is None
            else:
                r = seperator.join(random.sample(m, random.randint(0, c)))

            return r

        except Exception as e:
            console.print_exception()
            return ""

    # Loop wildcards
    def sub_loop(text):
        bak = text
        for i in range(1, wildcards.loop_max):
            tmp = wildcards.resub.sub(wildcards.sub, bak)

            if bak == tmp:
                return tmp
            bak = tmp
        return bak

    # Retrieve from among the cards.
    def card(match):
        if match.group(2) in wildcards.cards:
            r = random.choice(wildcards.cards[match.group(2)])
        else:
            r = match.group(2)

        return r

    # Repeat the process of retrieving from among the cards. Also handle the ones separated by |.
    def card_loop(text):
        bak = text
        for i in range(1, wildcards.loop_max):
            tmp = wildcards.recard.sub(wildcards.card, bak)

            if bak == tmp:
                tmp = wildcards.sub_loop(tmp)

            if bak == tmp:
                return tmp
            bak = tmp

        return bak

    # Read card file
    def card_load():
        card_path = wildcards.card_path
        cards = {}

        files = glob.glob(card_path, recursive=True)

        for file in files:
            basename = (
                os.path.relpath(file, os.path.dirname(__file__))
                .replace("\\", "/")
                .replace("../../wildcards/", "")
            )
            file_name = os.path.splitext(basename)[0]

            if not file_name in cards:
                cards[file_name] = []

            f = open(file, "r", encoding="unicode_escape")
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                # Exclude comments and empty lines
                if line.startswith("#") or len(line) == 0:
                    continue
                cards[file_name] += [line]

        wildcards.cards = cards
        print(f"[cyan]cards file count : [/cyan]", len(wildcards.cards))

        wildcards.is_card_Load = True

    # Execute
    def run(text, load=False):
        if text is None or type(text) is not str:
            print("[red]text is not str : [/red]", text)
            return None
        if not wildcards.is_card_Load or load:
            wildcards.card_load()

        result = wildcards.card_loop(text)

        return result


# ============================================================


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
print("wildcards test : " + wildcards.run("__haircolor__"))
print("wildcards test : " + wildcards.run("__sad/haircolor__"))
print("wildcards test : " + wildcards.run("__sad/asw/haircolor__"))
