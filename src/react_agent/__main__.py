import argparse
from react_agent.logging_config import set_logging
from react_agent.steps.pipeline import react_pipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--log", action="store_true", help="Enable normal logging")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        set_logging(2)
    elif args.log:
        set_logging(1)
    else:
        set_logging(0)

    answer = react_pipeline(args.prompt, model="qwen2.5")
    print(answer)


if __name__ == "__main__":
    main()
