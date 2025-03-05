import os
import json

# Create templates directory if it doesn't exist
templates_dir = "templates"
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

# Template 1: Space Adventure
space_adventure = {
    "title": "Space Adventure",
    "template": "Captain [name] embarked on a journey to the [adjective] planet [planet_name]. The ship's [noun] malfunctioned as they [verb_past] through an asteroid field. \"[exclamation]!\" shouted the captain, \"We need to [verb] immediately!\" The alien crew members began to [verb] frantically. Eventually, they landed on a [adjective] moon where [plural_noun] roamed freely. It was the most [adjective] adventure in the history of space exploration.",
    "placeholders": ["name", "adjective", "planet_name", "noun", "verb_past", "exclamation", "verb", "verb", "adjective", "plural_noun", "adjective"]
}

# Template 2: Fairy Tale
fairy_tale = {
    "title": "Once Upon a Time",
    "template": "Once upon a time, in a [adjective] kingdom, there lived a [noun] named [name]. Every day, they would [verb] by the [adjective] [place]. One day, a [adjective] [magical_creature] appeared and granted them three [plural_noun]. \"[exclamation]!\" they shouted with joy. With their new [plural_noun], [name] decided to [verb] the evil [villain]. After a [adjective] battle, they lived [adverb] ever after.",
    "placeholders": ["adjective", "noun", "name", "verb", "adjective", "place", "adjective", "magical_creature", "plural_noun", "exclamation", "plural_noun", "name", "verb", "villain", "adjective", "adverb"]
}

# Template 3: Cooking Disaster
cooking_disaster = {
    "title": "Kitchen Catastrophe",
    "template": "Today I decided to cook a [adjective] meal for my [relative]. I started by [verb_ending_in_ing] [number] [plural_food] in a [adjective] pan. I accidentally added too much [substance], which made everything smell like [smelly_item]. \"[exclamation]!\" I shouted as the mixture began to [verb]. I tried to fix it by adding a [adjective] [food_item], but that only made it [verb]. In the end, we just ordered [type_of_cuisine] food and [verb_past] while watching [TV_show].",
    "placeholders": ["adjective", "relative", "verb_ending_in_ing", "number", "plural_food", "adjective", "substance", "smelly_item", "exclamation", "verb", "adjective", "food_item", "verb", "type_of_cuisine", "verb_past", "TV_show"]
}

# Template 4: Superhero Origin
superhero_origin = {
    "title": "Birth of a Hero",
    "template": "By day, [name] was just an ordinary [occupation], but at night, they became [superhero_name], the most [adjective] superhero in [city_name]! Their superpowers included [verb_ending_in_ing] [adverb] and shooting [plural_noun] from their [body_part]. Their arch-nemesis, [villain_name], was always plotting to [verb] the city's supply of [plural_noun]. With the help of their sidekick, [animal], [superhero_name] always saved the day by using their [adjective] [noun] to [verb] the day!",
    "placeholders": ["name", "occupation", "superhero_name", "adjective", "city_name", "verb_ending_in_ing", "adverb", "plural_noun", "body_part", "villain_name", "verb", "plural_noun", "animal", "superhero_name", "adjective", "noun", "verb"]
}

# Template 5: Vacation Gone Wrong
vacation_disaster = {
    "title": "Vacation Disaster",
    "template": "Last summer, my family decided to go on a [adjective] vacation to [place]. We packed our [plural_noun] and headed off in our [adjective] [vehicle]. After [number] hours of traveling, we realized we had forgotten our [important_item]! \"[exclamation]!\" my [family_member] screamed. We stopped at a [adjective] store to buy a new one, but they only had [adjective] ones. The hotel was even worse! The room was full of [plural_noun] and the [room_item] was [verb_ending_in_ing]. We ended up [verb_ending_in_ing] at a nearby [place] instead, which turned out to be the most [adjective] part of our trip.",
    "placeholders": ["adjective", "place", "plural_noun", "adjective", "vehicle", "number", "important_item", "exclamation", "family_member", "adjective", "adjective", "plural_noun", "room_item", "verb_ending_in_ing", "verb_ending_in_ing", "place", "adjective"]
}

# Save templates to files
templates = [
    ("space_adventure.json", space_adventure),
    ("fairy_tale.json", fairy_tale),
    ("cooking_disaster.json", cooking_disaster),
    ("superhero_origin.json", superhero_origin),
    ("vacation_disaster.json", vacation_disaster)
]

for filename, template in templates:
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, "w") as file:
        json.dump(template, file, indent=2)

print(f"Created 5 template files in the '{templates_dir}' directory:")
for filename, _ in templates:
    print(f"- {filename}") 