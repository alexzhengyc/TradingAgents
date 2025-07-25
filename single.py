from utils.stock_utils import get_stock_stats_metrics, score_stock_from_metrics
from utils.news_utils import score_stock_from_news, sum_recent_news_scores

def main():
    """Main function to demonstrate the functionality"""
    # Example usage of stock metrics
    symbol = "AAPL"
    date = "2025-07-23"
    
    print(f"Analyzing {symbol} for {date}")
    print("=" * 50)
    
    # Get stock statistics and score
    try:
        metrics = get_stock_stats_metrics(symbol, date)
        score = score_stock_from_metrics(metrics)
        print(f"Stock Metrics Score: {score}")
        print()
    except Exception as e:
        print(f"Error getting stock metrics: {e}")
        print()

    # Get news scores
    try:
        result = score_stock_from_news(symbol, date)
        print(f"News Analysis: {result}")
        print()
    except Exception as e:
        print(f"Error getting news scores: {e}")
        print()

    # Get recent news summary
    try:
        recent_result = sum_recent_news_scores(symbol, date)
        print(f"Recent News Summary: {recent_result}")
    except Exception as e:
        print(f"Error getting recent news summary: {e}")


if __name__ == "__main__":
    main() 