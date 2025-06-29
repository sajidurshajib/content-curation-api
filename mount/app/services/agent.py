import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

os.environ['GROQ_API_KEY']


llm = ChatGroq(
	model_name='llama3-70b-8192',
	temperature=0.3,
)


prompt = ChatPromptTemplate.from_messages(
	[
		(
			'user',
			"""
Given the following content, provide:

1. A concise summary (max 2-3 sentences).
2. Sentiment analysis (Positive / Negative / Neutral) with a brief explanation.
3. A list of 2-4 key topics discussed.

Respond in the following format:

Summary: <Your 2–3 sentence summary here>

Sentiment Analysis: <Positive / Negative / Neutral> — <Brief explanation of the sentiment>

Topics: <Comma-separated list of 2–4 key topics>

Content:
{content}
""",
		)
	]
)


chain = prompt | llm | StrOutputParser()


def summarize_content(content: str) -> str:
	return chain.invoke({'content': content})
