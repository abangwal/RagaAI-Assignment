## Market Brief Agent

### Workflow Diagram
---
![](diagram.jpeg)

[**Checkout detailed Documentation**](docs/ai_tool_usage.md)

#### Overview
* An acyclic workflow where the user interacts through a Streamlit App.
* User's query is first parsed by the Orchestrator API endpoint that returns the result for what tools to use along with the result of those tools' execution.
* The original user query and the generated supporting context are then passed to the final response synthesizer.
* Final response is streamed back to the Streamlit app again via API communication.
* User can further instruct to listen to the generated response using Deepgram's voice models.

### Tools 

**All tools are accessible through an API interface**
* `/data/get_historical_data` : This tool brings historical changes in a particular given stock. Must provide a YFinance ticker as a parameter.
* `/data/get_earning_metrics` : This tool generates the stock earnings summary over the past 3–4 years using YFinance earning metrics.
* `/data/get_portfolio_data` : This tool brings a current portfolio snapshot/updates. *Currently only supports IND portfolio*.
* `/data/get_knowledge` : This is a ***RAG*** based tool. It uses a company's prior documents as a knowledge base and uses semantic similarity to provide context on company-related user queries.
* `/data/get_update` : This tool is used to get latest updates on stock by scraping NEWS from variety of publications. This ensures diverse unbiased NEWS as context for agile responses.
* `/orchestrator/orchestrator_decision` : Tool to make orchestration decisions—i.e., which tool to call with what parameters.
* `/orchestrator/final_response` : Tool to generate the final user-friendly response with **guardrails** to avoid giving aggressive financial advice.

### Deployment

Fully functional **Docker**-based deployment for maintainability and scalability.

```
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirement.txt

# Create a non-root user
RUN useradd -m appuser

# Create necessary directories and set permissions
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    mkdir -p /app/chroma_storage
    
USER appuser
# Start the FastAPI app on port 7860, the default port expected by Spaces
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "7860"]
```

#### FYIs
* Voice I/O is slow because of Streamlit voice processing and Deepgram API latency.
