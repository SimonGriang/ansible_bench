import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../../test_report/overall_report.csv", delimiter=";")

print(df.describe())

print("Yamllint-Failure-Rate:", df["Yamllint failed"].mean())
print("Ansiblelint-Failure-Rate:", df["Ansiblelint failed"].mean())

print(df.corr(numeric_only=True))

#print(df.groupby("referenced task files (yes/no)")["Molecule failed"].mean())

df.plot.scatter(x="File size (chars)", y="Yamllint failed")
plt.title("Zusammenhang: Dateigröße vs. Yamllint-Fehler")
plt.xlabel("Dateigröße (Zeichen)")
plt.ylabel("Yamllint-Fehler")

plt.tight_layout()
plt.savefig("plot_yamllint_vs_size.png", dpi=300)
print("Plot gespeichert als plot_yamllint_vs_size.png")