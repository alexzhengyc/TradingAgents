import pandas as pd
import os
from datetime import datetime, timedelta
from openai import OpenAI

from .models import NewsList, NewsValidationList, NewsScoreList
from .constants import NEWS_TOPICS_DEFAULT


def clean_news_content(content: str) -> str:
    """Clean news content by removing URLs, extra spaces, and limiting to 500 characters"""
    import re
    
    # Remove URLs (http/https, www, and common URL patterns)
    url_pattern = r'https?://[^\s]+|www\.[^\s]+|[^\s]+\.[a-z]{2,3}(?:/[^\s]*)?'
    content = re.sub(url_pattern, '', content, flags=re.IGNORECASE)
    
    # Remove extra whitespace and strip
    content = re.sub(r'\s+', ' ', content).strip()
    
    # Limit to 500 characters
    if len(content) > 1000:
        content = content[:1000].rstrip() + "..."
    
    return content


def get_topic_news_openai(ticker: str, topic: str, date: str) -> NewsList:
    client = OpenAI()

    completion = client.chat.completions.parse(
        model="gpt-4.1",
        web_search_options={
            "search_context_size": "medium",
        },
        messages=[
            {
                "role": "user",
                "content": f"Can you search [{topic}] news for {ticker} happening exactly on {date} EST? Return up to five influential news related to the topic for {ticker} on {date}. Please dont return any news thats happening on other dates."
            }
        ],  
        response_format=NewsList,
    )

    return completion.choices[0].message.parsed


def validate_news_openai(symbol: str, date: str, news_content: list[str]) -> NewsValidationList:
    client = OpenAI()
    completion = client.chat.completions.parse(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": f"""Please validate the following news items for {symbol} on {date}. 
For each news item, determine:
1. is_wrong_date: If you find proof that the news is happening or written before {date} EST, return True.
2. is_informational: Does this news provide information to make trading decisions for {symbol} on {date}?
3. is_duplicate: Is this news a duplicate of another news item?

News items to validate:
{chr(10).join([f"{i+1}. {content}" for i, content in enumerate(news_content)])}
                """
            }
        ],
        response_format=NewsValidationList,
    )
    return completion.choices[0].message.parsed


def get_stock_news(symbol: str, date: str) -> str:
    """Scan all news to validate with OpenAI and save results to CSV"""
    # Get all news data
    all_news = []
    validated_news = []
    
    for topic_key, topic_description in NEWS_TOPICS_DEFAULT.items():
        initial_news = []

        # Get news from OpenAI
        try:
            topic = f"{topic_key}: {topic_description}"
            news_result = get_topic_news_openai(symbol, topic, date)
            if news_result and news_result.news:
                initial_news = [clean_news_content(news) for news in news_result.news]
        except Exception as e:
            print(f"Error getting {topic_key} news for {symbol}: {e}")
    
        # Validate news
        try:
            validation_results = validate_news_openai(symbol, date, initial_news)
            if validation_results and validation_results.validations:

                validations = validation_results.validations

                for i, (news_item, validation) in enumerate(zip(initial_news, validations)):
                    news_record = {
                        'date': date,
                        'topic': topic_key, 
                        'content': news_item,
                        'is_wrong_date': validation.is_wrong_date,
                        'is_informational': validation.is_informational,
                        'is_duplicate': validation.is_duplicate,
                    }
                    all_news.append(news_record)
                    if not validation.is_wrong_date and validation.is_informational and not validation.is_duplicate:
                        validated_news.append({
                            'date': date,
                            'topic': topic_key,
                            'content': news_item
                        })
        except Exception as e:
            print(f"Error validating news for {symbol}: {e}")
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_news)
    filename = f"data/news/{symbol}_news_all_{date.replace('-', '_')}.csv"
    df.to_csv(filename, index=False)

    df = pd.DataFrame(validated_news)
    filename = f"data/news/{symbol}_news_validated_{date.replace('-', '_')}.csv"
    df.to_csv(filename, index=False)    
    
    # Summary statistics
    total_items = len(all_news)
    informational_and_correct = sum(1 for item in all_news if item['is_informational'] and not item['is_wrong_date'] and not item['is_duplicate'])
    
    print(f"News validation completed for {symbol} on {date}")
    print(f"Total news items: {total_items}")
    print(f"Informational and correctly dated: {informational_and_correct}")
    print(f"Results saved to {filename}")
    
    return f"Validated {total_items} news items for {symbol}. {informational_and_correct} items passed validation. Results saved to {filename}"


def score_stock_from_news(symbol: str, date: str) -> dict:
    """Score each news item based on how the content is positive or negative for the stock price. Rated the news from -5 to 5."""
    # First get/validate the news
    validation_result = get_stock_news(symbol, date)
    print(validation_result)
    
    # Read the validated news from CSV
    try:
        filename = f"data/news/{symbol}_news_validated_{date.replace('-', '_')}.csv"
        validated_df = pd.read_csv(filename)
        
        if validated_df.empty:
            return {
                'symbol': symbol,
                'date': date,
                'total_news_items': 0,
                'average_score': 0,
                'news_scores': [],
                'summary': "No validated news items found"
            }
        
        # Prepare news content for scoring
        news_items = []
        for _, row in validated_df.iterrows():
            news_items.append(f"Topic: {row['topic']}\nContent: {row['content']}")
        
        # Get score scores from OpenAI
        client = OpenAI()
        
        completion = client.chat.completions.parse(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a stock market analyst. You are given a list of news items for a stock. You need to score each news item based on their potential impact on the stock price.

Use this scoring scale:
-5: Very negative impact (major bad news, significant risks)
-4: Negative impact (concerning developments)
-3: Somewhat negative (minor negative factors)
-2: Slightly negative (small concerns)
-1: Mildly negative (barely negative)
0: Neutral (no clear impact on stock price)
1: Mildly positive (barely positive)
2: Slightly positive (small positive factors)
3: Somewhat positive (minor positive developments)
4: Positive impact (good news, positive developments)
5: Very positive impact (major good news, significant opportunities)

For each news item, provide:
1. A score from -5 to 5
2. Very brief reasoning for the score"""
                },
                {
                    "role": "user",
                    "content": f"""News items to score:
{chr(10).join([f"{i+1}. {content}" for i, content in enumerate(news_items)])}
                    """
                }
            ],
            response_format=NewsScoreList,
        )
        
        scores = completion.choices[0].message.parsed.scores
        
        # Combine news data with scores
        scored_news = []
        total_score = 0
        
        for i, (_, row) in enumerate(validated_df.iterrows()):
            if i < len(scores):
                score_data = {
                    'topic': row['topic'],
                    'content': row['content'][:200] + "..." if len(row['content']) > 200 else row['content'],
                    'score': scores[i].score,
                    'reasoning': scores[i].reasoning
                }
                scored_news.append(score_data)
                total_score += scores[i].score
        
        # Calculate average score
        average_score = total_score / len(scored_news) if scored_news else 0
        
        # Save scored news to CSV
        scored_df = pd.DataFrame(scored_news)
        scored_filename = f"data/news/{symbol}_news_scored_{date.replace('-', '_')}.csv"
        scored_df.to_csv(scored_filename, index=False)
        
        return f"Scored {len(scored_news)} news items. Average score: {round(average_score, 2)}/5. Results saved to {scored_filename}"
        
    except FileNotFoundError:
        return f"No validated news file found for {symbol} on {date}"
    except Exception as e:
        return f"Error scoring news: {str(e)}"


