import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

xPoints = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
y1Points = np.array([12, 14, 16, 18, 10, 12, 14, 16, 18, 120])
y2Points = np.array([12, 7, 6, 5, 4, 3, 2, 2, 1, 12])

plt.subplot(1, 2, 1) # row 1, col 2 index 1
plt.plot(xPoints, y1Points)
plt.title("My first plot!")
plt.xlabel('X-axis ')
plt.ylabel('Y-axis ')

plt.subplot(1, 2, 2) # index 2
plt.plot(xPoints, y2Points)
plt.title("My second plot!")
plt.xlabel('X-axis ')
plt.ylabel('Y-axis ')

plt.show()

# pandas Series is a fancy list. pandas Dataframe is a dict-like collection of Series, each Series has a column key.

# Access:
# df[*column_name*] for column selection
# df.loc for row selection by label (non-integer)
# df.iloc for row selection by index (integer)

# Adding/removing
# df.drop([*row_label/index*], inplace) removes row (axis = 1 optional)
# df.drop(["columns"], axis = 1, inplace) or df.pop("column") removes column
# .pop returns the removed column, .drop returns the df without the column
# df.dropna() drops NaN rows


# Setting column as index:
# df.set_index("indexname", drop, inplace)
#   drop determines whether to keep the old column, inplace determines whether to change the df (true) /make a new df (false, default)
# pd.read_csv(data, index_col = *col index*)

print("aklhj")
df: pd.DataFrame = 0