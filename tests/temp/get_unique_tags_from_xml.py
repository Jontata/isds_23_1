from lxml import etree

def get_unique_tags(input_path, limit=100):
    # Set to store unique tags
    unique_tags = set()

    # Counter for the number of items processed
    count = 0

    # Parse the input XML file iteratively
    context = etree.iterparse(input_path, events=('start',))

    for event, elem in context:
        # Add the tag to the set
        unique_tags.add(elem.tag)

        # Clear the element to free up memory
        elem.clear()

        # Increment the counter
        count += 1

        # Break the loop after processing the desired number of items
        if count >= limit:
            break

        # Also eliminate now-empty references from the root node to elem
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    return unique_tags

# Path to the XML file
input_path = r"path"

# Retrieve and print the unique tags from the first 100 items
tags = get_unique_tags(input_path)
print("Unique tags in the first 100 items:")
for tag in tags:
    print(tag)