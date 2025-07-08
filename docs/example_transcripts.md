# Example Transcripts for Part 4: Custom API & RAG Integration

## 1. Product-KB Retrieval Endpoint (/products)

### Success Mode Examples

**Example 1: Coffee Cup Search**
```
User: "I want to buy a coffee cup"
API Call: GET /products?query=I want to buy a coffee cup
Response: {
  "query": "I want to buy a coffee cup",
  "answer": "I found several great coffee cups from ZUS Coffee! Here are your options:\n\n• ZUS All Day Cup 500ml (17oz) - Available in multiple collections including Aqua, Mountain, and Sundaze. Prices start from RM55.00 (regular RM79.00).\n\n• ZUS OG CUP 2.0 With Screw-On Lid 500ml (17oz) - Available in Thunder Blue, Space Black, and Lucky Pink. Currently on sale from RM55.00.\n\n• ZUS Frozee Cold Cup 650ml (22oz) - Perfect for cold drinks, available in Frost White, Pink, Green, and Peach colors for RM55.00.\n\nAll cups are high-quality, reusable, and come with various color options to match your style!",
  "success": true
}
```

**Example 2: Specific Product Search**
```
User: "Show me ZUS All Day Cup options"
API Call: GET /products?query=Show me ZUS All Day Cup options
Response: {
  "query": "Show me ZUS All Day Cup options",
  "answer": "Here are the ZUS All Day Cup options available:\n\n• ZUS All Day Cup 500ml (17oz) - Aqua Collection\n  Colors: Misty Blue, Ocean Breeze, Blue Lagoon, Deep Sea\n  Price: RM79.00\n\n• ZUS All Day Cup 500ml (17oz) - Mountain Collection\n  Colors: Soft Fern, Pine Green, Terrain Green, Forest Green\n  Price: RM79.00\n\n• ZUS All Day Cup 500ml (17oz) - Sundaze Collection\n  Colors: Seashell, Sand Castle, Tideline\n  Price: from RM55.00 (Regular RM79.00)\n\n• ZUS All Day Cup 500ml (17oz) - Standard Collection\n  Colors: Creamy Beige, Cherry Blossom, Fresh Mint, Fuzz Peach\n  Price: from RM55.00 (Regular RM79.00)\n\nAll cups are 500ml (17oz) capacity and come with various color options!",
  "success": true
}
```

### Failure Mode Examples

**Example 1: No Results Found**
```
User: "I want to buy a laptop"
API Call: GET /products?query=I want to buy a laptop
Response: {
  "query": "I want to buy a laptop",
  "answer": "Sorry, I couldn't find any products matching your query. Please try different keywords related to ZUS Coffee drinkware products.",
  "success": true
}
```

**Example 2: API Error**
```
User: "Show me coffee cups"
API Call: GET /products?query=Show me coffee cups
Response: {
  "detail": "Error during product search: OpenAI API quota exceeded"
}
```

## 2. Outlets Text2SQL Endpoint (/outlets)

### Success Mode Examples

**Example 1: Location-based Query**
```
User: "Show me all outlets in Petaling Jaya"
API Call: GET /outlets?query=Show me all outlets in Petaling Jaya
Response: {
  "query": "Show me all outlets in Petaling Jaya",
  "sql_query": "SELECT * FROM outlets WHERE LOWER(location) LIKE '%petaling jaya%'",
  "results": [
    {
      "id": 1,
      "name": "ZUS Coffee SS2",
      "location": "Petaling Jaya",
      "address": "No. 1, Jalan SS2/24, SS2, 47300 Petaling Jaya",
      "opening_hours": "7:00 AM - 11:00 PM",
      "phone": "+603-1234-5678",
      "services": "Coffee, Food, WiFi",
      "latitude": 3.1077,
      "longitude": 101.6067
    },
    {
      "id": 2,
      "name": "ZUS Coffee Damansara",
      "location": "Petaling Jaya",
      "address": "Damansara Uptown, 47400 Petaling Jaya",
      "opening_hours": "8:30 AM - 10:30 PM",
      "phone": "+603-1234-5679",
      "services": "Coffee, Food, WiFi, Drive-thru",
      "latitude": 3.1429,
      "longitude": 101.6177
    },
    {
      "id": 8,
      "name": "ZUS Coffee 1 Utama",
      "location": "Petaling Jaya",
      "address": "1 Utama Shopping Centre, 47800 Petaling Jaya",
      "opening_hours": "10:00 AM - 10:00 PM",
      "phone": "+603-1234-5685",
      "services": "Coffee, Food, WiFi, Drive-thru",
      "latitude": 3.1429,
      "longitude": 101.6177
    }
  ],
  "count": 3,
  "success": true
}
```

