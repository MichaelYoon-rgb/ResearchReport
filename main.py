import zipfile, json, re
from docx import Document
from docx_helper import DocxHelper
from fmp_helper import FMPAPI
from graph_helper import GraphHelper
from deepseek_helper import DeepSeekAPI
regex = re.compile("foo")


def main():

    # Example usage
    api_key_fmp = "fE3LyQCTT2Y8oiCEhF4dZ57ootdPvCEh"
    api_key_deepseek = "sk-05f74d53dcad4da58bc57ebcb0929c65"
    print()
    print("Welcome to this demo.\n"
          "The purpose of this is to provide an overview the software's ability as a prototype, all features are still under development and will be improved.\n"
          "Currently on the development roadmap, I have plans that this software will be hosted on a web server online under a public domain.\n"
          "Due to restrictions on resources, the demo is just an executable file which shows off the software.\n"
          "You can type out the symbol of any international company, such as AAPL, and it will generate a report saved as Result2.docx.\n")
    print("Please Enter A Symbol: ", end="")

    symbol = input()

    print("\n")

    print("Generating pdf...")
    print("Scraping live data from API...")
    fetcher = FMPAPI(api_key_fmp)
    yearly_data, profile_data, news_data = fetcher.fetch_data(symbol, save=True)
    print("Processing data...")
    
    graph = GraphHelper("Revenue Change Over Years", "Year", "Revenue")
    graph.parse_data(yearly_data, "revenue")
    revenue_graph_bytes = graph.generate_graph("revenue.png")
    print("AI weights generating report...")
    
    deepseek = DeepSeekAPI(api_key_deepseek, news_data, profile_data)
    profile_data["News"] = deepseek.generate_news()
    profile_data["Highlights"] = deepseek.generate_highlights()
    print(profile_data["Highlights"])
    print(profile_data["News"])

    profile_data["Images"] = {
        "Revenue": revenue_graph_bytes
    }
    
    input_file = 'Template.docx'
    output_file = 'Report.docx'
    print("Reconstructing input template file...")
    
    replacer = DocxHelper(input_file, output_file, yearly_data, profile_data)
    absolute_path = replacer.generate_docx()
    print(f"Report has been successfully generated at {absolute_path}")

if __name__ == "__main__":
    main()
