from itinerary_generator import (
    create_prompt,
    generate_itinerary
)

attractions = [
    "India Gate",
    "Red Fort",
    "Qutub Minar"
]

prompt = create_prompt(
    budget=5000,
    days=2,
    interest="Historical",
    city="Delhi",
    attractions=attractions
)

print(prompt)

print()

print(generate_itinerary(prompt))