**Example 2: Service-based Query**
```
User: "Which outlets have drive-thru?"
API Call: GET /outlets?query=Which outlets have drive-thru?
Response: {
  "query": "Which outlets have drive-thru?",
  "sql_query": "SELECT * FROM outlets WHERE LOWER(services) LIKE '%drive%'",
  "results": [
    {
      "id": 2,
      "name": "ZUS Coffee Damansara",
      "location": "Petaling Jaya",
      "address": "Damansara Uptown, 47400 Petaling Jaya",
      "opening_hours": "8:30 AM - 10:30 PM",
      "phone": "+603-1234-5679",
      "services": "Coffee, Food, WiFi, Drive-thru",
      "latitude": 3.1429,
      "longitude": 101.6177
    },
    {
      "id": 8,
      "name": "ZUS Coffee 1 Utama",
      "location": "Petaling Jaya",
      "address": "1 Utama Shopping Centre, 47800 Petaling Jaya",
      "opening_hours": "10:00 AM - 10:00 PM",
      "phone": "+603-1234-5685",
      "services": "Coffee, Food, WiFi, Drive-thru",
      "latitude": 3.1429,
      "longitude": 101.6177
    }
  ],
  "count": 2,
  "success": true
}
```

**Example 3: Specific Outlet Query**
```
User: "Tell me about SS2 outlet"
API Call: GET /outlets?query=Tell me about SS2 outlet
Response: {
  "query": "Tell me about SS2 outlet",
  "sql_query": "SELECT * FROM outlets WHERE LOWER(name) LIKE '%ss2%' OR LOWER(name) LIKE '%ss 2%'",
  "results": [
    {
      "id": 1,
      "name": "ZUS Coffee SS2",
      "location": "Petaling Jaya",
      "address": "No. 1, Jalan SS2/24, SS2, 47300 Petaling Jaya",
      "opening_hours": "7:00 AM - 11:00 PM",
      "phone": "+603-1234-5678",
      "services": "Coffee, Food, WiFi",
      "latitude": 3.1077,
      "longitude": 101.6067
    }
  ],
  "count": 1,
  "success": true
}
```

### Failure Mode Examples

**Example 1: No Matching Results**
```
User: "Show me outlets in Mars"
API Call: GET /outlets?query=Show me outlets in Mars
Response: {
  "query": "Show me outlets in Mars",
  "sql_query": "SELECT * FROM outlets",
  "results": [],
  "count": 0,
  "success": true
}
```

**Example 2: Database Error**
```
User: "Show me all outlets"
API Call: GET /outlets?query=Show me all outlets
Response: {
  "detail": "Database connection failed"
}
```

## 3. Chatbot Integration (/chat)

### Success Mode Examples

**Example 1: Multi-turn Conversation with Product Search**
```
User: "Hello"
API Call: POST /chat
Request: {"query": "Hello"}
Response: {
  "response": "Hello! I'm your AI assistant. I can help you with outlet information, calculations, and product searches. How can I help you today?",
  "conversation_state": {
    "location": null,
    "outlet": null,
    "current_state": "initial",
    "conversation_history": [...],
    "confidence_score": 0.0
  }
}

User: "I want to buy a coffee cup"
API Call: POST /chat
Request: {"query": "I want to buy a coffee cup"}
Response: {
  "response": "I found several great coffee cups from ZUS Coffee! Here are your options:\n\n• ZUS All Day Cup 500ml (17oz) - Available in multiple collections including Aqua, Mountain, and Sundaze. Prices start from RM55.00 (regular RM79.00).\n\n• ZUS OG CUP 2.0 With Screw-On Lid 500ml (17oz) - Available in Thunder Blue, Space Black, and Lucky Pink. Currently on sale from RM55.00.\n\n• ZUS Frozee Cold Cup 650ml (22oz) - Perfect for cold drinks, available in Frost White, Pink, Green, and Peach colors for RM55.00.\n\nAll cups are high-quality, reusable, and come with various color options to match your style!",
  "conversation_state": {
    "location": null,
    "outlet": null,
    "current_state": "initial",
    "conversation_history": [...],
    "confidence_score": 0.0
  }
}
```

