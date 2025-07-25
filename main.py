import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from utils.stock_utils import get_stock_stats_metrics, score_stock_from_metrics
from utils.news_utils import score_stock_from_news, sum_recent_news_scores


def ensure_ticker_directory(ticker):
    """Ensure the ticker-specific data directory exists"""
    ticker_dir = f"data/{ticker}"
    if not os.path.exists(ticker_dir):
        os.makedirs(ticker_dir)
    return ticker_dir


def check_metrics_exists(ticker, date):
    """Check if metrics data already exists for the given ticker and date"""
    metrics_file = f"data/{ticker}/metrics.csv"
    if not os.path.exists(metrics_file):
        return False
    
    try:
        df = pd.read_csv(metrics_file)
        return date in df['as_of'].values if 'as_of' in df.columns else False
    except:
        return False


def check_news_exists(ticker, date):
    """Check if news data already exists for the given ticker and date"""
    news_file = f"data/{ticker}/news_{date}.csv"
    return os.path.exists(news_file)


def save_metrics_data(ticker, metrics_data):
    """Save metrics data to data/{ticker}/metrics.csv"""
    ensure_ticker_directory(ticker)
    metrics_file = f"data/{ticker}/metrics.csv"
    
    # Convert dict to DataFrame row
    df_new = pd.DataFrame([metrics_data])
    
    if os.path.exists(metrics_file):
        # Load existing data and append
        try:
            df_existing = pd.read_csv(metrics_file)
            # Remove any existing data for the same date
            if 'as_of' in df_existing.columns:
                df_existing = df_existing[df_existing['as_of'] != metrics_data['as_of']]
            # Append new data
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(metrics_file, index=False)
        except:
            # If there's an issue reading the existing file, overwrite it
            df_new.to_csv(metrics_file, index=False)
    else:
        # Create new file
        df_new.to_csv(metrics_file, index=False)
    
    print(f"    ✓ Metrics saved to {metrics_file}")


def save_news_data(ticker, date):
    """Copy scored news from global news directory to ticker-specific directory"""
    ensure_ticker_directory(ticker)
    
    # Source file (existing format)
    source_file = f"data/news/{ticker}_news_scored_{date.replace('-', '_')}.csv"
    # Destination file (new format)
    dest_file = f"data/{ticker}/news_{date}.csv"
    
    if os.path.exists(source_file):
        try:
            # Copy the file to the new location
            df = pd.read_csv(source_file)
            df.to_csv(dest_file, index=False)
            print(f"    ✓ News saved to {dest_file}")
            return True
        except Exception as e:
            print(f"    ✗ Error copying news data: {e}")
            return False
    else:
        print(f"    ⚠ No scored news file found at {source_file}")
        return False


def get_trading_days_range(start_date=None, end_date=None, num_days=7):
    """
    Get trading days within a specified date range or the most recent trading days.
    
    Args:
        start_date (str or datetime): Start date in 'YYYY-MM-DD' format or datetime object
        end_date (str or datetime): End date in 'YYYY-MM-DD' format or datetime object  
        num_days (int): Number of recent days to get if start_date/end_date not provided
    
    Returns:
        list: List of trading day strings in 'YYYY-MM-DD' format
    """
    if start_date is None and end_date is None:
        # Default behavior: get recent trading days
        end_date = datetime.now()
        # Go back extra days to ensure we get enough trading days
        start_date = end_date - timedelta(days=num_days * 2)
        trading_days = pd.bdate_range(start=start_date, end=end_date)
        # Return the last num_days trading days
        return [d.strftime('%Y-%m-%d') for d in trading_days[-num_days:]]
    
    # Convert string dates to datetime if needed
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Generate business days (excludes weekends automatically)
    trading_days = pd.bdate_range(start=start_date, end=end_date)
    return [d.strftime('%Y-%m-%d') for d in trading_days]


def get_recent_trading_days(num_days=7):
    """Get the most recent trading days (business days) - kept for backward compatibility"""
    return get_trading_days_range(num_days=num_days)


