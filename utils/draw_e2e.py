# Splitting data for human-generated questions (q_id 1-15) and GPT-generated questions (q_id 16-30)
# scores_human = scores[:15]
# scores_gpt = scores[15:]
# rag_status_human = rag_status[:15]
# rag_status_gpt = rag_status[15:]
# locations_human = locations[:15]
# locations_gpt = locations[15:]
# comments_human = comments[:15]
# comments_gpt = comments[15:]

# Function to create score distribution histograms
def plot_histogram(data, title, ax):
    ax.hist(data, bins=[0, 1, 2, 3, 4, 5, 6], edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel('Scores')
    ax.set_ylabel('Frequency')
    ax.grid(True)

# Function to create RAG status pie charts
def plot_pie_chart(data, title, ax):
    rag_counts = {status: data.count(status) for status in set(data)}
    labels = ['Correct', 'Incorrect']
    sizes = [rag_counts.get('Y', 0), rag_counts.get('N', 0)]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['green', 'red'])
    ax.set_title(title)

# Function to plot average scores by location
def plot_location_scores(data, scores, title, ax):
    location_scores = {loc: [] for loc in set(data) if loc}
    for loc, score in zip(data, scores):
        if loc:
            location_scores[loc].append(score)
    location_avg_scores = {loc: np.mean(scores) for loc, scores in location_scores.items()}
    locations_sorted = sorted(location_avg_scores, key=location_avg_scores.get, reverse=True)
    scores_sorted = [location_avg_scores[loc] for loc in locations_sorted]
    ax.bar(locations_sorted, scores_sorted, color='skyblue')
    ax.set_title(title)
    ax.set_xlabel('Location')
    ax.set_ylabel('Average Score')
    ax.set_xticklabels(locations_sorted, rotation=45)
    ax.grid(True, axis='y')

# Function to create word clouds
def plot_word_cloud(data, title, ax):
    comment_text = " ".join(data)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comment_text)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title)

# Creating figures with subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Analysis of Human vs. GPT-Generated Questions')

# Plotting histograms
plot_histogram(scores_human, 'Score Distribution (Human-Generated)', axs[0, 0])
plot_histogram(scores_gpt, 'Score Distribution (GPT-Generated)', axs[0, 1])

# Plotting pie charts
plot_pie_chart(rag_status_human, 'RAG Correctness (Human-Generated)', axs[1, 0])
plot_pie_chart(rag_status_gpt, 'RAG Correctness (GPT-Generated)', axs[1, 1])

# Showing histograms and pie charts
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Creating figures for location scores and word clouds separately due to layout constraints
fig, axs = plt.subplots(1, 2, figsize=(15, 5))
fig.suptitle('Average Scores by Location')

# Plotting location scores
plot_location_scores(locations_human, scores_human, 'Human-Generated', axs[0])
plot_location_scores(locations_gpt, scores_gpt, 'GPT-Generated', axs[1])
plt.tight_layout()
plt.show()

fig, axs = plt.subplots(1, 2, figsize=(15, 7))
fig.suptitle('Comments Word Cloud')

# Plotting word clouds
plot_word_cloud(comments_human, 'Comments (Human-Generated)', axs[0])
plot_word_cloud(comments_gpt, 'Comments (GPT-Generated)', axs[1])
plt.tight_layout()
plt.show()
