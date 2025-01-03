import pandas as pd
import streamlit as st
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(
    page_title="Data Analysis Portal",
    page_icon="📊",
    layout="wide"
)

# Page Title and Subheader
st.title(':rainbow[Data Analytics Portal]')
st.subheader(':gray[Explore Data with Ease.]', divider='rainbow')

# File Upload Section
file = st.file_uploader('Drop CSV or Excel', type=['csv', 'xlsx'])

if file:
    # Load file based on type
    if file.name.endswith('.csv'):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    # Display the dataset
    st.dataframe(data)
    st.info('File uploaded successfully', icon='🚨')

    # Data Cleaning Options
    st.subheader(':rainbow[Data Cleaning Options]', divider='rainbow')

    # Remove duplicates
    remove_duplicates = st.checkbox('Remove Duplicate Rows')
    if remove_duplicates:
        original_shape = data.shape
        data = data.drop_duplicates()
        removed_rows = original_shape[0] - data.shape[0]
        st.success(f'Removed {removed_rows} duplicate rows. New shape: {data.shape}', icon='✅')

    # Handle missing values
    st.subheader('Missing Value Handling')
    missing_value_option = st.radio(
        "How would you like to handle missing values?",
        options=["Keep as is", "Remove rows with missing values", "Fill missing values with a specific value"]
    )

    if missing_value_option == "Remove rows with missing values":
        original_shape = data.shape
        data = data.dropna()
        removed_rows = original_shape[0] - data.shape[0]
        st.success(f'Removed {removed_rows} rows with missing values. New shape: {data.shape}', icon='✅')

    elif missing_value_option == "Fill missing values with a specific value":
        fill_value = st.text_input("Enter the value to fill missing values:")
        if fill_value:
            data = data.fillna(fill_value)
            st.success("Filled all missing values with the specified value.", icon='✅')

    # Tabs for data insights
    st.subheader(':rainbow[Basic Information Of Dataset]', divider='rainbow')
    tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Tops and Bottom Rows', 'Data Types', 'Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.')
        st.subheader(':gray[Statistical Summary Of Dataset]')
        st.dataframe(data.describe())

        st.subheader(':gray[Missing Values per Column]')
        st.dataframe(data.isnull().sum())

        total_missing = data.isnull().sum().sum()
        st.subheader(f':gray[Total Missing Values: {total_missing}]')

    with tab2:
        st.subheader(':grey[Top Rows]')
        top_rows = st.number_input(
            "Enter the number of top rows to display", 
            min_value=1, 
            max_value=len(data), 
            step=1, 
            value=5
        )
        st.dataframe(data.head(top_rows))

        st.subheader(':grey[Bottom Rows]')
        bottom_rows = st.number_input(
            "Enter the number of bottom rows to display", 
            min_value=1, 
            max_value=len(data), 
            step=1, 
            value=5,
            key="bottom_rows"
        )
        st.dataframe(data.tail(bottom_rows))

    with tab3:
        st.subheader(':grey[Data Types of Columns]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(':grey[Column Names in the Dataset]')
        st.write(list(data.columns))

    # Value Counts
    st.subheader(':rainbow[Column Values Count]', divider='rainbow')
    with st.expander('Value Count'):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose Column Name', options=list(data.columns))
        with col2:
            top_rows = st.number_input('Top rows', min_value=1, step=1, value=5)

        count = st.button('Count')
        if count:
            result = data[column].value_counts().reset_index().head(top_rows)
            result.columns = [column, 'count']
            st.dataframe(result)

            # Visualization
            st.subheader('Visualization', divider='grey')
            fig_bar = px.bar(data_frame=result, x=column, y='count')
            st.plotly_chart(fig_bar)

            fig_line = px.line(data_frame=result, x=column, y='count', text='count', template='plotly_white')
            st.plotly_chart(fig_line)

            fig_pie = px.pie(data_frame=result, names=column, values='count')
            st.plotly_chart(fig_pie)

    # Groupby Section
    st.subheader(':rainbow[Groupby: Simplify Your Data Analysis]', divider='rainbow')
    st.write('The groupby lets you summarize data by specific categories and groups.')
    with st.expander('Group By your columns'):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose columns to group by', options=list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation', options=list(data.columns))
        with col3:
            operation = st.selectbox('Choose operation', options=['sum', 'max', 'min', 'mean', 'median', 'count'])

        if groupby_cols:
            result = data.groupby(groupby_cols).agg(
                newcol=(operation_col, operation)
            ).reset_index()
            st.dataframe(result)

            # Visualization
            st.subheader(':gray[Data Visualization]', divider='gray')
            graphs = st.selectbox('Choose your graphs', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])
            if graphs == 'line':
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))
                fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers='o')
                st.plotly_chart(fig)
            elif graphs == 'bar':
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))
                facet_col = st.selectbox('Column Information', options=[None] + list(result.columns))
                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                st.plotly_chart(fig)
            elif graphs == 'scatter':
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))
                size = st.selectbox('Size Column', options=[None] + list(result.columns))
                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
                st.plotly_chart(fig)
            elif graphs == 'pie':
                values = st.selectbox('Choose Numerical Values', options=list(result.columns))
                names = st.selectbox('Choose labels', options=list(result.columns))
                fig = px.pie(data_frame=result, values=values, names=names)
                st.plotly_chart(fig)
            elif graphs == 'sunburst':
                path = st.multiselect('Choose your Path', options=list(result.columns))
                fig = px.sunburst(data_frame=result, path=path, values='newcol')
                st.plotly_chart(fig)
