from bs4 import BeautifulSoup
import json


# Read HTML from 'html.txt' file
with open('html.txt', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

result = {
    "name": "",
    "events": []
}

# Get character name
name_tag = soup.find(class_="eventhelper_viewer_top_label__9C9uv")
if name_tag:
    result["name"] = name_tag.get_text(strip=True).split('(')[0].strip()

# Find all event wrappers
for ew in soup.find_all(class_="eventhelper_ewrapper__A_RGO"):
    event_name = ew.find(class_="tooltips_ttable_heading__DK4_X")
    if not event_name:
        continue
    event = {
        "event": event_name.get_text(strip=True),
        "options": []
    }
    # Find all option cells
    grid = ew.find(class_="eventhelper_egrid__F3rTP")
    if grid:
        cells = grid.find_all(class_="eventhelper_ecell__B48KX")
        for i in range(0, len(cells), 2):
            if i+1 >= len(cells):
                break
            option_name = cells[i].get_text(strip=True)
            effects = [div.get_text(" ", strip=True) for div in cells[i+1].find_all("div", recursive=False)]
            if not effects:
                # Sometimes effects are direct text
                effects = [cells[i+1].get_text(" ", strip=True)]
            event["options"].append({
                "option": option_name,
                "effects": effects
            })
    result["events"].append(event)

# Output as JSON to a file with a custom name
output_filename = input('Enter output filename (e.g., output or output.json): ').strip()
if not output_filename:
    output_filename = 'output'
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f'Exported to {output_filename}')