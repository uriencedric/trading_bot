

import argparse

from misc.constants import FUNCTIONS
from tools.run import get_function

def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Cryptocurrency Trading Bot with AI and Volume-Based Refinements"
    )

    # Add arguments
    parser.add_argument(
        "--funcname",
        type=str,
        help=""" Supported :
            "_back_test"
            "_back_test_optimized"
            "_adaptive_training_with_risk_controls"
            "_hybrid_trend_aware_strategy"
            "_run_strategy_parallel_grid_search"
            "_simulation_historical_data"
            "_trend_aware_strategy_on_symbols"
            "_volume_enhanced_strategy_on_symbol"
            "_volume_enhanced_historical_strategy_on_symbols"
            "_walk_forward_live_trading"
            "_walk_forward_adaptative_training"
    }""",
        required=True,
    )

    # Parse the arguments
    args = parser.parse_args()

    # Validate the arguments
    if args.funcname not in FUNCTIONS:
        print(f"Error: function {args.funcname} provided is not supported.")
        return

    get_function(args.funcname)()

if __name__ == "__main__":
    main()