def run_pipeline(symbol="AAPL", start_date=None, end_date=None, num_days=30, save_to_score_dir=True):
    """
    Run backtesting pipeline for a symbol over specified date range or recent trading days.
    
    Args:
        symbol (str): Stock symbol to analyze (default: AAPL)
        start_date (str): Start date in 'YYYY-MM-DD' format (optional)
        end_date (str): End date in 'YYYY-MM-DD' format (optional)
        num_days (int): Number of recent days if start_date/end_date not provided (default: 7)
        save_to_score_dir (bool): Whether to save results to data/score directory
    
    Returns:
        pd.DataFrame: DataFrame with all the collected scores
    """
    print(f"Starting backtesting pipeline for {symbol}")
    print("=" * 60)
    
    # Get trading days based on parameters
    if start_date is not None or end_date is not None:
        trading_days = get_trading_days_range(start_date, end_date)
        print(f"Analyzing trading days from {start_date or 'earliest'} to {end_date or 'latest'}:")
    else:
        trading_days = get_trading_days_range(num_days=num_days)
        print(f"Analyzing {len(trading_days)} recent trading days:")
    
    for day in trading_days:
        print(f"  - {day}")
    print()
    
    # Validate we have trading days
    if not trading_days:
        print("No trading days found in the specified range!")
        return pd.DataFrame()
    
    results = []
    
    for i, trade_date in enumerate(trading_days):
        print(f"Processing day {i+1}/{len(trading_days)}: {trade_date}")
        print("-" * 40)
        
        row_data = {
            'symbol': symbol,
            'trade_date': trade_date,
            'day_number': i + 1
        }
        
        # 1. Get and score stock metrics
        if check_metrics_exists(symbol, trade_date):
            print("  ✓ Metrics data already exists, loading from cache...")
            try:
                metrics_file = f"data/{symbol}/metrics.csv"
                df_metrics = pd.read_csv(metrics_file)
                metrics_row = df_metrics[df_metrics['as_of'] == trade_date].iloc[0]
                
                # Create metrics dict from cached data
                metrics = metrics_row.to_dict()
                
                # Check if scores are already saved in CSV, otherwise calculate them
                score_fields = ['metrics_trend_score', 'metrics_momentum_score', 
                               'metrics_volume_flow_score', 'metrics_volatility_penalty']
                
                if all(field in metrics and pd.notna(metrics[field]) for field in score_fields):
                    # Use cached scores directly from CSV
                    print("    ✓ Using cached scores from CSV")
                    row_data.update({
                        'metrics_trend_score': metrics['metrics_trend_score'],
                        'metrics_momentum_score': metrics['metrics_momentum_score'],
                        'metrics_volume_flow_score': metrics['metrics_volume_flow_score'],
                        'metrics_volatility_penalty': metrics['metrics_volatility_penalty']
                    })
                    print(f"    ✓ Cached scores: Trend={metrics['metrics_trend_score']}, "
                          f"Momentum={metrics['metrics_momentum_score']}, "
                          f"VolumeFlow={metrics['metrics_volume_flow_score']}, "
                          f"VolPenalty={metrics['metrics_volatility_penalty']}")
                else:
                    # Calculate scores and update CSV cache
                    print("    ⚠ Scores not found in cache, calculating and updating...")
                    metrics_scores = score_stock_from_metrics(metrics)
                    
                    # Add scores to row data
                    row_data.update({
                        'metrics_trend_score': metrics_scores['Trend'],
                        'metrics_momentum_score': metrics_scores['Momentum'],
                        'metrics_volume_flow_score': metrics_scores['VolumeFlow'],
                        'metrics_volatility_penalty': metrics_scores['VolatilityPenalty']
                    })
                    
                    # Update the cached metrics with scores
                    metrics.update({
                        'metrics_trend_score': metrics_scores['Trend'],
                        'metrics_momentum_score': metrics_scores['Momentum'],
                        'metrics_volume_flow_score': metrics_scores['VolumeFlow'],
                        'metrics_volatility_penalty': metrics_scores['VolatilityPenalty']
                    })
                    
                    # Save updated metrics back to CSV cache
                    save_metrics_data(symbol, metrics)
                    
                    print(f"    ✓ Calculated and cached scores: Trend={metrics_scores['Trend']}, "
                          f"Momentum={metrics_scores['Momentum']}, "
                          f"VolumeFlow={metrics_scores['VolumeFlow']}, "
                          f"VolPenalty={metrics_scores['VolatilityPenalty']}")
                
                # Add some key raw metrics for reference
                row_data.update({
                    'price_vs_ma5': metrics['price_vs_ma5'],
                    'price_vs_ma10': metrics['price_vs_ma10'],
                    'rsi_5': metrics['rsi_5'],
                    'rsi_7': metrics['rsi_7'],
                    'vol_over_avg20': metrics['vol_over_avg20']
                })
                
            except Exception as e:
                print(f"    ✗ Error loading cached metrics: {e}")
                row_data.update({
                    'metrics_trend_score': None,
                    'metrics_momentum_score': None,
                    'metrics_volume_flow_score': None,
                    'metrics_volatility_penalty': None,
                    'price_vs_ma5': None,
                    'price_vs_ma10': None,
                    'rsi_5': None,
                    'rsi_7': None,
                    'vol_over_avg20': None
                })
        else:
            try:
                print("  Getting stock metrics...")
                metrics = get_stock_stats_metrics(symbol, trade_date)
                
                # Calculate scores from metrics
                metrics_scores = score_stock_from_metrics(metrics)
                
                # Add scores to the metrics dict so they get saved to metrics.csv
                metrics.update({
                    'metrics_trend_score': metrics_scores['Trend'],
                    'metrics_momentum_score': metrics_scores['Momentum'], 
                    'metrics_volume_flow_score': metrics_scores['VolumeFlow'],
                    'metrics_volatility_penalty': metrics_scores['VolatilityPenalty']
                })
                
                # Save raw metrics data + scores
                save_metrics_data(symbol, metrics)
                
                # Add metrics scores to row
                row_data.update({
                    'metrics_trend_score': metrics_scores['Trend'],
                    'metrics_momentum_score': metrics_scores['Momentum'],
                    'metrics_volume_flow_score': metrics_scores['VolumeFlow'],
                    'metrics_volatility_penalty': metrics_scores['VolatilityPenalty']
                })
                
                # Add some key raw metrics for reference
                row_data.update({
                    'price_vs_ma5': metrics['price_vs_ma5'],
                    'price_vs_ma10': metrics['price_vs_ma10'],
                    'rsi_5': metrics['rsi_5'],
                    'rsi_7': metrics['rsi_7'],
                    'vol_over_avg20': metrics['vol_over_avg20']
                })
                
                print(f"    ✓ Metrics scores: Trend={metrics_scores['Trend']}, "
                      f"Momentum={metrics_scores['Momentum']}, "
                      f"VolumeFlow={metrics_scores['VolumeFlow']}, "
                      f"VolPenalty={metrics_scores['VolatilityPenalty']}")
                
            except Exception as e:
                print(f"    ✗ Error getting stock metrics: {e}")
                row_data.update({
                    'metrics_trend_score': None,
                    'metrics_momentum_score': None,
                    'metrics_volume_flow_score': None,
                    'metrics_volatility_penalty': None,
                    'price_vs_ma5': None,
                    'price_vs_ma10': None,
                    'rsi_5': None,
                    'rsi_7': None,
                    'vol_over_avg20': None
                })
        
        # 2. Get and score news
        if check_news_exists(symbol, trade_date):
            print("  ✓ News data already exists, loading from cache...")
            try:
                # Try to get recent news summary (this looks at past 5 days)
                recent_news_result = sum_recent_news_scores(symbol, trade_date)
                row_data.update({
                    'news_avg_weighted_score': recent_news_result['average_weighted_score'],
                    'news_total_weighted_score': recent_news_result['total_weighted_score'],
                    'news_total_items': recent_news_result['total_news_items']
                })
                print(f"    ✓ Cached news summary: avg_weighted_score={recent_news_result['average_weighted_score']}, "
                      f"total_items={recent_news_result['total_news_items']}")
            except Exception as e:
                print(f"    ⚠ Cached news summary error: {e}")
                row_data.update({
                    'news_avg_weighted_score': None,
                    'news_total_weighted_score': None,
                    'news_total_items': None
                })
        else:
            try:
                print("  Getting news scores...")
                news_result = score_stock_from_news(symbol, trade_date)
                print(f"    ✓ News analysis completed")
                
                # Save news data to ticker-specific directory
                save_news_data(symbol, trade_date)
                
                # Try to get recent news summary (this looks at past 5 days)
                try:
                    recent_news_result = sum_recent_news_scores(symbol, trade_date)
                    row_data.update({
                        'news_avg_weighted_score': recent_news_result['average_weighted_score'],
                        'news_total_weighted_score': recent_news_result['total_weighted_score'],
                        'news_total_items': recent_news_result['total_news_items']
                    })
                    print(f"    ✓ Recent news summary: avg_weighted_score={recent_news_result['average_weighted_score']}, "
                          f"total_items={recent_news_result['total_news_items']}")
                except Exception as e:
                    print(f"    ⚠ Recent news summary error: {e}")
                    row_data.update({
                        'news_avg_weighted_score': None,
                        'news_total_weighted_score': None,
                        'news_total_items': None
                    })
                    
            except Exception as e:
                print(f"    ✗ Error getting news scores: {e}")
                row_data.update({
                    'news_avg_weighted_score': None,
                    'news_total_weighted_score': None,
                    'news_total_items': None
                })
        
        # 3. Calculate composite scores
        try:
            # Simple composite metrics score (average of positive scores minus volatility penalty)
            if all(x is not None for x in [row_data['metrics_trend_score'], 
                                           row_data['metrics_momentum_score'], 
                                           row_data['metrics_volume_flow_score']]):
                composite_metrics = (row_data['metrics_trend_score'] + 
                                   row_data['metrics_momentum_score'] + 
                                   row_data['metrics_volume_flow_score']) / 3
                
                if row_data['metrics_volatility_penalty'] is not None:
                    composite_metrics -= row_data['metrics_volatility_penalty'] * 0.5  # Penalty weight
                
                row_data['composite_metrics_score'] = round(composite_metrics, 2)
            else:
                row_data['composite_metrics_score'] = None
        except:
            row_data['composite_metrics_score'] = None
        
        results.append(row_data)
        print(f"  ✓ Completed {trade_date}")
        print()
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Save to CSV if requested
    if save_to_score_dir:
        # Create filename with timestamp and date range
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if start_date and end_date:
            date_range = f"{start_date}_to_{end_date}"
        else:
            date_range = f"recent_{num_days}days"
        filename = f"data/score/{symbol}_backtesting_scores_{date_range}_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"Results saved to: {filename}")
        
        # Also save a latest version for easy access
        latest_filename = f"data/score/{symbol}_latest_scores.csv"
        df.to_csv(latest_filename, index=False)
        print(f"Latest results saved to: {latest_filename}")
    
    # Print summary
    print("\nBACKTESTING SUMMARY")
    print("=" * 60)
    print(f"Symbol: {symbol}")
    print(f"Period: {df['trade_date'].min()} to {df['trade_date'].max()}")
    print(f"Trading days analyzed: {len(df)}")
    
    if 'composite_metrics_score' in df.columns:
        valid_composite = df['composite_metrics_score'].dropna()
        if len(valid_composite) > 0:
            print(f"Average composite metrics score: {valid_composite.mean():.2f}")
            print(f"Best day (metrics): {df.loc[df['composite_metrics_score'].idxmax(), 'trade_date']} "
                  f"(score: {df['composite_metrics_score'].max():.2f})")
            print(f"Worst day (metrics): {df.loc[df['composite_metrics_score'].idxmin(), 'trade_date']} "
                  f"(score: {df['composite_metrics_score'].min():.2f})")
    
    if 'news_avg_weighted_score' in df.columns:
        valid_news = df['news_avg_weighted_score'].dropna()
        if len(valid_news) > 0:
            print(f"Average news score: {valid_news.mean():.2f}")
    
    print(f"Total news items analyzed: {df['news_total_items'].sum()}")
    
    return df


