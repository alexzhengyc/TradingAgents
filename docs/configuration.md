# TradingAgents Configuration Guide

This document provides a comprehensive guide to configuring and customizing the TradingAgents system for different use cases, LLM providers, and analysis requirements.

## 🔧 Configuration Overview

TradingAgents uses a flexible configuration system that allows customization of:

- **LLM Providers**: OpenAI, Anthropic, Google Gemini, Ollama, OpenRouter
- **Agent Selection**: Choose which analysts to include
- **Analysis Depth**: Configure debate rounds and research intensity  
- **Data Sources**: Online vs offline data modes
- **Performance Settings**: Optimize for speed vs quality

## 📋 Default Configuration

The system ships with sensible defaults in `tradingagents/default_config.py`:

```python
DEFAULT_CONFIG = {
    # Directory Settings
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": "/Users/yluo/Documents/Code/ScAI/FR1-data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    
    # LLM Settings
    "llm_provider": "openai",
    "deep_think_llm": "o4-mini",              # For complex reasoning tasks
    "quick_think_llm": "gpt-4o-mini",         # For routine analysis
    "backend_url": "https://api.openai.com/v1",
    
    # Debate and Discussion Settings
    "max_debate_rounds": 1,                   # Research team debate rounds
    "max_risk_discuss_rounds": 1,             # Risk management rounds
    "max_recur_limit": 100,                   # LangGraph recursion limit
    
    # Tool Settings
    "online_tools": True,                     # Use real-time data vs cached
}
```

## 🤖 LLM Provider Configuration

### OpenAI Configuration
```python
openai_config = {
    "llm_provider": "openai",
    "backend_url": "https://api.openai.com/v1",
    "deep_think_llm": "o1-preview",           # Best reasoning model
    "quick_think_llm": "gpt-4o-mini",         # Fast and cost-effective
}

# Environment variables required:
# export OPENAI_API_KEY=your_api_key
```

**Available OpenAI Models**:
```python
openai_models = {
    # Deep Thinking (Complex Reasoning)
    "o1-preview": "Most capable reasoning model",
    "o1-mini": "Faster reasoning model", 
    "gpt-4o": "Latest GPT-4 model",
    
    # Quick Thinking (Routine Tasks)
    "gpt-4o-mini": "Cost-effective GPT-4 model",
    "gpt-4": "Reliable GPT-4 baseline",
    "gpt-3.5-turbo": "Fast and economical"
}
```

### Anthropic Configuration
```python
anthropic_config = {
    "llm_provider": "anthropic", 
    "backend_url": "https://api.anthropic.com/v1",
    "deep_think_llm": "claude-3-opus-20240229",
    "quick_think_llm": "claude-3-haiku-20240307",
}

# Environment variables required:
# export ANTHROPIC_API_KEY=your_api_key
```

**Available Anthropic Models**:
```python
anthropic_models = {
    # Deep Thinking
    "claude-3-opus-20240229": "Most capable Claude model",
    "claude-3-sonnet-20240229": "Balanced performance",
    
    # Quick Thinking  
    "claude-3-haiku-20240307": "Fast and economical",
    "claude-3-5-sonnet-20241022": "Latest Sonnet model"
}
```

### Google Gemini Configuration
```python
gemini_config = {
    "llm_provider": "google",
    "backend_url": "https://generativelanguage.googleapis.com/v1", 
    "deep_think_llm": "gemini-2.0-flash-exp",
    "quick_think_llm": "gemini-2.0-flash",
}

# Environment variables required:
# export GOOGLE_API_KEY=your_api_key
```

**Available Gemini Models**:
```python
gemini_models = {
    # Deep Thinking
    "gemini-2.0-flash-exp": "Latest experimental model",
    "gemini-1.5-pro": "High-capability model",
    
    # Quick Thinking
    "gemini-2.0-flash": "Fast and efficient",
    "gemini-1.5-flash": "Balanced speed/performance"
}
```

### Local Ollama Configuration
```python
ollama_config = {
    "llm_provider": "ollama",
    "backend_url": "http://localhost:11434/v1",
    "deep_think_llm": "llama3.1:70b",
    "quick_think_llm": "llama3.1:8b",
}

# No API key required - runs locally
```

**Available Ollama Models**:
```python
ollama_models = {
    # Deep Thinking (Larger Models)
    "llama3.1:70b": "Large Llama model for complex reasoning",
    "mixtral:8x7b": "Mixture of experts model",
    
    # Quick Thinking (Smaller Models)
    "llama3.1:8b": "Fast general-purpose model", 
    "qwen2.5:7b": "Efficient reasoning model",
    "phi3:mini": "Compact Microsoft model"
}
```

### OpenRouter Configuration
```python
openrouter_config = {
    "llm_provider": "openrouter",
    "backend_url": "https://openrouter.ai/api/v1",
    "deep_think_llm": "anthropic/claude-3-opus",
    "quick_think_llm": "anthropic/claude-3-haiku",
}

# Environment variables required:
# export OPENROUTER_API_KEY=your_api_key
```

## 👥 Agent Selection Configuration

### Analyst Team Selection
Choose which analysts to include in your analysis:

