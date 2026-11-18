# Short Video Engagement Dashboard

**Name:** Daniel Y
**Roll No:** 2647215
**Course:** MCA411-2 Python Programming, CHRIST (Deemed to be University)
**Assignment:** Q8 - Design a web application to explore different graphs using layouts

---

## 1. Introduction

This project is an interactive dashboard built with Python and Streamlit. It lets a user explore how short videos perform on a video platform: how often they are played, liked, commented on, shared and followed. Instead of reading through thousands of rows in a spreadsheet, the user can filter the data from a sidebar and see the key numbers, tables and charts update immediately.

The goal was to keep the application easy to read and easy to use, while still covering everything the assignment asks for: KPIs, filters, several chart types, a clean layout, and deployment on Streamlit Community Cloud.

---

## 2. About the Dataset

The dataset is a CSV file named `video_features_statistic_pure.csv`. Each row describes one video, and the columns hold statistics collected about that video.

| Item           | Details                                                              |
| -------------- | -------------------------------------------------------------------- |
| Rows           | 7,583 videos                                                         |
| Columns        | 52                                                                   |
| Type of data   | All numeric (video_id, counts and engagement figures)                |
| Missing values | Rows without play or like counts are dropped when the file is loaded |

The columns fall into a few natural groups:

- **Exposure and plays:** `show_cnt`, `play_cnt`, `play_user_num`, `play_duration`, `complete_play_cnt`, `valid_play_cnt`, `play_progress`
- **Likes:** `like_cnt`, `like_user_num`, `click_like_cnt`, `double_click_cnt`, `cancel_like_cnt`
- **Comments:** `comment_cnt`, `direct_comment_cnt`, `reply_comment_cnt`, `delete_comment_cnt`, `comment_like_cnt`
- **Follows, shares and saves:** `follow_cnt`, `share_cnt`, `download_cnt`, `collect_cnt`
- **Negative feedback:** `report_cnt`, `reduce_similar_cnt`

Most of these columns come in pairs, one counting total actions (`_cnt`) and one counting the number of distinct users (`_user_num`).

### Columns created for the analysis

The original file contains only numbers, with no ready-made categories and no date column. Since the assignment asks for category-wise counts, group-by operations and a trend line, I created a few extra columns in the code:

1. **Popularity Tier** - videos are ranked by `play_cnt` and split into four equal groups: Low, Medium, High and Very High.
2. **Like Rate** - `like_cnt` divided by `play_cnt`. This tells us how likely a viewer is to like a video, regardless of how many views it has.
3. **Engagement Level** - videos are ranked by like rate and split into three equal groups: Low, Medium and High.
4. **Video ID Group** - videos are sorted by `video_id` and divided into 20 equal groups. Because the dataset has no time column, this is what the line chart uses along its x-axis.

---

## 3. Application Layout and Components

The application follows the layout requirements of the assignment. Each component below is used for a specific purpose.

### Header and footer

A title banner and short description appear at the top of the page, and a footer with the course details appears at the bottom.

### Sidebar

All the controls live in the sidebar so that the main page stays clean:

- **File uploader** - optional, lets the user load a different CSV.
- **Multiselect** - choose which Popularity Tiers and Engagement Levels to include.
- **Select box and slider** - pick any numeric column and narrow it to a chosen range.
- **Analysis settings** - choose the main metric to analyse and the category used for grouping.

### KPI row (columns and metrics)

Four KPI cards sit side by side using Streamlit columns:

- Total number of videos
- Sum of the selected metric
- Average of the selected metric
- Average like rate

Below this, group-by operations produce the video count and the average metric for each category.

### Tabs

The main content is split into four tabs:

1. **Dataset Overview** - row and column counts, a preview of the first 100 filtered rows, plus expanders for data types and missing values.
2. **Data Analysis** - category-wise video counts, average of the selected metric by category, and an expander with descriptive statistics for key metrics.
3. **Visualizations** - all five charts, described in the next section.
4. **Insights** - short, automatically generated findings, such as the largest group, the group with the highest average, and the numeric column most strongly correlated with the selected metric.

