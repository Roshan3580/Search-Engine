# Assignment3
**TEST.txt**

# Test Queries and Performance Analysis

## Initial Test Queries
1. **"climate change effects"**  
   - Initial Performance: Retrieved too many irrelevant documents.
   - Improvement: Implemented TF-IDF ranking to prioritize relevant results.

2. **"industrial pollution impact"**  
   - Initial Performance: Some documents with "pollution" but not "industrial" appeared at the top.
   - Improvement: Applied stemming to unify variations of words (e.g., "industry" → "industri").

3. **"green energy policy"**  
   - Initial Performance: Retrieved documents about "policy" but not necessarily "green energy."
   - Improvement: Adjusted query processing to ensure multi-term relevance.

4. **"air quality regulations"**  
   - Initial Performance: Retrieved too many results due to common words "air" and "quality."
   - Improvement: Tuned ranking to weigh term frequency and document significance better.

5. **"environmental justice laws"**  
   - Initial Performance: Some documents discussing "justice" but unrelated to the environment were included.
   - Improvement: Enhanced tokenization to filter out less relevant context.

