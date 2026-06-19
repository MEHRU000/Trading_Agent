"""
News Manager utility to fetch and parse high-impact economic news from Forex Factory.
Includes a robust parsing mechanism, dynamic timezone conversion to UTC, and mock fallbacks.
"""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.utils.logger import app_logger

FOREX_FACTORY_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# In-memory cache variables for news events
_cached_news = None
_last_fetch_time = None


def is_us_dst(dt: datetime) -> bool:
    """
    Checks if Daylight Saving Time (DST) is active in the US for a given datetime.
    Starts on the second Sunday of March and ends on the first Sunday of November.
    """
    try:
        # Find second Sunday in March
        march_1st = datetime(dt.year, 3, 1)
        # weekday(): Monday=0, Sunday=6
        # Days to first Sunday: (6 - weekday)
        first_sun_march = 1 + ((6 - march_1st.weekday()) % 7)
        second_sun_march = first_sun_march + 7
        
        # Find first Sunday in November
        nov_1st = datetime(dt.year, 11, 1)
        first_sun_nov = 1 + ((6 - nov_1st.weekday()) % 7)
        
        dst_start = datetime(dt.year, 3, second_sun_march, 2)
        dst_end = datetime(dt.year, 11, first_sun_nov, 2)
        
        return dst_start <= dt < dst_end
    except Exception:
        # Default to True in summer months (April to October) as approximation fallback
        return 4 <= dt.month <= 10


def convert_eastern_to_utc(date_str: str, time_str: str) -> str:
    """
    Converts Eastern Time (EST/EDT) event date and time string into a UTC ISO-8601 string.
    
    Args:
        date_str: Date string in "MM-DD-YYYY" format (e.g., "06-09-2026")
        time_str: Time string in "H:MMam/pm" format (e.g., "8:30am", "12:00pm", "All Day", "Tentative")
        
    Returns:
        str: ISO-8601 formatted UTC timestamp (e.g. "2026-06-09T12:30:00Z")
    """
    # Clean inputs
    date_str = date_str.strip()
    time_str = time_str.strip().lower().replace(" ", "")
    
    try:
        # Parse base date
        base_dt = datetime.strptime(date_str, "%m-%d-%Y")
    except Exception:
        # If date format fails, return current time ISO
        return datetime.utcnow().strftime("%Y-%m-%dT00:00:00Z")

    # If time is non-numeric (e.g., All Day or Tentative), set to midnight Eastern
    if not time_str or any(x in time_str for x in ["day", "tentative", "tba"]):
        hour, minute = 0, 0
    else:
        try:
            # Strip am/pm
            is_pm = "pm" in time_str
            time_digits = time_str.replace("am", "").replace("pm", "")
            
            if ":" in time_digits:
                parts = time_digits.split(":")
                hour = int(parts[0])
                minute = int(parts[1])
            else:
                hour = int(time_digits)
                minute = 0
                
            if is_pm and hour < 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
        except Exception:
            hour, minute = 0, 0

    # Create local datetime
    local_dt = datetime(base_dt.year, base_dt.month, base_dt.day, hour, minute)
    
    # Calculate offset (EDT is UTC-4, EST is UTC-5)
    offset_hours = 4 if is_us_dst(local_dt) else 5
    
    # Add offset to get UTC time
    utc_dt = local_dt + timedelta(hours=offset_hours)
    
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_forex_factory_news(force: bool = False) -> List[Dict[str, Any]]:
    """
    Fetches the Forex Factory weekly calendar XML, parses it, and filters for
    today's major economic news events (High/Medium impact, focusing on USD and major currencies).
    
    Includes an in-memory caching layer with dynamic TTL:
    - Default cache duration is 15 minutes.
    - Accelerates to a 30-second TTL if a scheduled news event is within 5 minutes of now.
    """
    global _cached_news, _last_fetch_time
    now = datetime.utcnow()
    
    # 1. Determine cache TTL (accelerates near releases to display actual values on time)
    cache_duration = timedelta(minutes=15)
    if not force and _cached_news:
        for event in _cached_news:
            iso = event.get("iso_time")
            if iso:
                try:
                    event_time = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")
                    time_diff = abs((event_time - now).total_seconds())
                    # If within 5 minutes (300s) of any event, reduce TTL to 30 seconds
                    if time_diff <= 300:
                        cache_duration = timedelta(seconds=30)
                        break
                except Exception:
                    continue

    # 2. Return cached news if TTL is still valid
    if not force and _cached_news is not None and _last_fetch_time is not None:
        if now - _last_fetch_time < cache_duration:
            app_logger.debug("Returning cached economic calendar news events.")
            return _cached_news

    # 3. Fetch fresh news from Forex Factory
    try:
        app_logger.info(f"Fetching Forex Factory economic calendar from: {FOREX_FACTORY_URL}")
        
        req = urllib.request.Request(
            FOREX_FACTORY_URL,
            headers={"User-Agent": USER_AGENT}
        )
        
        with urllib.request.urlopen(req, timeout=8) as response:
            xml_data = response.read()
            
        parsed_events = parse_news_xml(xml_data)
        if parsed_events:
            _cached_news = parsed_events
            _last_fetch_time = now
            return _cached_news
            
    except Exception as e:
        app_logger.error(f"Error fetching Forex Factory news: {e}. Utilizing fallback news feed.")
        if _cached_news is not None:
            app_logger.info("Utilizing expired cached news events as fallback.")
            return _cached_news
        else:
            # Cache the fallback news to prevent hammering during rate-limits or offline periods
            _cached_news = get_fallback_news()
            _last_fetch_time = now
            return _cached_news
            
    return get_fallback_news()


