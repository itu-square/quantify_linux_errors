import kconfiglib


conf = kconfiglib.Config("linux-3.19/Kconfig_concat", "linux-3.19")
# conf.load_config("/tmp/randconfigs/7")

top = conf.get_top_level_items()
syms = conf.get_symbols()

print len(syms)

for sym in syms:
    pass
    
        

print len(syms)


