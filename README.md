v1.0.0

# Genimate: A tool to create Generative Animations
This script can be used to assemble generative animated images using weighted components,
and create the metadata in the format required by [MintGarden.io](mintgarden.io)'s
MintGarden Studio bulk minter. It makes use of [Gifski](https://gif.ski/) an amazing lossless GIF creation tool.

I've tried to make this as beginner friendly as possible.

This is an extension of my [NFT-Assembler-for-MintGarden-Bulk](https://github.com/andrewhstovell/Chia-NFT-Assembler-for-MintGarden-Bulk) example,
With the main difference being that this is intended to produce animated images.

#### Disclaimer:
* I am not affiliated with MintGarden.io
* This software is provided as is, for example purposes.


## Dependancies
- [Python 3](https://www.python.org/downloads/)
- [Pillow 9.x](https://pillow.readthedocs.io/en/stable/) run: `pip install Pillow`

## Running the Example
1. Clone the repository to your device, or [download the folder](https://github.com/andrewhstovell/Genimate/archive/refs/heads/main.zip) and extract the contents.
2. Navigate to the directory in your CLI (or `right-click + open terminal here` in the folder on Windows)
3. Type/paste `Done!" when done

![screenshot of steps 2 to 3]() TO DO

4. Check the newly created ***./collection/*** folder and contents that have been created. Remember to look at the metadata file.

> ***In the name of all that is good, please don't try to turn these example images into NFT's.***

## Usage
1. Create your own component PNG frames and place them in ***./components/TraitName/TraitVariation*** directory, and name them 1.png -> X.png in chronological order

For example: ./components/Feature/Blackhole/1.png

    *Your components can use any dimensions, as long as they are all the same.*

2. Edit the `genimate.py` file, set your collection's name, description and the amount of images to generate, the FPS and Frames per Animation configs
```
# Change these
COLLECTION_NAME = "Super Duper Animated Example Collection"
COLLECTION_DESCRIPTION = "Super Duper Animated Example NFT's"
TOTAL_IMAGES = 100 # Number of random unique images you want to generate
FRAMES_PER_ANIMATION = 3 # The number of frames that have been created for each trait variant
FPS = 5 # The speed of the Animation, the lower = slower
```
3. Replace the component names with the names of your TraitName directories
4. Adjust corresponding weights accordingly (lower = rarer)
```
# The weightings for each trait drive the rarity and add up to 100%
traits = [
    Trait(
        "Background", # Parent Folder
        ["Pink", "Teal", "Lime", "Cream"], # Sub Folder
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
```
* Run the program, and generate your Images and Metadata
* Run the program again until your batch of NFT's is just right!

## Testing
This is especially important if you have edited the code beyond what is presented in these instructions.

To double-check that every NFT has unique trait assignments in the metadata, 
run `python duplicate_identifier.py`

You should get 0 duplicates identified.

### Problems or need help?
Feel free to create an issue ticket, i will try to address as soon as possible

----
> *Want to toss some Mojo's or an NFT at the Andy?* <br/>
`xch1pelfpwqtnn0waj6vkrvdn7v8cx7h93gjmknakhq58hhrnlhqmk9s8xv64r`