def parse_news_xml(xml_data: bytes) -> List[Dict[str, Any]]:
    """
    Parses XML data from Forex Factory calendar and returns structured news list.
    """
    try:
        root = ET.fromstring(xml_data)
    except Exception as parse_err:
        app_logger.error(f"Failed to parse news XML: {parse_err}")
        return get_fallback_news()

    news_events = []
    today_str = datetime.utcnow().strftime("%m-%d-%Y") # e.g. "06-09-2026"
    
    # Forex Factory date format inside XML is MM-DD-YYYY
    for event in root.findall("event"):
        try:
            title = event.find("title").text if event.find("title") is not None else "Unknown Event"
            country = event.find("country").text if event.find("country") is not None else "USD"
            date_val = event.find("date").text if event.find("date") is not None else ""
            time_val = event.find("time").text if event.find("time") is not None else ""
            impact = event.find("impact").text if event.find("impact") is not None else "Low"
            forecast = event.find("forecast").text if event.find("forecast") is not None else ""
            previous = event.find("previous").text if event.find("previous") is not None else ""

            # Standardize empty values
            forecast = forecast if forecast else "—"
            previous = previous if previous else "—"

            # Filter for USD or major currencies
            if country in ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"] and impact in ["High", "Medium", "Low"]:
                event_date = date_val.strip()
                event_time = time_val.strip()
                
                # Convert Eastern Time (Forex Factory standard) to UTC ISO format
                iso_time = convert_eastern_to_utc(event_date, event_time)
                
                news_events.append({
                    "title": title.strip(),
                    "country": country.strip(),
                    "date": event_date,
                    "time": event_time,
                    "iso_time": iso_time,
                    "impact": impact.strip(),
                    "forecast": forecast.strip(),
                    "previous": previous.strip()
                })
        except Exception as item_err:
            app_logger.warning(f"Error parsing news XML event node: {item_err}")
            continue

    if not news_events:
        return get_fallback_news()
    return news_events


