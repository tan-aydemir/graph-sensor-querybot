import json
import openai
from datetime import datetime

# Set up API
client = openai.OpenAI(api_key="placeholder - add yours")

"""
check if it's in the prompt (temperature, or other sensor, or time interval)
"""

# Pull out relevant data based on user input - and not all the data
def get_relevant_information(question, full_json_path="data/dorm_timeseries_1day_custom.json"):
    # We first ask GPT to pull out a structured filter from the user's natural language question
    schema_extraction_messages = [
        {
            "role": "system",
            "content": (
                "You must extract structured filters from questions about dormitory sensor data. "
                "Return JSON like:\n"
                "{\n"
                "  'rooms': ['Dorm_101'],\n"
                "  'sensor_types': ['temperature'],\n"
                "  'start_time': '2025-05-01T00:00:00',\n"
                "  'end_time': '2025-05-02T00:00:00'\n"
                "}\n"
                "If no time is specified, use full day of May 1, 2025."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # Forward user input
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=schema_extraction_messages,
        temperature=0,  # set to 0 to reduce creativity and encourage deterministic output
        max_tokens=200
    )

    # Parse the response into a dictionary
    try:
        filters = json.loads(response.choices[0].message.content.replace("'", "\""))
    except json.JSONDecodeError:
        # If GPT's output isn't valid JSON, fall back to a default time window and all rooms or sensors. 
        filters = {
            "rooms": [],
            "sensor_types": ["temperature", "occupancy"],
            "start_time": "2025-05-01T00:00:00",
            "end_time": "2025-05-02T00:00:00"
        }

    #Load full JSON - for it to be later reduced into relevant pieces
    with open(full_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Keep just the relevant information
    filtered_data = []
    for row in data:
        #If a room filter exists and this row's room isn't in it, continue
        if filters.get("rooms") and row.get("room") not in filters["rooms"]:
            continue
        #If we have start and end times, check if the row falls within that window
        if filters.get("start_time") and filters.get("end_time"):
            if not (filters["start_time"] <= row.get("timestamp", "") <= filters["end_time"]):
                continue
        #If it passed all the filters, keep it
        filtered_data.append(row)

    return filtered_data

#main method that combines two JSON files
def query_graph_nlp(question):
    # Load graph structure
    with open("data/relations.json", "r", encoding="utf-8-sig") as f:
        graph_data = json.load(f)
    formatted_graph = json.dumps(graph_data, indent=2)

    #Pull only the relevant rows of sensor data based on the user's question
    sensor_data = get_relevant_information(question)
    formatted_sensors = json.dumps(sensor_data, indent=2)

    #Build the full prompt for the model
    messages = [
        {
            "role": "system",
            "content": (
                "You analyze dormitory layout and sensor data to answer user queries. "
                "Here is the graph structure:\n"
                f"{formatted_graph}\n\n"
                "And the filtered sensor data:\n"
                f"{formatted_sensors}\n\n"
                "Please respond accurately and clearly. Do not use asterisks for bolding."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    #Call GPT with the full message stack
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=400,
        temperature=0.3  # Low temperature to prevent the model from dreaming
    )

    # Extract the model’s answer from the response and return it
    interpretation = response.choices[0].message.content.strip()
    print(f"[LLM Response]\n{interpretation}")
    return interpretation
