# **Profitability Analysis of Betting Strategies Using OddsPortal Data**

## **Project Overview**
This project focuses on analyzing the profitability of betting strategies for two distinct markets:
- **1-2 market** for tennis, where only two outcomes are possible (Player 1 wins or Player 2 wins).
- **1-X-2 market** for soccer, which includes three possible outcomes (Home win, Draw, Away win).

The analysis pipeline begins with **data cleaning** and progresses through **exploratory data analysis (EDA)**, **visualization**, and ultimately to **profitability evaluation**. The primary goal is to evaluate the potential profitability of different betting strategies based on historical odds data.

All data parsing and collection steps have been completed using the scripts `soccer.py` and `tennis.py`, which are available in the repository. The parsed data is stored in the `data/` folder. This README focuses solely on the analysis process.

## **Repository Structure**
- `soccer.py` and `tennis.py`: Scripts used for data scraping from OddsPortal.
- `data/`: Contains the parsed datasets used in the analysis.
- `analysis.ipynb`: Jupyter Notebooks demonstrating the analysis process.

## **Workflow**

---

Now, let's dive into the **analysis process**, starting with preparing the dataset for exploration and evaluation. 

---

### **1. Data Cleaning and Preprocessing**
The first step in the analysis process is cleaning and preparing the dataset. Ensuring the data is structured and free from errors is crucial for reliable analysis. 

For this project, we start by examining the tennis dataset to gain insights into its structure, detect missing values, and identify potential issues. Below are two screenshots that illustrate the initial exploration of the dataset, including data types and missing values. Based on this examination, we will determine the best approach for handling these issues and preparing the data for further analysis.

#### **1.1 Datatypes Overview**
![Datatypes Overview](images/Picture1.png)

#### **1.2 Missing Values**
![Missing Values](images/Picture2.png)

### **2. Parsing Issues Analysis**
To understand the reasons behind missing and incorrect data during parsing, we analyzed the OddsPortal webpage. Below is a screenshot of the parsed page.

#### **2.1 Parsing Issues Analysis**
![OddsPortal Page Analysis](images/Picture3.png)

From the screenshot, we can immediately observe the following:
1. Tennis matches do not have draw results, so the draw column can be safely removed.
2. The dataset shows incorrect data for the match **Demidova D. – Senic N.**, with two `NaN` values in the `Country` and `League` columns.
3. Upon analyzing the parsed page, it is clear that some tournaments feature two matches starting simultaneously in the same country and tournament. 

**Conclusion:** The parser failed to capture consecutive events occurring at the same time within a single tournament. To address this issue, the missing values can be filled using the last valid values from the dataset.

### **3. Data Cleaning: Handling Missing Values**
After identifying missing and incorrect values in the dataset, the following cleaning steps were performed:
1. Converted the `date` column to a standard datetime format.
2. Forward-filled missing values in the `date`, `country`, and `league` columns.
3. Removed the `draw_odds` column, as draws are not applicable in tennis matches.

Below is a screenshot demonstrating these cleaning steps:

#### **3.1 Data Cleaning Process**
![Data Cleaning Process](images/Picture4.png)

### **4. Feature Engineering: Creating New Columns**
The next step involves feature engineering to prepare the dataset for analysis. This includes:

1. Removing rows with missing values in the `score` column, as these cannot be analyzed.
2. Splitting the `score` column into two new columns: `sets_player1` and `sets_player2`, representing the number of sets won by each player.
3. Creating two additional columns, `winner_player1` and `winner_player2`, to identify the winner of each match based on the set scores.

Below is a screenshot demonstrating these feature engineering steps:

#### **4.1 Feature Engineering: Creating Sets and Winners Columns**
![Feature Engineering: Sets and Winners](images/Picture5.png)

### **5. Profit Analysis and Visualization for Tennis**
After preparing the dataset, we moved on to analyzing the player's profit if they consistently bet on the same outcome across the entire dataset. The tennis dataset consisted of **7,530 matches**, providing a solid basis for analyzing betting strategies.

**Steps involved:**
1. Created a `profit` column to calculate the player's profit for each match.
2. Added a `cumulative_profit` column to track the total profit, used for plotting the graph.
3. Reset the index after removing rows to ensure proper visualization.
4. Defined a custom function to format Y-axis values with a `$` symbol for better readability.

Below is a screenshot of the code used for profit analysis and visualization:

#### **5.1 Columns Creation and Visualization Code**
![Profit Analysis and Visualization](images/Picture6.png)

#### **5.2 Betting on Player 1**
![Cumulative Profit Graph for Player 1 (Tennis)](images/Picture7.png)

This graph represents the cumulative profit for a player consistently placing $1 bets on Player 1 across the dataset. The strategy resulted in a total loss exceeding **$1,000**.

#### **5.3 Betting on Player 2**
![Cumulative Profit Graph for Player 2 (Tennis)](images/Picture8.png)

This graph illustrates the cumulative profit when consistently betting $1 on opponents (Player 2). The results are slightly better than betting on Player 1, but the total loss is still around $1,000

### **6. Profit Analysis and Visualization for Soccer**

Similar to the process for tennis, we applied the same steps for soccer, including data cleaning, feature engineering, and visualization. The soccer dataset consisted of **16,788 matches**, providing a larger sample for analysis. 

Below are the results of these analyses:

#### **6.1 Betting on Home Win (1)**
![Cumulative Profit Graph for Home Win (Soccer)](images/Picture9.png)

The graph below shows the cumulative profit for consistently betting $1 on the home team to win. The results indicate a loss of slightly more than **$1,000** over the dataset.


#### **6.2 Betting on Draw (X)**
![Cumulative Profit Graph for Away (Soccer)](images/Picture10.png)

This graph represents the cumulative profit for consistently placing $1 bets on Player 2 (opponents). While the results are slightly better compared to betting on Player 1, the strategy still resulted in a total loss of approximately **$1,000**.

#### **6.3 Betting on Away Win (2)**
![Cumulative Profit Graph for Away Win (Soccer)](images/Picture11.png)

Finally, this graph demonstrates the cumulative profit when consistently betting $1 on a draw result. The analysis reveals a significant loss exceeding **$2,500**.

## **7. Conclusion**

The analysis clearly demonstrates that betting on outcomes in both tennis and soccer is consistently unprofitable over the long term. Regardless of the chosen strategy—whether betting on Player 1, Player 2, home wins, draws, or away wins — all approaches resulted in significant cumulative losses.