def get_fallback_news() -> List[Dict[str, Any]]:
    """
    Returns a realistic list of mock USD/EUR/GBP/AUD high/medium/low-impact economic events
    spread across the current week as fallback when Forex Factory is unreachable.
    """
    from datetime import datetime, timedelta
    today = datetime.utcnow()
    
    today_str = today.strftime("%m-%d-%Y")
    tomorrow_str = (today + timedelta(days=1)).strftime("%m-%d-%Y")
    day_2_str = (today + timedelta(days=2)).strftime("%m-%d-%Y")
    day_3_str = (today + timedelta(days=3)).strftime("%m-%d-%Y")
    day_4_str = (today + timedelta(days=4)).strftime("%m-%d-%Y")

    return [
        # Today
        {
            "title": "Core CPI m/m (Consumer Price Index)",
            "country": "USD",
            "date": today_str,
            "time": "8:30am",
            "iso_time": convert_eastern_to_utc(today_str, "8:30am"),
            "impact": "High",
            "forecast": "0.3%",
            "previous": "0.2%"
        },
        {
            "title": "CPI y/y (Consumer Inflation)",
            "country": "USD",
            "date": today_str,
            "time": "8:30am",
            "iso_time": convert_eastern_to_utc(today_str, "8:30am"),
            "impact": "High",
            "forecast": "3.1%",
            "previous": "3.4%"
        },
        {
            "title": "ECB Press Conference",
            "country": "EUR",
            "date": today_str,
            "time": "9:15am",
            "iso_time": convert_eastern_to_utc(today_str, "9:15am"),
            "impact": "High",
            "forecast": "—",
            "previous": "—"
        },
        {
            "title": "Unemployment Claims",
            "country": "USD",
            "date": today_str,
            "time": "8:30am",
            "iso_time": convert_eastern_to_utc(today_str, "8:30am"),
            "impact": "Medium",
            "forecast": "215K",
            "previous": "220K"
        },
        {
            "title": "FOMC Statement (Federal Open Market Committee)",
            "country": "USD",
            "date": today_str,
            "time": "2:00pm",
            "iso_time": convert_eastern_to_utc(today_str, "2:00pm"),
            "impact": "High",
            "forecast": "—",
            "previous": "—"
        },
        {
            "title": "Federal Funds Rate (Interest Rate Cut Decision)",
            "country": "USD",
            "date": today_str,
            "time": "2:00pm",
            "iso_time": convert_eastern_to_utc(today_str, "2:00pm"),
            "impact": "High",
            "forecast": "5.25%",
            "previous": "5.50%"
        },
        # Tomorrow
        {
            "title": "Retail Sales m/m",
            "country": "USD",
            "date": tomorrow_str,
            "time": "8:30am",
            "iso_time": convert_eastern_to_utc(tomorrow_str, "8:30am"),
            "impact": "High",
            "forecast": "0.4%",
            "previous": "0.1%"
        },
        {
            "title": "Core Retail Sales m/m",
            "country": "USD",
            "date": tomorrow_str,
            "time": "8:30am",
            "iso_time": convert_eastern_to_utc(tomorrow_str, "8:30am"),
            "impact": "Medium",
            "forecast": "0.2%",
            "previous": "0.2%"
        },
        {
            "title": "Flash Manufacturing PMI",
            "country": "EUR",
            "date": tomorrow_str,
            "time": "4:00am",
            "iso_time": convert_eastern_to_utc(tomorrow_str, "4:00am"),
            "impact": "Medium",
            "forecast": "47.8",
            "previous": "47.3"
        },
        {
            "title": "Gov Council Member Speaks",
            "country": "GBP",
            "date": tomorrow_str,
            "time": "11:30am",
            "iso_time": convert_eastern_to_utc(tomorrow_str, "11:30am"),
            "impact": "Low",
            "forecast": "—",
            "previous": "—"
        },
        # Day 2 (Upcoming)
        {
            "title": "Empire State Manufacturing Index",
            "country": "USD",
            "date": day_2_str,
            "time": "8:30am",
            "iso_time": convert_eastern_to_utc(day_2_str, "8:30am"),
            "impact": "Medium",
            "forecast": "-11.2",
            "previous": "-14.3"
        },
        {
            "title": "BOE Inflation Letters",
            "country": "GBP",
            "date": day_2_str,
            "time": "7:00am",
            "iso_time": convert_eastern_to_utc(day_2_str, "7:00am"),
            "impact": "High",
            "forecast": "—",
            "previous": "—"
        },
        # Day 3 (Upcoming)
        {
            "title": "Philly Fed Manufacturing Index",
            "country": "USD",
            "date": day_3_str,
            "time": "8:30am",
            "iso_time": convert_eastern_to_utc(day_3_str, "8:30am"),
            "impact": "Medium",
            "forecast": "10.4",
            "previous": "15.2"
        },
        {
            "title": "Existing Home Sales",
            "country": "USD",
            "date": day_3_str,
            "time": "10:00am",
            "iso_time": convert_eastern_to_utc(day_3_str, "10:00am"),
            "impact": "Low",
            "forecast": "4.15M",
            "previous": "4.10M"
        },
        # Day 4 (Upcoming)
        {
            "title": "RBA Rate Statement",
            "country": "AUD",
            "date": day_4_str,
            "time": "12:30am",
            "iso_time": convert_eastern_to_utc(day_4_str, "12:30am"),
            "impact": "High",
            "forecast": "4.35%",
            "previous": "4.35%"
        }
    ]
