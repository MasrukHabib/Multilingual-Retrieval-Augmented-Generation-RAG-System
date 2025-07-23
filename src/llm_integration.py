import openai
import os
from typing import List
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config


# LLMIntegration class for interacting with OpenAI's chat completion API
class LLMIntegration:
    def __init__(self, api_key: str, model_name: str = config.GENERATION_MODEL):
        """
        Initializes the LLMIntegration with an OpenAI API key and model name.

        Args:
            api_key (str): Your OpenAI API key.
            model_name (str): The name of the OpenAI chat completion model to use.
        """
        openai.api_key = api_key
        self.model_name = model_name

    def generate_answer(self, query: str, context_chunks: List[str]) -> str:
        """
        Generates an answer to the query based on the provided context chunks
        using the OpenAI LLM.

        Args:
            query (str): The user's query.
            context_chunks (List[str]): A list of relevant text chunks retrieved from the knowledge base.

        Returns:
            str: The generated answer from the LLM.
                 Returns an error message if the generation fails.
        """
        # Construct the context string from chunks
        context_str = "\n\n".join(context_chunks) if context_chunks else ""

        # System message: Guides the LLM's behavior and role. Emphasizes strict adherence to context and language matching.
        system_message = (
            "You are an AI assistant designed to answer questions strictly based on the provided text context. "
            "If the answer is explicitly found in the context, provide it directly. "
            "If the answer is NOT found or cannot be directly inferred from the context, "
            "you MUST state 'I don't have enough information from the provided text to answer this question.' "
            "Do NOT use external knowledge. "
            "Ensure your answer is in the same language as the user's query (e.g., if the query is in Bangla, answer in Bangla)."
            "Be concise and to the point."
        )

        # User message: Provides the query and the context to the LLM.
        # Clearly separates context from the question.
        if context_str:
            user_message = (
                f"Here is the relevant information:\n\n"
                f"{context_str}\n\n"
                f"Based ONLY on the information provided above, answer the following question:\n"
                f"{query}"
            )
        else:
            # Fallback for when no relevant chunks are found. The system message already handles this, but we reinforce it.
            user_message = (
                f"No specific context was found for your question. "
                f"Please answer the following question based on general knowledge, or state if you cannot answer:\n"
                f"{query}"
            )

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        try:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.1, # Lower temperature for more deterministic, factual answers
                max_tokens=500,  # Max length of the generated answer
            )
            return response.choices[0].message.content.strip()
        except openai.APIError as e:
            print(f"OpenAI API Error during answer generation: {e}")
            return f"দুঃখিত, উত্তর তৈরি করার সময় একটি ত্রুটি হয়েছে: {e} (Sorry, I encountered an error while trying to generate an answer: {e})"
        except Exception as e:
            print(f"উত্তর তৈরি করার সময় একটি অপ্রত্যাশিত ত্রুটি হয়েছে: {e} (An unexpected error occurred during answer generation: {e})")
            return f"দুঃখিত, একটি অপ্রত্যাশিত ত্রুটি হয়েছে: {e} (Sorry, an unexpected error occurred: {e})"

if __name__ == '__main__':

    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
        print("Please set your OpenAI API key in config.py or as an environment variable to run this example.")
    else:
        llm_integrator = LLMIntegration(api_key=config.OPENAI_API_KEY)

        # Test case 1: With relevant context (Bangla)
        query_bangla = "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"
        context_bangla = [
            "অনুপম তার মামার কাছে শুম্ভুনাথকে সুপুরুষ বলে বর্ণনা করেছে।",
            "শুম্ভুনাথের স্বাস্থ্য ছিল সুঠাম এবং তার মুখশ্রী ছিল শান্ত ও গম্ভীর।",
            "তার চোখ ছিল গভীর ও শান্ত, যা তার ব্যক্তিত্বের গম্ভীরতা প্রকাশ করে।",
            "শুম্ভুনাথের হাসি ছিল মৃদু ও বিনয়ী, যা তার চরিত্রের নম্রতা নির্দেশ করে।",
            "তার কথাবার্তা ছিল সংক্ষিপ্ত ও স্পষ্ট, যা তার আত্মবিশ্বাস ও বুদ্ধিমত্তার পরিচয় দেয়।",
            "অনুপমের ভাষায়, শুম্ভুনাথের এই গুণাবলী তাকে সুপুরুষ হিসেবে চিহ্নিত করে।",
            "সুপুরুষ বলতে বোঝানো হয়েছে একজন ব্যক্তির শারীরিক সৌন্দর্য, ব্যক্তিত্বের গুণাবলী এবং আচরণের নম্রতা।",
        ]
        print(f"\n--- Testing LLM with Bangla Query and Context ---")
        answer_bangla = llm_integrator.generate_answer(query_bangla, context_bangla)
        print(f"Query: {query_bangla}")
        print(f"Answer: {answer_bangla}")

        # Test case 2: With relevant context (English)
        query_english = "When did the modern era of Bengali literature begin?"
        context_english = [
            "Ancient era's example is Charyapad. It was composed between the tenth and twelfth centuries.",
            "The medieval period started from the thirteenth century and ended in the mid-eighteenth century.",
            "The modern era extends from the beginning of the nineteenth century to the present."
        ]
        print(f"\n--- Testing LLM with English Query and Context ---")
        answer_english = llm_integrator.generate_answer(query_english, context_english)
        print(f"Query: {query_english}")
        print(f"Answer: {answer_english}")

        # Test case 3: Without context (should indicate lack of info based on system message)
        query_no_context = "Who invented the telephone?"
        print(f"\n--- Testing LLM with No Context ---")
        answer_no_context = llm_integrator.generate_answer(query_no_context, [])
        print(f"Query: {query_no_context}")
        print(f"Answer: {answer_no_context}")

        # Test case 4: Context provided, but answer not in context
        query_not_in_context = "বাংলাদেশের জাতীয় ফল কি?"
        context_irrelevant = [
            "বাংলাদেশের রাজধানী ঢাকা।",
            "বাংলাদেশের প্রধান নদী পদ্মা।"
        ]
        print(f"\n--- Testing LLM with Irrelevant Context ---")
        answer_not_in_context = llm_integrator.generate_answer(query_not_in_context, context_irrelevant)
        print(f"Query: {query_not_in_context}")
        print(f"Answer: {answer_not_in_context}")
