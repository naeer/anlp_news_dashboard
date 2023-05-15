import pandas as pd
import streamlit as st
import altair as alt


def app():
    st.title('News filtering Tool and Dashboard')
    st.text('These are the latest news collected for the selected topic and applied filters.')
    st.text('Go to the left panel to apply filters to the dataframe and update the visualisations'
            'accordingly.')

    app_df = pd.read_csv('./data_app_st.csv', encoding='utf-8')

    # Extract the month and date from the 'date' column and concatenate them
    app_df['date'] = pd.to_datetime(app_df['date'])
    app_df['month_year'] = app_df['date'].dt.strftime('%b-%Y')

    # Count words and sentences

    def count_words(word_list):
        return len(word_list)

    def count_sentences(sent_list):
        return len(sent_list)

    def calculate_reading_time(num_words):
        return round(num_words * 0.007, 2)

    # Add columns for the number of words and sentences in each article
    app_df['num_words'] = app_df['article_wordtok'].apply(lambda x: count_words(x.split()))
    app_df['num_sentences'] = app_df['article_sentok'].apply(lambda x: count_sentences(x.split()))
    app_df['reading_time_mins'] = app_df['num_words'].apply(lambda x: calculate_reading_time(x))

    # Create a selectbox for the user to filter by keyword
    keywords = app_df['keyword'].unique()
    selected_keyword = st.sidebar.selectbox('Select a keyword', keywords)

    # Create a multiselect for the user to filter by source
    sources = app_df['source'].unique()
    selected_sources = st.sidebar.multiselect('Select sources', sources, default=sources)

    # Create a text input for the user to filter by headline
    headlines = app_df['headline'].unique()
    selected_headline = st.sidebar.text_input('Filter by headline', '')

    # Filter the data based on the selected keyword, sources, and headline
    filtered_df = app_df[(app_df['keyword'] == selected_keyword) &
                         app_df['source'].isin(selected_sources) &
                         app_df['headline'].str.contains(selected_headline, case=False)]

    # Display the filtered data frame
    st.write(filtered_df)

    # Plot sentiment barchart
    st.header('Sentiment Analysis plot')
    st.write('Sentiment scores are calculated per article by providing a score to each sentence'
             'and then obtaning the mean value.')
    st.write('If interested in reading articles with a positive or negative sentiment, go to the'
             'DataFrame and sort by sentiment score or label')
    # Filter the data for sentiment by keyword and sources
    label_counts = filtered_df['article_sentiment_label'].value_counts().reset_index()
    label_counts.columns = ['label', 'count']
    chart = alt.Chart(label_counts).mark_bar().encode(
        x='label',
        y='count',
        color=alt.value('blue')
    ).properties(
        title='Sentiment Label Counts',
        width=alt.Step(40),
        height=alt.Step(100)
    )
    st.altair_chart(chart, use_container_width=True)

    st.header('Articles over time plot')
    st.write('Do you see any trend or relevant increase on the number of articles on a given time'
             'you might want to read articles from those dates to see if any relevant event happened')
    # Plot articles over time
    articles_by_month_year = filtered_df.groupby('month_year')['article'].count().reset_index(name='count')
    chart = alt.Chart(articles_by_month_year).mark_line().encode(
        x='month_year:T',
        y='count',
        tooltip=[alt.Tooltip('month_year:T'), 'count']
    ).properties(
        title='Number of Articles over Time',
        width=alt.Step(40),
        height=alt.Step(100)
    )
    st.altair_chart(chart, use_container_width=True)

    # Named entities barchart
    st.header('Named Entities in Articles plot')
    st.write('Do you spot any person or organisation who appears frequently on the articles?'
             'you might want to explore their connection with the topic.')
    # Preprocess the named_entities column by splitting the strings and creating a new row for each entity
    app_df_exp = filtered_df['named_entities'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
    app_df_exp.name = 'named_entities'
    app_df_exp = filtered_df.drop('named_entities', axis=1).join(app_df_exp)

    # Group the data frame by named_entities and count the frequency of each entity and select the top 10
    top_entities = app_df_exp['named_entities'].value_counts().reset_index()
    top_entities.columns = ['named_entities', 'counts']
    top_entities = top_entities.head(10)
    top_entities = top_entities.sort_values(by='counts', ascending=False)

    # Create bar chart
    chart = alt.Chart(top_entities).mark_bar().encode(
        x=alt.X('counts:Q', axis=alt.Axis(title='Count')),
        y=alt.Y('named_entities:N', axis=alt.Axis(title='Named Entities'),
                sort=alt.EncodingSortField(field="counts", order="descending"))
    )

    chart = chart.properties(title='Top 10 Named Entities')
    st.write(chart)

    # Wordcloud
    st.header('Top Frequent Words plot')
    st.write('Are some of the words surprising or relevant to you? do you see any connection between'
             'the words and topic?')
    # Preprocess the named_entities column by splitting the strings and creating a new row for each entity
    app_df_exp = filtered_df['article_clean_wordtok'].str.split(',', expand=True).stack().reset_index(level=1,
                                                                                                      drop=True)
    app_df_exp.name = 'wordtok'
    app_df_exp = filtered_df.drop('article_wordtok', axis=1).join(app_df_exp)

    # Group the data frame by wordtok and count the frequency of each entity
    top_words = app_df_exp['wordtok'].value_counts().reset_index()
    top_words.columns = ['wordtok', 'counts']

    # Select the top 100 words
    top_words = top_words.head(100)

    # Create a wordcloud using Altair
    chart = alt.Chart(top_words).mark_text().encode(
        x=alt.X('counts:Q', title='Count'),
        y=alt.Y('wordtok:N', title='Word'),
        text='wordtok',
        size=alt.Size('counts:Q', title='Count'),
        color=alt.Color('counts:Q', scale=alt.Scale(scheme='viridis'), title='Count')
    ).properties(
        title='Top 100 Words in Articles',
        width=500,
        height=500
    )

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    app()
