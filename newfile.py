import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. Load CSV file into Python using pandas
# ==========================================
file_path = 'Gene_expression (1).csv'  # Adjust file name if needed
df = pd.read_csv(file_path)

print("--- Step 1: File Loaded Successfully ---")

# ==========================================
# 2. Check the dataset
# ==========================================
print("\n--- Step 2: Dataset Info & First Few Rows ---")
print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset Summary:")
print(df.info())

# ==========================================
# 3. Calculate avg expression for Control & Treated samples
# ==========================================
# Dynamic column selection based on column names
control_cols = [col for col in df.columns if 'Control' in col]
treated_cols = [col for col in df.columns if 'Treated' in col]

df['Control_Avg'] = df[control_cols].mean(axis=1)
df['Treated_Avg'] = df[treated_cols].mean(axis=1)

print("\n--- Step 3: Average Expression Calculated ---")
print(df[['Gene', 'Control_Avg', 'Treated_Avg']])

# ==========================================
# 4. Compare expression between conditions
# ==========================================
# Calculate Difference / Expression Change (Treated - Control)
df['Expression_Change'] = df['Treated_Avg'] - df['Control_Avg']

print("\n--- Step 4: Comparison (Difference = Treated_Avg - Control_Avg) ---")
print(df[['Gene', 'Control_Avg', 'Treated_Avg', 'Expression_Change']])

# ==========================================
# 5. Identify genes with Up-regulated (↑) / Down-regulated (↓) expression
# ==========================================
# Threshold can be set as desired (e.g., > 0.5 up, < -0.5 down)
def classify_gene(change):
    if change > 0.5:
        return 'Upregulated (↑)'
    elif change < -0.5:
        return 'Downregulated (↓)'
    else:
        return 'Unchanged'

df['Status'] = df['Expression_Change'].apply(classify_gene)

print("\n--- Step 5: Gene Expression Classification ---")
print(df[['Gene', 'Expression_Change', 'Status']])

# Summary counts
print("\nSummary Counts:")
print(df['Status'].value_counts())

# ==========================================
# 6. Visualize results using simple plots
# ==========================================
# Plot 1: Bar Chart comparing Control vs Treated Average Expression
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(df))
width = 0.35

ax.bar([i - width/2 for i in x], df['Control_Avg'], width, label='Control Avg', color='skyblue')
ax.bar([i + width/2 for i in x], df['Treated_Avg'], width, label='Treated Avg', color='coral')

ax.set_xlabel('Genes')
ax.set_ylabel('Average Expression Level')
ax.set_title('Gene Expression: Control vs Treated')
ax.set_xticks(x)
ax.set_xticklabels(df['Gene'], rotation=45)
ax.legend()
plt.tight_layout()
plt.show()

# Plot 2: Horizontal Bar Chart of Expression Changes (Up vs Down)
colors = ['green' if status == 'Upregulated (↑)' else ('red' if status == 'Downregulated (↓)' else 'gray') 
          for status in df['Status']]

plt.figure(figsize=(8, 5))
plt.barh(df['Gene'], df['Expression_Change'], color=colors)
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
plt.xlabel('Expression Change (Treated - Control)')
plt.ylabel('Gene')
plt.title('Gene Expression Change (Green: ↑ Upregulated, Red: ↓ Downregulated)')
plt.tight_layout()
plt.show()