import pandas as pd
import matplotlib.pyplot as plot

data = {
"Blanks": [43, 43, 43, 43, 43, 45, 45, 49, 51, 51, 51, 51, 53, 53, 53, 53, 56, 56, 56, 58, 58, 58, 59],
"NORMAL edits": [90, 161, 211, 213, 264, 161, 405, 7542, 1053, 1769, 3170, 4174, 4766, 15980, 35953, 66084, 5127, 299318, 1311650, 32461, 864442, 1003800, 120230],
"NORMAL backtracks": [494, 748, 1030, 1121, 1208, 763, 1981, 40447, 5999, 8736, 14749, 21765, 22506, 79478, 174457, 354121, 26240, 1405383, 6218229, 155722, 393026, 4996629, 614523],
"MRV edits": [43, 43, 43, 43, 43, 83, 86, 223, 51, 51, 62, 68, 112, 1057, 101, 1966, 557, 2814, 331, 3117, 2558, 5619, 2039],
"MRV backtracks": [197, 155, 169, 178, 167, 356, 358, 943, 216, 203, 233, 296, 444, 4216, 428, 8306, 2484, 10784, 1426, 12568, 9813, 23536, 9065]
}

print("Number of data items:", len(data["Blanks"]))
df=pd.DataFrame(data)

plot_data=df.groupby("Blanks").mean() # defines plot_data as a grouped graph
 
#[Normal Edits (Light Red), Normal Backtracks (Dark Red), MRV Edits (Light Blue), MRV Backtracks (Dark Blue)]
ax=plot_data.plot(kind="bar", figsize=(12,6), width=0.8, color=["#ff9999", "#cc0000", "#99ccff", "#004c99"])

ax.set_yscale("log") # logarithmic y-axis scale, used to better see all data

plot.title("Sudoku Solver Performance: Normal vs MRV", style="oblique", fontsize="16")
plot.ylabel("Count (Log Scale)\n", color="green", fontsize="12")
plot.xlabel("\nNumber of Empty Cells", color="green", fontsize="12")
plot.xticks(rotation=0) # writes x axis values the right way up
plot.grid(axis="y", alpha=0.25) # horizontal guiding lines to the y axis, used for easier viewing visibility
plot.legend(loc="upper left") # colour key placement

plot.show() # output
