from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

IP_INFO_API = "http://ip-api.com/json/"
WEATHER_API = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_API_KEY = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):
    # Get client IP address
    client_ip = request.client.host

    # Get location data from IP address
    location_response = requests.get(f"{IP_INFO_API}{client_ip}")
    if location_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get location data")
    location_data = location_response.json()
    city = location_data.get("city", "Unknown")
    
    # Get weather data for the location
    weather_response = requests.get(f"{WEATHER_API}?q={city}&units=metric&appid={WEATHER_API_KEY}")
    if weather_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get weather data")
    weather_data = weather_response.json()
    temperature = weather_data["main"]["temp"]
    
    # Create the response
    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    
    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
