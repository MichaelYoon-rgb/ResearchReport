import json
from openai import OpenAI

class DeepSeekAPI:
    def __init__(self, api_key, news_data, profile_data):
        self.api_key = api_key
        self.news_data = news_data
        self.profile_data = profile_data
        self.summary = self.summaries_articles(news_data)
    
    def summaries_articles(self, news_data):
        summary = []
        for news in news_data:
            summary.append(f"Title: {news["title"]}\nContent: {news["text"]}\nPublised Date: {news["publishedDate"]}")
        
        return ("\n\n").join(summary)

    def deepseek(self, messages):
        client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )

        return response.choices[0].message.content
    
    def generate_news(self):
        messages = [
            {"role": "system", "content": "You are a financial analyst summarizing stock-related news."},
            {"role": "user", "content": (
                "Summarize recent news and events for this stock using the articles below:\n\n"
                f"{self.summary}"
                "Output raw text. Only use new lines (\n) for the title."
                "Limit to 2 paragraphs."
            )}
        ]
        return self.deepseek(messages)

    def generate_highlights(self):
        messages = [
            {"role": "system", "content": "You are a financial analyst providing concise, data-driven stock evaluations."},
            {"role": "user", "content": (
                "Evaluate the stock using the format:\n\n"
                "We issue a BUY recommendation on [Company Name] ([Ticker]) with a one-year target price of [Target Price], "
                "offering an estimated upside of [X]% from [Closing Price]. Key factors:\n"
                "Macroeconomic Outlook: [Economic trends]\n"
                "Brand Diversity: [Product portfolio & market strength]\n"
                "Growth Strategy: [Growth initiatives, R&D, acquisitions]\n"
                "Valuation: [Key valuation metrics]\n"
                "Main Risk Factors: [Risks & challenges]\n"
                f"Use the data below to guide your evaluation:\n{self.profile_data}\n"
                f"Use recent news and events of this stock to guid your evaluation:\n{self.summary}\n"
                "Output raw text with no styling. Only use new lines (\n) for the title."
            )}
        ]
        response = self.deepseek(messages)
        return response

