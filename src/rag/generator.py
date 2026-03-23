import os
from dotenv import load_dotenv
from openai import OpenAI
from src.config import LLM_MODEL


# Cargar variables del .env
load_dotenv()


class Generator:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
    
# -------------------------
# Test rápido en consola    
# -------------------------

if __name__ == "__main__":
    from src.rag.retriever import Retriever
    from src.rag.prompt_builder import PromptBuilder

    retriever = Retriever()
    builder = PromptBuilder()
    generator = Generator()

    query = "What is inflation?"

    docs = retriever.retrieve(query, k=3)
    prompt = builder.build_prompt(query, docs)

    answer = generator.generate(prompt)

    print("\n--- ANSWER ---\n")
    print(answer)