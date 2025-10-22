import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from src.logger import log_info, log_error
from src.database import SessionLocal
from src.models import WaterLog

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def generate_water_insight(total_ml: float, user_id: str = "user_1") -> str:
    """
    Generates personalized hydration advice based on user's daily water intake,
    saves the insight to the database, and logs the result.
    """
    db = SessionLocal()

    try:
        # 1️⃣ Build the prompt
        template = PromptTemplate.from_template(
            "The user drank {total_ml} ml of water today. "
            "Provide a short, friendly hydration insight."
        )

        # 2️⃣ Initialize the model
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=groq_api_key
        )

        # 3️⃣ Run the model (modern chain syntax)
        insight = (template | llm).invoke({"total_ml": total_ml})
        ai_text = insight.content if hasattr(insight, "content") else str(insight)

        # 4️⃣ Save to database
        new_entry = WaterLog(
            user_id=user_id,
            amount_ml=total_ml,
            ai_insight=ai_text
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        log_info(f"AI insight generated and stored for {total_ml} ml intake.")
        print(f"✅ Insight saved in database (Record ID: {new_entry.id})")

        return ai_text

    except Exception as e:
        db.rollback()
        log_error(f"Error generating or saving insight: {str(e)}")
        print(f"⚠️ Error: {e}")
        return "⚠️ Could not generate insight at this time. Please try again later."

    finally:
        db.close()


if __name__ == "__main__":
    # Test the agent directly
    print("💧 Running Water Intake AI Agent Test...")
    test_amount = 1800
    result = generate_water_insight(test_amount)
    print(f"\nAI Insight for {test_amount} ml:\n{result}\n")

