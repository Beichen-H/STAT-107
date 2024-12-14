import pandas as pd
import random

data = []
for i in range(200000):
  supports_kingfisther = 0
  follows_datascienceduo = 0
  datascience_major = 0

  if (i % 100) < 70:
    supports_kingfisther = 1

  if (i % 100) < 52:
    follows_datascienceduo = 1

  if (i % 100) < 48:
    datascience_major = 1

  d = {
    "DSmajor": datascience_major,
    "FollowsDuo": follows_datascienceduo,
    "ProKingfisher": supports_kingfisther,
  }
  data.append(d)

df = pd.DataFrame(data)
df

sampleSize = random.randint(40, 60)
sampleSize2 = 1000 + random.randint(0, 100)
turnOut = random.randint(18, 22)

sample = df.sample(n=sampleSize)
sample2 = df.sample(n=sampleSize2)
sample3 = df.sample(frac=turnOut / 100)

def getSample():
  return sample

def getExpensiveSample():
  return sample2

def electionDay():
  print(f"The election was held and {turnOut}% of the population voted.")
  print()
  print("== Kingfisher Support ==")
  kf = sum(sample3.ProKingfisher)
  kf_pct = kf / len(sample3)
  print(f"SUPPORT KINGFISHER: {kf} {round(kf_pct * 100, 2)}%")
  kf = len(sample3) - sum(sample3.ProKingfisher)
  kf_pct = kf / len(sample3)
  print(f"OPPOSE KINGFISHER : {kf} {round(kf_pct * 100, 2)}%")
  print()
  print("== Follows @datascienceduo ==")
  kf = sum(sample3.FollowsDuo)
  kf_pct = kf / len(sample3)
  print(f"FOLLOWS DUO    : {kf} {round(kf_pct * 100, 2)}%")
  kf = len(sample3) - sum(sample3.FollowsDuo)
  kf_pct = kf / len(sample3)
  print(f"DOES NOT FOLLOW: {kf} {round(kf_pct * 100, 2)}%")


