from PIL import Image
from shutil import rmtree
from os import path, mkdir, listdir, system
from dataclasses import dataclass
import sys
import csv
import random

## CONFIGURATION
# Change these
COLLECTION_NAME = "Super Duper Animated Example Collection"
COLLECTION_DESCRIPTION = "Super Duper Animated Example NFT's"
TOTAL_IMAGES = 100 # Number of random unique images you want to generate
FRAMES_PER_ANIMATION = 3 # The number of frames that have been created for each trait variant
FPS = 5 # The speed of the Animation, the lower = slower

# Should not need to change these
TEMP_DIR = './temp' # This directory will temporarily store the constructed frames for the animation
COLLECTION_DIR = './collection' # Output directory
COMPONENT_DIR = './components' # This is the directory where your Trait directories reside

all_images = [] # This is used to store the images as they are generated

# Each image is made up a series of traits
@dataclass
class Trait:
    name: str
    variants: list[str]
    weights: list[int]

# Make sure these Trait Types and Names match the directory structure of the traits. Case-Sensitive

# FOR EXAMPLE
# components/TraitType/Trait/x.png
# components/Background/Pink/x.png
# Where x is the frame number.

# The weightings for each trait drive the rarity and add up to 100%
# Note traits in this list must be in order of Layer. I.e., Background first, Foreground last.
traits = [
    Trait(
        "Background", 
        ["Pink", "Teal", "Lime", "Cream"], 
        [30, 20, 10, 40]),
    Trait(
        "Feature", 
        ["House", "Tree", "Sun", "Moon"], 
        [15, 35, 35, 15]),
    Trait(
        "Face", 
        ["Round", "Square", "Triangle"], 
        [30, 50, 20]),
    Trait(
        "Eyes", 
        ["Blue", "Red", "Brown"], 
        [30, 10, 60]),
    Trait(
        "Nose", 
        ["Pointy", "Rounded", "Dots"], 
        [30 , 30 , 40]),
    Trait(
        "Mouth", 
        ["Smile", "Grumpy", "Neutral", "Cute"], 
        [30, 30, 20, 20]),
]


## Generate Traits
# A recursive function to generate unique trait combinations (i.e., an image)
def create_new_image():
    new_image = {}
    
    # For each trait category, select a random trait based on the weightings
    for trait in traits:
        new_image[trait.name] = random.choices(trait.variants, trait.weights)[0]
    
    if (new_image in all_images):
        return create_new_image()
    else:
        return new_image



## Helper function for generating progress bars    
def progress_bar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#', print_end = "\r"):
    total = len(iterable)
    
    # Progress Bar Printing Function
    def print_progress_bar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = print_end)
        
    # Initial Call
    print_progress_bar(0)
    
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        print_progress_bar(i + 1)
    print()


# Generate the unique combinations based on trait weightings
for i in progress_bar(range(TOTAL_IMAGES), prefix = 'Combining Images:', suffix = 'Complete', length = 25):
    new_trait_image = create_new_image()
    all_images.append(new_trait_image)
    
    
    
## Check the stats of the new images
# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique? %s" % (all_images_unique(all_images)))

def make_empty_directory(dir : str):
    if path.isdir(dir):
        rmtree(dir)
    mkdir(dir)
    
make_empty_directory(COLLECTION_DIR)

def generate_frames_from_traits(image):
    for i in range(1, FRAMES_PER_ANIMATION + 1):
        layers = []

        # Load the components frames which will make up the image
        for trait in image:
            layers.append(Image.open(f'{COMPONENT_DIR}/{trait}/{image[trait]}/{i}.png').convert('RGBA'))

        # Merge the frames layers
        composite = Image.alpha_composite(layers[0], layers[1])
        for img_no in range(1, len(layers)):
            composite = Image.alpha_composite(composite, layers[img_no])

        # Convert to RGB & save the frame
        rgb_im = composite.convert('RGB')
        rgb_im.save(f'{TEMP_DIR}/{i}.png')
        
        
        
        
def create_lossless_gif(directory: str, gif_filename):
    """
    Create a lossless GIF using gifski from a directory containing PNG images.

    Args:
        directory: The directory containing the PNG images.
        gif_filename: The name of the output GIF file.

    Returns:
        None
    """
    # Get a list of the files in the directory, and filter for only PNG files
    files = [f for f in listdir(directory) if f.endswith('.png')]

    # Sort the list of files numerically
    files = sorted(files, key=lambda x: int(x.split('.')[0]))

    # Open the first file to determine the dimensions of the GIF
    first_file = f'{directory}/{files[0]}'
    with Image.open(first_file) as image:
        width, height = image.size

    # Build the command to run gifski - This command is generally less secure than

    gifski_command = f'gifski.exe --width {width} --height {height} --fps {FPS} --quality 100 --quiet --output=\"{COLLECTION_DIR}/{gif_filename}\" {directory}/*.png'
    
    # Run the gifski command
    result = system(gifski_command)



## Generate Animations and Metadata (metadata is suitable for MintGarden Studio bulk minter)
# Add the file, name and description for each image
for i in progress_bar(range(len(all_images)), prefix = 'Generating Animations and Metadata:', suffix = 'Complete', length = 25):
    name = "%s #%s" % (COLLECTION_NAME, str(i + 1))
    make_empty_directory(TEMP_DIR)
    generate_frames_from_traits(all_images[i])
    create_lossless_gif(TEMP_DIR, f'{name}.gif')
    
    # File metadata to suit MintGarden Bulk Generator
    # Feel free to change the values, do not change the keys.
    file_data = {
        "file": "%s.gif" % (str(i + 1)),                        
        "name": name,
        "description": "%s/%s %s" % (str(i + 1), str(TOTAL_IMAGES), COLLECTION_DESCRIPTION)  
    }
    file_data.update(all_images[i])
    all_images[i] = file_data
    
rmtree(TEMP_DIR)
    
# Create the metadata.csv file ready for the MintGarden Bulk minter
metadata_file = open(f'./{COLLECTION_DIR}/metadata.csv', 'w', newline='')
writer = csv.writer(metadata_file, delimiter =';')

# Write the metadata headers
writer.writerow(all_images[0].keys())

for item in progress_bar(all_images, prefix = 'Compiling Metadata:', suffix = 'Complete', length = 25):
    # Write the metadata for this item to metadata.csv
    writer.writerow(item.values())

metadata_file.close()

print("DONE!")