```python
# Full analyst team (default)
selected_analysts = ["market", "social", "news", "fundamentals"]

# Technical analysis focus
technical_focus = ["market", "fundamentals"]

# Sentiment-driven analysis  
sentiment_focus = ["social", "news"]

# Fundamental analysis only
fundamental_only = ["fundamentals"]

# Custom combinations
custom_selection = ["market", "news"]  # Market + news analysis
```

**Agent Configuration Examples**:
```python
# Day trading configuration (fast execution)
day_trading_config = {
    "selected_analysts": ["market", "social"],    # Quick sentiment + technical
    "max_debate_rounds": 1,                       # Minimal debate
    "quick_think_llm": "gpt-4o-mini",            # Fast model
    "online_tools": True                          # Real-time data
}

# Long-term investment configuration (thorough analysis)
long_term_config = {
    "selected_analysts": ["market", "social", "news", "fundamentals"],
    "max_debate_rounds": 3,                       # Thorough debate
    "max_risk_discuss_rounds": 2,                 # Detailed risk analysis
    "deep_think_llm": "o1-preview",              # Best reasoning
    "online_tools": True
}

# Research/backtesting configuration (consistent data)
research_config = {
    "selected_analysts": ["market", "fundamentals"],
    "max_debate_rounds": 2,
    "online_tools": False,                        # Cached data for consistency
    "quick_think_llm": "gpt-4o-mini"             # Cost-effective
}
```

## 🎯 Analysis Depth Configuration

### Debate Intensity Settings
Control the depth and quality of agent discussions:

```python
# Quick analysis (1-2 minutes)
quick_analysis = {
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
}

# Balanced analysis (5-10 minutes)  
balanced_analysis = {
    "max_debate_rounds": 2,
    "max_risk_discuss_rounds": 2,
}

# Deep analysis (15-30 minutes)
deep_analysis = {
    "max_debate_rounds": 4,
    "max_risk_discuss_rounds": 3,
}

# Research-grade analysis (30+ minutes)
research_analysis = {
    "max_debate_rounds": 6,
    "max_risk_discuss_rounds": 4,
}
```

### Performance vs Quality Trade-offs
```python
# Speed-optimized configuration
speed_config = {
    "selected_analysts": ["market"],              # Single analyst
    "max_debate_rounds": 1,                       # Minimal debate
    "quick_think_llm": "gpt-4o-mini",            # Fast model
    "deep_think_llm": "gpt-4o-mini",             # Same model for consistency
    "online_tools": False,                        # Cached data
}

# Quality-optimized configuration  
quality_config = {
    "selected_analysts": ["market", "social", "news", "fundamentals"],
    "max_debate_rounds": 5,                       # Extensive debate
    "max_risk_discuss_rounds": 3,                 # Thorough risk analysis
    "quick_think_llm": "gpt-4o",                 # High-quality model
    "deep_think_llm": "o1-preview",              # Best reasoning model
    "online_tools": True,                         # Real-time data
}
```

## 📊 Data Source Configuration

### Online vs Offline Data
```python
# Online mode: Real-time data with higher costs
online_config = {
    "online_tools": True,
    # Pros: Latest data, real-time market conditions
    # Cons: Higher API costs, variable data, rate limits
}

# Offline mode: Cached data for consistency
offline_config = {
    "online_tools": False,
    # Pros: No API costs, consistent data, faster execution
    # Cons: Limited to cached date range (2015-2025)
}
```

### Data Directory Configuration
```python
# Custom data directories
custom_data_config = {
    "data_dir": "/path/to/your/financial/data",           # Main data directory
    "data_cache_dir": "/path/to/cache",                   # Runtime cache
    "results_dir": "/path/to/results",                    # Output directory
}

# Environment variable override
# export TRADINGAGENTS_RESULTS_DIR=/custom/results/path
```

## 🎛️ Advanced Configuration

### Memory System Configuration
```python
memory_config = {
    "embedding_model": "text-embedding-3-small",         # OpenAI embeddings
    "vector_store": "chroma",                             # Vector database
    "memory_retrieval_count": 2,                          # Memories per query
    "memory_similarity_threshold": 0.7,                   # Relevance threshold
}

# For Ollama (local embeddings)
ollama_memory_config = {
    "embedding_model": "nomic-embed-text",                # Local embeddings
    "vector_store": "chroma",
    "memory_retrieval_count": 3,
}
```

### API Rate Limiting
```python
rate_limit_config = {
    "openai_requests_per_minute": 500,
    "anthropic_requests_per_minute": 50,
    "finnhub_requests_per_minute": 60,
    "max_concurrent_requests": 10,
    "retry_attempts": 3,
    "retry_delay": 1.0,  # seconds
}
```

### Graph Execution Settings
```python
execution_config = {
    "max_recur_limit": 150,                               # LangGraph recursion limit
    "stream_mode": "values",                              # Streaming mode
    "timeout": 1800,                                      # 30 minutes timeout
    "parallel_execution": True,                           # Enable parallelization
}
```

## 🔧 Configuration Examples

