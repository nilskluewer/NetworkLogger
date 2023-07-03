import speedtest

s = speedtest.Speedtest()

print(s.download())
print(s.upload())
