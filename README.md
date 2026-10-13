# Freelancer Email Prompts Lite

**Turn an awkward client email into a ready-to-paste AI prompt in 30 seconds.**

A tiny offline command-line tool with 6 ready-made prompt templates for the emails freelancers dread:
three steps of the unpaid-invoice ladder, scope creep, declining a project, and a one-time "find my writing voice" prompt.
It fills the `[PLACEHOLDERS]`, optionally puts your Voice Block in front, and prints a prompt for ChatGPT, Claude, Gemini or any chat assistant.

## What it does

- `list` shows the 6 prompts, `show` displays one with its placeholders.
- `fill` replaces placeholders from `--set KEY=VALUE` or by asking you (`--ask`), and tells you what is still missing.
- `--voice FILE` prepends your saved Voice Block so the email sounds like you.
- Prints to the screen by default. `--out FILE` writes one file and refuses to overwrite unless `--force`.
- No network, no telemetry, no deletes, nothing else is read or written.

## Quick start

```bash
python emailprompt.py list
python emailprompt.py fill invoice-nudge --set "CLIENT FIRST NAME=Jonas" --set "INVOICE NUMBER=2026-031" --set "AMOUNT=EUR 1,200" --set "DUE DATE=14 June"
```

Copy the printed text into your AI assistant, read the draft aloud, check names, amounts and dates, then send.

Interactive, with your voice:

```bash
python emailprompt.py fill invoice-firm --ask --voice my_voice.txt
```

To create `my_voice.txt`: run `python emailprompt.py fill voice-finder --ask`, give it three emails you wrote, paste the result into the assistant, and save the answer.

## Requirements

- Python 3.8+ (standard library only), plus any AI chat assistant (free tiers work).
- Do not paste confidential client data, passwords or bank details into a chat.

## Notes

This helps with wording only. Late fees, interest and notice periods depend on your contract and local rules. AI output varies, so always review before sending.

Created with AI assistance by an automated system.

## Full version

The free tool covers 6 prompts. The full **Freelancer Client Email Prompt Pack** adds:

- 60 prompts in 8 situations (the complete 10-step invoice ladder, price increases, proposal follow-ups, late feedback, testimonials and referrals, project wrap-up, and more),
- two tone variants and an example output for every prompt,
- a formatted PDF, a one-page Quick-Start and plain-text copies for easy copy and paste.

It is a paid product, with a 30-day refund promise: https://kontor7-agent.github.io/p/freelancer-client-email-prompt-pack?s=github

Released under the MIT licence (see `LICENSE`).