### Containers and expanders

Containers group related items together, for example the overview figures and the data table. Expanders hide extra detail, such as data types, missing values, descriptive statistics and the guide on how to read the charts, so the page does not feel crowded.

### Other implementation details

- `st.cache_data` is used when loading the file, so the data is read and prepared only once.
- If the filters remove every row, the app shows a clear warning instead of an error.

---

## 4. Charts Used

All charts are built with Plotly Express, so they are interactive: users can hover for values, zoom, and click legend entries to hide or show a series. Every chart has a title, axis labels and a legend where relevant.

### Bar chart

- **What it shows:** the average of the selected metric for each category (for example, average likes per Popularity Tier).
- **Why it was chosen:** bar charts are the clearest way to compare values across a small number of categories.

### Line chart

- **What it shows:** the average of the selected metric across the 20 Video ID Groups.
- **Why it was chosen:** it reveals whether the metric rises, falls or stays steady as the video IDs increase. Since there is no date column, the Video ID Group serves as the ordered axis.

### Scatter plot

- **What it shows:** the relationship between two numeric variables, with each dot representing one video and the colour showing its Popularity Tier. By default it compares `play_cnt` and `like_cnt`.
- **Why it was chosen:** it helps spot patterns, clusters and outliers, such as videos with unusually high likes for their number of plays. A log-scale option is included because the values are heavily skewed.

### Histogram

- **What it shows:** how the selected metric is distributed across all filtered videos. The user can change the number of bins and switch the count axis to a log scale.
- **Why it was chosen:** it shows the overall shape of the data at a glance. In this dataset most videos have low values while a small number have very high ones, which is a typical pattern for online content.

### Pie chart

- **What it shows:** each category's share of the filtered videos, for example the proportion of videos in each Engagement Level.
- **Why it was chosen:** it gives a quick picture of how the data is split between groups. It works well here because the number of categories is small.

---

## 5. How Filters Affect the Dashboard

Every filter in the sidebar is applied to one shared, filtered copy of the data. Because the KPIs, tables, charts and insights are all built from that copy, they always stay consistent with each other. When a user changes a tier, a range or the main metric, the whole page refreshes automatically.

---

## 6. Technologies Used

| Tool           | Purpose                                              |
| -------------- | ---------------------------------------------------- |
| Python         | Programming language                                 |
| Streamlit      | Web application framework and layout components      |
| Pandas         | Loading, cleaning, grouping and summarising the data |
| Plotly Express | Interactive charts                                   |

---

## 7. Project Files

| File                                  | Description                                                |
| ------------------------------------- | ---------------------------------------------------------- |
| `app.py`                            | The complete Streamlit application                         |
| `requirements.txt`                  | List of Python packages needed (streamlit, pandas, plotly) |
| `video_features_statistic_pure.csv` | The dataset                                                |
| `README.md`                         | This document                                              |

---

## 8. How to Run the Application Locally

1. Place `app.py`, `requirements.txt` and the CSV file in the same folder.
2. Open a terminal in that folder and install the packages:

   ```
   pip install -r requirements.txt
   ```
3. Start the application:

   ```
   streamlit run app.py
   ```
4. The dashboard opens in the browser at `http://localhost:8501`.

---

## 9. Deployment on Streamlit Community Cloud

1. Create a public GitHub repository and upload `app.py`, `requirements.txt` and the CSV file.
2. Sign in at share.streamlit.io with the same GitHub account.
3. Choose "Create app", select the repository and branch, and set `app.py` as the main file.
4. Click Deploy. After a short installation step, the application receives a public link.
5. Open the link and confirm that the filters, charts and tabs work as expected.

---

## 10. Conclusion

The dashboard turns a large table of video statistics into something a person can explore in a few clicks. It meets the assignment requirements through KPIs that respond to filters, five different chart types, a layout built from the sidebar, columns, containers, expanders and tabs, and a deployment on Streamlit Community Cloud. Since the code is divided into clearly labelled sections, it is also straightforward to extend with new filters or charts in the future.
