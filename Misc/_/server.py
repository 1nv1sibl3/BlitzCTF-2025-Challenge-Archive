import random

flag = "Blitz{X723M3_73MP3247U23!!!}"

seed = "bl175_h4ck_rul35!!!"
random.seed(seed)

indexes = [i for i in range(len(flag))]
random.shuffle(indexes)

def shuffle(s):
    return ''.join(s[index] for index in indexes)

rule_1 = "ONLY 🧊 OR 🔥 !!!"
rule_2 = "LENGTH MUST BE " + str(len(flag)) + " !!!"
rule_3 = "🧊 COUNT MUST BE EQUAL TO 🔥 COUNT !!!"

print("FLAG:", shuffle(flag))
print("🥶🥵🥶🥵🥶🥵")
print("RULE 1:", rule_1)
print("RULE 2:", rule_2)
print("RULE 3:", rule_3)


while True:
    emojis = input("GIVE INPUT!!! ")

    # validate character
    if any(c not in ('🔥', '🧊') for c in emojis):
        print(rule_1)

        continue

    # validate length
    if len(emojis) != len(flag):
        print(rule_2)

        continue

    # Validation 3: balance fire and ice
    ice_count = emojis.count('🧊')
    fire_count = emojis.count('🔥')
    if ice_count != fire_count:
        print(rule_3)

    if ice_count > fire_count:
        print("TOO COLD!!! 🥶🥶🥶")

        continue

    if fire_count > ice_count:
        print("TOO HOT!!! 🥵🥵🥵")

        continue

    print("TAKE OUTPUT!!!", shuffle(emojis))
