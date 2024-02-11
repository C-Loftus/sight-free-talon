import os

from talon import Context, Module, actions, cron

ctx = Context()

mod = Module()
mod.tag("openai_defined", desc="The user has a valid openai API key")

# TODO Check if there's a better way to do this other than updating on an interval
####################################################################

#  perhaps there's some sort of callback?
# def check_openai():
#     if os.getenv("OPENAI_API_KEY"):
#         ctx.tags = ["user.openai_defined"]
#     else:
#         ctx.tags = []

if os.getenv("OPENAI_API_KEY"):
    ctx.tags = ["user.openai_defined"]
else:
    ctx.tags = []

# cron.interval("15s", check_openai)
