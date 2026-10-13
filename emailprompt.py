# -*- coding: utf-8 -*-
"""emailprompt - fill in a ready-made client-email prompt, then paste it into any AI chat assistant.

Standard library only. No network access. Reads/writes nothing unless you ask:
  --voice FILE  reads your Voice Block (text file)
  --out FILE    writes the finished prompt (refuses to overwrite an existing file unless --force)

Examples:
  python emailprompt.py list
  python emailprompt.py show invoice-nudge
  python emailprompt.py fill invoice-nudge --set "CLIENT FIRST NAME=Jonas" --set "AMOUNT=EUR 1,200"
  python emailprompt.py fill invoice-firm --ask --voice my_voice.txt
"""
import argparse
import os
import re
import sys

PROMPTS = {
    "voice-finder": (
        "Step 0: find your writing voice (do this once)",
        "Here are three emails I wrote to clients:\n\n[EMAIL 1]\n\n[EMAIL 2]\n\n[EMAIL 3]\n\n"
        "Describe my writing voice as a short style guide of at most 8 bullet points: sentence length, "
        "formality, greeting and sign-off habits, typical phrases, what I never do. "
        "Write it so I can paste it in front of future prompts as a 'Voice Block'.",
    ),
    "invoice-friendly": (
        "Friendly heads-up before an invoice is due",
        "Write a short, friendly email to [CLIENT FIRST NAME] reminding them that invoice [INVOICE NUMBER] "
        "for [AMOUNT] is due on [DUE DATE]. Include how to pay: [PAYMENT DETAILS]. Tone: warm, zero pressure, "
        "like a helpful note from a colleague. Max 70 words, plain text, no exclamation marks.",
    ),
    "invoice-nudge": (
        "First nudge: invoice just past due",
        "Write a brief, kind email to [CLIENT FIRST NAME]. Invoice [INVOICE NUMBER] ([AMOUNT]) was due on "
        "[DUE DATE] and I have not seen the payment yet. Assume it is an oversight. Ask them to let me know if "
        "anything is blocking it. Say the invoice is attached again for convenience. "
        "Tone: relaxed and professional. Max 80 words.",
    ),
    "invoice-firm": (
        "Firm but respectful reminder at 14+ days overdue",
        "Write a firm but respectful email to [CLIENT FIRST NAME]. Invoice [INVOICE NUMBER] for [AMOUNT] is "
        "[NUMBER OF DAYS] days overdue after reminders on [DATE 1] and [DATE 2]. State the facts in three short "
        "sentences, ask for payment by [DEADLINE DATE], and say that if there is a problem with the invoice I "
        "want to hear it now. Do not threaten. Max 110 words.",
    ),
    "scope-creep": (
        "Politely park an extra request outside the agreed scope",
        "Write an email to [CLIENT FIRST NAME]. They asked for [EXTRA REQUEST], which is not part of what we "
        "agreed for [PROJECT]: [AGREED SCOPE IN ONE LINE]. Thank them for the idea, say plainly that it is "
        "outside the current scope, and offer two options: add it as a separate item (I will send a quote by "
        "[QUOTE DATE]) or keep it for a later phase. Friendly, no blame, no apology. Max 110 words.",
    ),
    "say-no": (
        "Decline a project politely",
        "Write a short, kind email declining the project '[PROJECT NAME]' offered by [CLIENT FIRST NAME]. "
        "Reason (keep it brief and true): [REASON]. Thank them for thinking of me, and if useful suggest "
        "[ALTERNATIVE, e.g. a colleague or a later start date]. Leave the door open. Max 90 words.",
    ),
}

PH = re.compile(r"\[([A-Z][A-Z0-9 _]*)\]")


def norm(key):
    return re.sub(r"\s+", " ", key.replace("_", " ").strip()).upper()


def placeholders(text):
    seen = []
    for m in PH.finditer(text):
        if m.group(1) not in seen:
            seen.append(m.group(1))
    return seen


def get(pid):
    if pid not in PROMPTS:
        sys.exit("Unknown prompt id '%s'. Run: python emailprompt.py list" % pid)
    return PROMPTS[pid]


def read_text(path):
    if not os.path.isfile(path):
        sys.exit("File not found: %s" % path)
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def cmd_list(_a):
    for pid, (title, _t) in PROMPTS.items():
        print("%-18s %s" % (pid, title))
    print("\nFull kit: 60 prompts in 8 situations - see README.")


def cmd_show(a):
    title, text = get(a.id)
    print(title + "\n")
    print(text + "\n")
    print("Placeholders: " + ", ".join(placeholders(text)))


def cmd_fill(a):
    title, text = get(a.id)
    values = {}
    for item in a.set or []:
        if "=" not in item:
            sys.exit("--set needs KEY=VALUE, got: %s" % item)
        k, v = item.split("=", 1)
        values[norm(k)] = v.strip()
    if a.ask:
        for ph in placeholders(text):
            if norm(ph) not in values:
                ans = input("%s: " % ph).strip()
                if ans:
                    values[norm(ph)] = ans
    result = PH.sub(lambda m: values.get(norm(m.group(1)), m.group(0)), text)
    if a.voice:
        result = "My writing voice (follow it closely):\n" + read_text(a.voice) + "\n\n" + result
    left = placeholders(result)
    if a.out:
        if os.path.exists(a.out) and not a.force:
            sys.exit("Refusing to overwrite %s (use --force)." % a.out)
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(result + "\n")
        print("Written: " + a.out)
    else:
        print(result)
    if left:
        sys.stderr.write("\nStill to fill: " + ", ".join(left) + "\n")
    sys.stderr.write("Reminder: check names, amounts and dates before sending. Do not paste secrets into a chat.\n")


def main():
    ap = argparse.ArgumentParser(description="Fill client-email prompts for AI chat assistants.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="list prompt ids").set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help="show one prompt")
    s.add_argument("id")
    s.set_defaults(fn=cmd_show)
    f = sub.add_parser("fill", help="fill placeholders and print the prompt")
    f.add_argument("id")
    f.add_argument("--set", action="append", metavar="KEY=VALUE", help="placeholder value (repeatable)")
    f.add_argument("--ask", action="store_true", help="ask for missing values interactively")
    f.add_argument("--voice", metavar="FILE", help="text file with your Voice Block, prepended to the prompt")
    f.add_argument("--out", metavar="FILE", help="write result to a file instead of printing")
    f.add_argument("--force", action="store_true", help="allow overwriting --out")
    f.set_defaults(fn=cmd_fill)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
