"""Generator Object Inspection."""


from inspect import isgenerator


g = (i for i in range(0))

print(f'{g} Is Generator? {isgenerator(g)}')
