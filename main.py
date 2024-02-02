# We download the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import pingouin

# Read men's and women's datasets(comma sepereted values)
men = pd.read_csv("men_results.csv")
women = pd.read_csv("women_results.csv")

# Filter the data for the time range and tournament (only official FIFA World Cup matches since 2002-01-01)
men["date"] = pd.to_datetime(men["date"])
men_subset = men[(men["date"] > "2002-01-01") & (men["tournament"].isin(["FIFA World Cup"]))]
women["date"] = pd.to_datetime(women["date"])
women_subset = women[(women["date"] > "2002-01-01") & (women["tournament"].isin(["FIFA World Cup"]))]

# Create group and goals_scored columns
men_subset["group"] = "men"
women_subset["group"] = "women"
men_subset["goals_scored"] = men_subset["home_score"] + men_subset["away_score"]
women_subset["goals_scored"] = women_subset["home_score"] + women_subset["away_score"]

# Display information using histograms(for men)
men_subset["goals_scored"].hist()
plt.title("Statistics of men")
plt.xlabel("Total number of goals scored in matches.")
plt.ylabel("Matches have been played with the same number of goals")
plt.show()
plt.clf()

# Display information using histograms(for women)
women_subset["goals_scored"].hist()
plt.title("Statistics of women")
plt.xlabel("Total number of goals scored in matches.")
plt.ylabel("Matches have been played with the same number of goals")
plt.show()
plt.clf()


# merging data on men and women and calculate goals scored in each match
both = pd.concat([women_subset, men_subset], axis=0, ignore_index=True)

# Transform the data for the pingouin Wilcoxon-Mann-Whitney
both_subset = both[["goals_scored", "group"]]
both_subset_wide = both_subset.pivot(columns="group", values="goals_scored")

# Perform right-tailed Wilcoxon-Mann-Whitney test with pingouin
results_pg = pingouin.mwu(x=both_subset_wide["women"],
                          y=both_subset_wide["men"],
                          alternative="greater")

# Extract p-value as a float
p_val = results_pg["p-val"].values[0]

# Determine hypothesis test result using sig. level. (Used a 10% significance level.)
if p_val <= 0.1:
    result = "Hypothesis rejected, there is a difference in medians between the two groups."
else:
    result = "Hypothesis accepted."

result_dict = {"p_val": p_val, "result": result}
print()
print(result_dict)
print()