def main():
    """Main function to run the backtesting pipeline"""
    # List of 10 major technology companies
    tech_companies = [
        "AAPL",  # Apple
        # "MSFT",  # Microsoft
        # "GOOGL", # Google/Alphabet
        # "AMZN",  # Amazon
        # "TSLA",  # Tesla
        # "META",  # Meta/Facebook
        # "NVDA",  # NVIDIA
        # "NFLX",  # Netflix
        # "ORCL",  # Oracle
        # "CRM"    # Salesforce
    ]
    
    all_results = []
    
    print(f"Running backtesting pipeline for {len(tech_companies)} technology companies...")
    print("Companies to analyze:", ", ".join(tech_companies))
    print("=" * 80)
    
    for i, symbol in enumerate(tech_companies):
        print(f"\n[{i+1}/{len(tech_companies)}] Processing {symbol}")
        print("=" * 60)
        
        try:
            df_result = run_pipeline(symbol, save_to_score_dir=True)
            if not df_result.empty:
                all_results.append(df_result)
                print(f"✓ Successfully processed {symbol}")
            else:
                print(f"⚠ No data returned for {symbol}")
        except Exception as e:
            print(f"✗ Error processing {symbol}: {e}")
            continue
    
    # Combine all results
    if all_results:
        df_combined = pd.concat(all_results, ignore_index=True)
        
        # Save combined results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        combined_filename = f"data/score/tech_companies_combined_scores_{timestamp}.csv"
        df_combined.to_csv(combined_filename, index=False)
        print(f"\nCombined results saved to: {combined_filename}")
        
        # Display summary for each company
        print("\nSUMMARY RESULTS BY COMPANY")
        print("=" * 80)
        
        for symbol in tech_companies:
            symbol_data = df_combined[df_combined['symbol'] == symbol]
            if not symbol_data.empty:
                avg_metrics = symbol_data['composite_metrics_score'].mean()
                avg_news = symbol_data['news_avg_weighted_score'].mean()
                total_news_items = symbol_data['news_total_items'].sum()
                
                print(f"{symbol:6s} | Avg Metrics: {avg_metrics:6.2f} | Avg News: {avg_news:6.2f} | News Items: {total_news_items:4.0f}")
            else:
                print(f"{symbol:6s} | No data available")
        
        # Display top performers
        print(f"\nTOP PERFORMERS (by composite metrics score)")
        print("-" * 60)
        top_performers = df_combined.groupby('symbol')['composite_metrics_score'].mean().sort_values(ascending=False)
        for symbol, score in top_performers.dropna().head(5).items():
            print(f"{symbol}: {score:.2f}")
        
        return df_combined
    else:
        print("No results to display")
        return pd.DataFrame()


if __name__ == "__main__":
    df = main()
