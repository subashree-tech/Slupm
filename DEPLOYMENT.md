# Vercel Deployment Guide

## Quick Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**:
   ```bash
   vercel
   ```

4. **Set Environment Variable**:
   After deployment, go to your Vercel dashboard → Project Settings → Environment Variables
   Add: `OPENAI_API_KEY` = `your_openai_api_key_here`

5. **Redeploy** to apply the environment variable:
   ```bash
   vercel --prod
   ```

## API Endpoints

Once deployed, your API will be available at: `https://your-project-name.vercel.app`

### Available Endpoints:

1. **GET /** - API Status and Documentation
   - Returns API information and usage examples

2. **POST /api/slump** - Main Endpoint for Frontend
   - Explains why users feel tired/sluggish after eating

### Example Frontend Integration:

```javascript
// Example API call from your frontend
const response = await fetch('https://your-project-name.vercel.app/api/slump', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    time_of_day: 'midday',
    meal_type: 'heavy',
    symptoms: ['tired', 'sleepy'],
    food: 'biryani',
    user_question: 'Why do I feel sleepy after lunch?'
  })
});

const data = await response.json();
console.log(data.explanation);
```

### Required Request Body:
- `time_of_day`: "morning", "midday", or "night"
- `meal_type`: "light", "heavy", or "full"
- `symptoms`: Array of strings (e.g., ["tired", "sleepy", "bloated"])

### Optional Request Body:
- `food`: Specific food eaten (e.g., "biryani", "salad")
- `user_question`: Specific question from user

## Environment Variables Needed:
- `OPENAI_API_KEY`: Your OpenAI API key

## Notes:
- CORS is enabled for all origins
- The API uses OpenAI GPT-4o-mini model
- Responses are limited to 200 tokens for concise explanations