### Example 1: Cost-Optimized Configuration
```python
cost_optimized_config = DEFAULT_CONFIG.copy()
cost_optimized_config.update({
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",                     # Cheaper alternative
    "quick_think_llm": "gpt-4o-mini",                    # Same model
    "max_debate_rounds": 1,                              # Minimal debate
    "max_risk_discuss_rounds": 1,                        # Quick risk check
    "online_tools": False,                               # No API costs for data
})

# Estimated cost: $0.10-0.50 per analysis
```

### Example 2: High-Quality Research Configuration
```python
research_config = DEFAULT_CONFIG.copy()
research_config.update({
    "llm_provider": "openai",
    "deep_think_llm": "o1-preview",                      # Best reasoning
    "quick_think_llm": "gpt-4o",                        # High-quality analysis
    "selected_analysts": ["market", "social", "news", "fundamentals"],
    "max_debate_rounds": 4,                              # Thorough debate
    "max_risk_discuss_rounds": 3,                        # Detailed risk analysis
    "online_tools": True,                                # Latest data
})

# Estimated cost: $5-15 per analysis
```

### Example 3: Local Deployment Configuration
```python
local_config = DEFAULT_CONFIG.copy()
local_config.update({
    "llm_provider": "ollama",
    "backend_url": "http://localhost:11434/v1",
    "deep_think_llm": "llama3.1:70b",                   # Large local model
    "quick_think_llm": "llama3.1:8b",                   # Fast local model
    "online_tools": False,                               # Use cached data
    "max_debate_rounds": 2,                              # Balanced analysis
})

# Cost: Free (after hardware/setup costs)
```

### Example 4: Production Trading Configuration
```python
production_config = DEFAULT_CONFIG.copy()
production_config.update({
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-opus-20240229",         # Reliable reasoning
    "quick_think_llm": "claude-3-sonnet-20240229",      # Balanced performance
    "selected_analysts": ["market", "news", "fundamentals"],
    "max_debate_rounds": 2,                              # Reasonable depth
    "max_risk_discuss_rounds": 2,                        # Thorough risk analysis
    "online_tools": True,                                # Real-time data
    "timeout": 900,                                      # 15 minute timeout
})
```

## 🔄 Dynamic Configuration

### Runtime Configuration Updates
```python
def create_custom_config(use_case="balanced"):
    """Create configuration based on use case"""
    base_config = DEFAULT_CONFIG.copy()
    
    configs = {
        "speed": {
            "selected_analysts": ["market"],
            "max_debate_rounds": 1,
            "quick_think_llm": "gpt-4o-mini",
            "online_tools": False
        },
        "balanced": {
            "selected_analysts": ["market", "news"],
            "max_debate_rounds": 2,
            "max_risk_discuss_rounds": 2,
        },
        "thorough": {
            "selected_analysts": ["market", "social", "news", "fundamentals"],
            "max_debate_rounds": 3,
            "max_risk_discuss_rounds": 3,
            "deep_think_llm": "o1-preview"
        }
    }
    
    base_config.update(configs.get(use_case, configs["balanced"]))
    return base_config

# Usage
config = create_custom_config("thorough")
ta = TradingAgentsGraph(config=config)
```

### Environment-Based Configuration
```python
import os

def get_env_config():
    """Load configuration from environment variables"""
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables if present
    env_overrides = {
        "llm_provider": os.getenv("LLM_PROVIDER"),
        "deep_think_llm": os.getenv("LLM_DEEP_THINK_MODEL"),
        "quick_think_llm": os.getenv("LLM_QUICK_THINK_MODEL"),
        "backend_url": os.getenv("LLM_BACKEND_URL"),
        "online_tools": os.getenv("ONLINE_TOOLS", "true").lower() == "true",
    }
    
    # Apply non-None overrides
    for key, value in env_overrides.items():
        if value is not None:
            config[key] = value
    
    return config

# Usage with environment variables
# export LLM_PROVIDER=anthropic
# export LLM_DEEP_THINK_MODEL=claude-3-opus-20240229
config = get_env_config()
```

## 📝 Configuration Validation

### Validation Functions
```python
def validate_config(config):
    """Validate configuration settings"""
    required_keys = [
        "llm_provider", "deep_think_llm", "quick_think_llm", 
        "max_debate_rounds", "max_risk_discuss_rounds"
    ]
    
    # Check required keys
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValueError(f"Missing configuration keys: {missing_keys}")
    
    # Validate LLM provider
    valid_providers = ["openai", "anthropic", "google", "ollama", "openrouter"]
    if config["llm_provider"] not in valid_providers:
        raise ValueError(f"Invalid LLM provider: {config['llm_provider']}")
    
    # Validate debate rounds
    if config["max_debate_rounds"] < 1 or config["max_debate_rounds"] > 10:
        raise ValueError("max_debate_rounds must be between 1 and 10")
    
    return True

# Usage
try:
    validate_config(my_config)
    ta = TradingAgentsGraph(config=my_config)
except ValueError as e:
    print(f"Configuration error: {e}")
```

This configuration system provides maximum flexibility while maintaining sensible defaults, allowing you to optimize TradingAgents for your specific use case, budget, and performance requirements. 