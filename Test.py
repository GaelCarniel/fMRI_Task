import pandas as pd

# Create an empty list
data = []

# Add rows to the list
data.append(["John", 25, "New York"])
data.append(["Anna", 28, "Los Angeles"])

# Create the DataFrame with column names
df = pd.DataFrame(data, columns=["Name", "Age", "City"])

print(df)
