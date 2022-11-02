import time

timer = time.time()

print(timer)
time.sleep(7.64)

total_timer = time.time() - timer
print(total_timer)

words_per_minute = (len("Every beginning has an end") * 60) / (5 * total_timer)
print(words_per_minute)