**Example 2: Multi-turn Conversation with Outlet Queries**
```
User: "Is there an outlet in Petaling Jaya?"
API Call: POST /chat
Request: {"query": "Is there an outlet in Petaling Jaya?"}
Response: {
  "response": "Yes! We have outlets in Petaling Jaya: SS 2, Damansara, 1 Utama. Which one are you interested in?",
  "conversation_state": {
    "location": "petaling jaya",
    "outlet": null,
    "current_state": "location_confirmed",
    "conversation_history": [...],
    "confidence_score": 0.8
  }
}

User: "SS 2"
API Call: POST /chat
Request: {"query": "SS 2"}
Response: {
  "response": "The SS 2 outlet opens at 9:00AM.",
  "conversation_state": {
    "location": "petaling jaya",
    "outlet": "ss 2",
    "current_state": "outlet_confirmed",
    "conversation_history": [...],
    "confidence_score": 0.9
  }
}
```

**Example 3: Calculator Integration**
```
User: "What is 15 plus 27?"
API Call: POST /chat
Request: {"query": "What is 15 plus 27?"}
Response: {
  "response": "The answer is 42.0.",
  "conversation_state": {
    "location": null,
    "outlet": null,
    "current_state": "initial",
    "conversation_history": [...],
    "confidence_score": 0.0
  }
}
```

### Failure Mode Examples

**Example 1: Calculator Service Unavailable**
```
User: "What is 10 divided by 2?"
API Call: POST /chat
Request: {"query": "What is 10 divided by 2?"}
Response: {
  "response": "Sorry, the calculator service is currently unavailable.",
  "conversation_state": {
    "location": null,
    "outlet": null,
    "current_state": "initial",
    "conversation_history": [...],
    "confidence_score": 0.0
  }
}
```

**Example 2: Product Search Error**
```
User: "Show me coffee products"
API Call: POST /chat
Request: {"query": "Show me coffee products"}
Response: {
  "response": "Sorry, I'm having trouble searching for products right now. Please try again later.",
  "conversation_state": {
    "location": null,
    "outlet": null,
    "current_state": "initial",
    "conversation_history": [...],
    "confidence_score": 0.0
  }
}
```

**Example 3: Invalid Input**
```
User: ""
API Call: POST /chat
Request: {"query": ""}
Response: {
  "response": "I didn't catch that. Could you please repeat your question?",
  "conversation_state": {
    "location": null,
    "outlet": null,
    "current_state": "initial",
    "conversation_history": [...],
    "confidence_score": 0.0
  }
}
```

## 4. Combined Workflow Example

**Complete Customer Journey:**
```
User: "Hello"
Bot: "Hello! I'm your AI assistant. I can help you with outlet information, calculations, and product searches. How can I help you today?"

User: "I want to buy a coffee cup and find a nearby outlet"
Bot: "I found several great coffee cups from ZUS Coffee! Here are your options:\n\n• ZUS All Day Cup 500ml (17oz) - Available in multiple collections including Aqua, Mountain, and Sundaze. Prices start from RM55.00 (regular RM79.00).\n\n• ZUS OG CUP 2.0 With Screw-On Lid 500ml (17oz) - Available in Thunder Blue, Space Black, and Lucky Pink. Currently on sale from RM55.00.\n\n• ZUS Frozee Cold Cup 650ml (22oz) - Perfect for cold drinks, available in Frost White, Pink, Green, and Peach colors for RM55.00.\n\nAll cups are high-quality, reusable, and come with various color options to match your style!\n\nFor nearby outlets, which area are you interested in? We have outlets in Petaling Jaya, Kuala Lumpur, Subang, and Puchong."

User: "Petaling Jaya"
Bot: "Yes! We have outlets in Petaling Jaya: SS 2, Damansara, 1 Utama. Which one are you interested in?"

User: "SS 2"
Bot: "The SS 2 outlet opens at 9:00AM."

User: "What time does it close?"
Bot: "The SS 2 outlet opens at 9:00AM."

User: "How much is the total for 2 coffee cups?"
Bot: "The answer is 110.0."
```

This demonstrates the complete integration of all three systems:
1. **Product RAG** - Provides detailed product information
2. **Text2SQL Outlets** - Queries outlet database for location and hours
3. **Calculator** - Performs price calculations
4. **State Management** - Maintains conversation context across turns 