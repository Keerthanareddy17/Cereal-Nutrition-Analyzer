from preswald import text, plotly, connect, get_df, table, slider
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from preswald import text_input, table, text

# Welcome message
text("""
# 🥣 Cereal Nutrition Analyzer
Explore your favorite breakfast cereals with delicious data insights!  
We crunch the numbers so you can crunch the flakes. 😋✨  
""")

# Load the CSV
connect()
df = get_df('cereal')

# Data Cleaning 
# 1. Drop rows with missing values
df = df.dropna()  

# 2. Remove duplicates
df = df.drop_duplicates()

# 3. Data Type Conversion 
# Ensure 'calories' and 'rating' are numeric as they are the crucial cols
df['calories'] = pd.to_numeric(df['calories'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Create a slider for user input to filter cereals by rating
threshold = slider("Rating Threshold", min_val=0, max_val=100, default=50)

# Filter the DataFrame based on the slider value
filtered_df = df[df["rating"] > threshold]

# Display the filtered data in a table
table(filtered_df, title="Cereals with Rating Greater than {}".format(threshold))


# 1. Rating vs Sugar
text("### 🍬 Sugar vs. ⭐ Rating\nSee how sugary cereals fare when it comes to consumer ratings. Do healthier options really get more love?")
fig1 = px.scatter(df, x='sugars', y='rating', color='mfr', hover_name='name',
                  title="🍬 Sugar vs. ⭐ Rating",
                  labels={"sugars": "Sugar (g)", "rating": "Rating"})
plotly(fig1)

# 2. Fiber Champions: Top 10 cereals with highest fiber
text("### 🌾 Top 10 High-Fiber Cereals\nFiber is your gut's best friend. Here are the top cereals packed with fiber!")
top_fiber = df.sort_values(by='fiber', ascending=False).head(10)
fig2 = px.bar(top_fiber, x='name', y='fiber', color='fiber',
              title="🌾 Top 10 High-Fiber Cereals", labels={"fiber": "Fiber (g)"})
plotly(fig2)

# 3. Nutrient Trends: Line Plot by Manufacturer
text("### 📈 Average Calories, Protein & Sugar by Manufacturer\nWho keeps it healthy? Compare the average nutrient profile across cereal brands.")
nutrient_cols = ['calories', 'protein', 'sugars']
avg_nutrients = df.groupby('mfr')[nutrient_cols].mean().reset_index().melt(id_vars='mfr')

fig3 = px.line(avg_nutrients, x='mfr', y='value', color='variable',
               markers=True,
               title="📈 Average Calories, Protein & Sugars by Manufacturer",
               labels={"value": "Amount", "mfr": "Manufacturer", "variable": "Nutrient"})
plotly(fig3)

# 4. Manufacturer Showdown: Avg Ratings by Brand
text("### 🏢 Average Cereal Ratings by Manufacturer\nWhich cereal brand rules the breakfast table? Find out by average ratings.")
avg_rating_by_mfr = df.groupby("mfr")["rating"].mean().reset_index()
fig4 = px.bar(avg_rating_by_mfr, x="mfr", y="rating", color="rating",
              title="🏢 Average Cereal Ratings by Manufacturer",
              labels={"rating": "Avg Rating", "mfr": "Manufacturer"})
plotly(fig4)
    
# 5. Fiber vs Protein Correlation
text("### 🥦 Fiber vs Protein (Bubble Size = Rating)\nAre high-fiber cereals also protein-rich? Hover to explore individual cereals.")
fig5 = px.scatter(df, x='fiber', y='protein', size='rating', color='calories',
                  hover_name='name', title="🥦 Fiber vs Protein (Size = Rating)")
plotly(fig5)

#6. 3D - Fiber, Sugar, Rating
text("### 🔬 3D Nutrition Landscape\nFiber, Sugar, and Rating all in one plot! Use this to explore the balance between health and taste.")
fig6 = px.scatter_3d(df, x='fiber', y='sugars', z='rating',
                     color='calories', size='protein',
                     hover_name='name',
                     title="🔬 3D Nutrition Landscape: Fiber, Sugar & Rating")
plotly(fig6)


# 7. Shelf Placement vs Rating (Line Plot by Average Rating)
text("### 📚 Shelf Placement vs Average Rating\nThis line plot shows the trend of average ratings for cereals placed at different shelf levels. Does the top shelf really deliver the best ratings?")
avg_shelf_rating = df.groupby('shelf')['rating'].mean().reset_index()
fig7 = px.line(avg_shelf_rating, x='shelf', y='rating', markers=True,
               title="Average Rating by Shelf Placement",
               labels={"shelf": "Shelf Level (1 = Bottom, 3 = Top)", "rating": "Average Rating"})
plotly(fig7)


# 📊 8. Carb-to-Fiber Ratio
text("### ⚖️ Carb-to-Fiber Ratio Distribution\nA low carb-to-fiber ratio can indicate a healthier cereal. Let's explore the distribution.")
df['carb_fiber_ratio'] = df['carbo'] / df['fiber'].replace(0, 0.1)  # avoid divide-by-zero
fig8 = px.histogram(df, x='carb_fiber_ratio', nbins=20, color='type',
                    title="Carbohydrate-to-Fiber Ratio",
                    labels={'carb_fiber_ratio': 'Carb/Fiber Ratio'})
plotly(fig8)

text("### 🔍 Search Your Cereal!\nLooking for something specific? Type in the name of your favorite cereal to see its nutrition breakdown. Whether it's 'Corn Flakes' or 'Wheat Crunch', we've got the scoop! 🥄")
# Get user input
cereal_name = text_input("Enter a cereal name to look up")

# Check that the input is not empty
if cereal_name.strip():
    matched_cereal = df[df["name"].str.contains(cereal_name, case=False)]
    
    if not matched_cereal.empty:
        table(matched_cereal, title=f"Nutrition Info for '{cereal_name}'")
    else:
        text(f"😕 No cereal found with name containing '{cereal_name}'. Try something like 'Corn' or 'Wheat'.")
else:
    text("👆 Please enter a cereal name above to see its details.")

    
# Closing message
text("""
# 🎉 Thanks for Exploring Cereal Nutrition! 

You've just uncovered the hidden nutritional gems of your favorite breakfast cereals.  
Stay healthy, stay curious, and keep crunching those flakes! 🥣✨  
""")