def sum_recent_news_scores(symbol: str, date: str) -> dict:
    """Sum the recent 7 days news scores for a stock. Read the news scores from the CSV files and sum the scores * decay factor"""
    target_date = datetime.strptime(date, "%Y-%m-%d")
    total_weighted_score = 0
    total_news_items = 0
    daily_scores = []
    
    # Decay factors: more recent days have higher weight
    # Day 0 (today) = 1.0, Day 1 = 0.8, Day 2 = 0.64, etc. (0.8^days_back)
    decay_factor = 0.8
    
    for days_back in range(5):
        check_date = target_date - timedelta(days=days_back)
        date_str = check_date.strftime("%Y-%m-%d")
        
        # Check ticker-specific directory first (new format)
        filename_new = f"data/{symbol}/news_{date_str}.csv"
        # Fallback to global news directory (old format)
        filename_old = f"data/news/{symbol}_news_scored_{date_str.replace('-', '_')}.csv"
        
        daily_info = {
            'date': date_str,
            'news_count': 0,
            'raw_score': 0,
            'decay_weight': decay_factor ** days_back,
            'weighted_score': 0
        }
        
        # Try new format first, then fallback to old format
        filename = filename_new if os.path.exists(filename_new) else filename_old
        
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            if not df.empty and 'score' in df.columns:
                scores = df['score'].tolist()
                daily_raw_score = sum(scores)
                daily_weighted_score = daily_raw_score * (decay_factor ** days_back)
                
                daily_info.update({
                    'news_count': len(scores),
                    'raw_score': daily_raw_score,
                    'weighted_score': daily_weighted_score
                })
                
                total_weighted_score += daily_weighted_score
                total_news_items += len(scores)
        else:
            print(f"No news file found for {symbol} on {date_str}")
        
        daily_scores.append(daily_info)
    
    # Calculate average weighted score per news item if any news exists
    avg_weighted_score = total_weighted_score / total_news_items if total_news_items > 0 else 0
    
    return {
        'average_weighted_score': round(avg_weighted_score, 2),
        'total_weighted_score': round(total_weighted_score, 2),
        'total_news_items': total_news_items,
        'summary': f"Analyzed {total_news_items} news items over 7 days with average weighted score of {round(avg_weighted_score, 2)}"
    } 