import re

numbers = re.compile(r'(\d+)')
floating = re.compile(r"(?i)chapter ([-+]?\d*\.\d+|\d+)")

floating_matcher = re.compile(r"([-+]?\d*\.\d+|\d+)")
