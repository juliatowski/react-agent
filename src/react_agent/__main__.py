import argparse
from react_agent.logging_config import set_logging
from react_agent.steps.pipeline import react_pipeline

#takes user promt and logging configuration to run model
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--log", action="store_true", help="Enable normal logging")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose, more detailed logging")

    args = parser.parse_args()

    if args.verbose:
        set_logging(2)
    elif args.log:
        set_logging(1)
    else:
        set_logging(0)

    answer = react_pipeline(args.prompt)
    print(answer)


if __name__ == "__main__":
    main()
