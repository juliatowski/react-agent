import sys
import time
from react_agent.steps.pipeline import react_pipeline  


def main() -> None:
    """Entry point for the react-agent CLI"""
    if len(sys.argv) < 2:
        print('Usage: react-agent "<your question>"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # timer to track excecut
    start = time.time()  
    #Llm model defined in the code for now, can change later
    answer = react_pipeline(query, model="qwen2.5")
    end = time.time()   

    elapsed = end - start

    print(f"\nFinal Answer: {answer}\n")
    print(f"(Promt completed in {elapsed:.2f} seconds)")

if __name__ == "__main__":
    main()