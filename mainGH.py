#Pokemon Pack Opening Simulator - main.py
#By Matt Thibodeau 2020
#https://github.com/matt-thibodeau/Pokemon-Pack-Opening-Simulator

import pygame, sys, os, random


mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Pokémon Pack Opening Simulator')

display_width = 1024
display_height = 768

packSizeX = 300
packSizeY = 500

cardSizeX = 126
cardSizeY = 176

screen = pygame.display.set_mode((display_width, display_height), 0, 32)

black = (0, 0, 0)
white = (255, 255, 255)

# All File Declarations go here
blankPack = pygame.image.load("./card_packs/card_packs/BLANK_ICON.png")
blankPack = pygame.transform.scale(blankPack, (packSizeX, packSizeY))

charizardPack = pygame.image.load("./card_packs/card_packs/charizard_pack.jpg")
charizardPack = pygame.transform.scale(charizardPack, (packSizeX, packSizeY))
charizardRect = charizardPack.get_rect()

blastoisePack = pygame.image.load("./card_packs/card_packs/blastoise_pack.jpg")
blastoisePack = pygame.transform.scale(blastoisePack, (packSizeX, packSizeY))
blastoiseRect = blastoisePack.get_rect()

venusaurPack = pygame.image.load("./card_packs/card_packs/venusaur_pack.jpg")
venusaurPack = pygame.transform.scale(venusaurPack, (packSizeX, packSizeY))
venusaurRect = venusaurPack.get_rect()

blankCard = pygame.transform.scale(blankPack, (cardSizeX, cardSizeY))
cardBack = pygame.image.load("./cardBacks/cardBacks/cardback.png")
cardBack = pygame.transform.scale(cardBack, (cardSizeX, cardSizeY))

cardBackHL = pygame.image.load("./cardBacks/cardBacks/Highlight.png")
cardBackHL = pygame.transform.scale(cardBackHL, (cardSizeX, cardSizeY))

background_image = pygame.image.load('./backgrounds/backgrounds/background.png')
woodenBackground = pygame.image.load('./backgrounds/backgrounds/woodenBackground.png')
woodenBackground = pygame.transform.scale(woodenBackground, (1024, 768))

# charCard is a generic card For Testing Purposes
charCard = pygame.image.load('./cardImages/cardImages/smallCards/holo/holo(4).jpg')
charCard = pygame.transform.scale(charCard, (cardSizeX, cardSizeY))

# set the main font of the program - more fonts are available in fonts folder
font = pygame.font.Font('./fonts/fonts/PocketMonk-15ze.ttf', 50)

# Background music. I set it to be a little quieter so you could still hear the pack opening
pygame.mixer.music.load("./sounds/sounds/soundtrack.mp3")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.25)

# draw text function makes drawing text a bit easier
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# by default click should be false, otherwise we get weird issues
click = False

# This is the main menu window
def main_menu():
    while True:

        screen.fill((0, 0, 0))
        screen.blit(background_image, [0,0])
        draw_text('Main Menu', font, (255, 255, 255), screen, 20, 20)

        # check for mouse location
        mx, my = pygame.mouse.get_pos()

        # button definition
        startButton = pygame.Rect(display_width * 0.4, display_height * 0.7, 200, 50)
        optionsButton = pygame.Rect(display_width * 0.4, display_height * 0.8, 200, 50)

        # If you click the start button start the game
        if startButton.collidepoint((mx, my)):
            if click:
                game()

        # If you click the options button open the options menu
        if optionsButton.collidepoint((mx, my)):
            if click:
                options()

        # button rendering
        pygame.draw.rect(screen, (52, 61, 235), startButton)
        pygame.draw.rect(screen, (52, 61, 235), optionsButton)

        # Text for the buttons
        draw_text('Start', font, (255, 255, 0), screen, display_width * 0.44, display_height * 0.7)
        draw_text('Options', font, (255, 255, 0), screen, display_width * 0.42, display_height * 0.8)

        click = False

        # Basic event handling. ESC to exit, left-click = click
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


# This is the main game program where everything really happens
def game():

    # Default declarations - things I don't want changed every frame
    currentPackImg = blankPack
    currentCards = []
    packsOpened = []
    valX = display_width
    valY = display_height
    cardLocations = []
    cardNumList = []
    packOpeningSound = pygame.mixer.Sound('./sounds/sounds/packOpen.wav')

    # Set all cards in currentCards to blank cards
    for x in range(11):
        currentCards.append(blankCard)

    # Fill the card number list with numbers 1-11
    for x in range(11):
        cardNumList.append(x)

    click = False

    # Main game loop
    running = True
    while running:

        # Defining the background
        screen.fill((0, 0, 0))
        screen.blit(woodenBackground, [0, 0])
        draw_text('Pack Opening', font, (255, 255, 255), screen, 20, 20)

        # Defining the area where the pack goes, and getting it ready to be updated
        packImgRect = pygame.Rect(display_width * 0.4, display_height * 0.1, packSizeX, packSizeY)
        packImg = currentPackImg
        screen.blit(packImg, packImgRect)
        # pygame.draw.rect(screen, (0, 0, 255), packImgRect)

        # check for mouse location
        mx, my = pygame.mouse.get_pos()

        # button definition
        button_1 = pygame.Rect(display_width * 0.05, display_height * 0.5, 200, 50)
        button_2 = pygame.Rect(display_width * 0.05, display_height * 0.5, 200, 50)

        # setting card locations
        # Unfortunately this is hard-coded in, will need to be refactored at some point
        # but this will be an annoying undertaking
        for x in range(11):
            cardImgRect = pygame.Rect(valX * 0.3, valY * 0.12, cardSizeX, cardSizeY)
            cardLocations.append(cardImgRect)
            if x == 3:
                # pygame.draw.rect(screen, (0, 250, 0), cardLocations[x])
                valY = valY + 1700
                valX = valX - 2000
            if x == 7:
                # pygame.draw.rect(screen, (0, 250, 0), cardLocations[x])
                valY = valY + 1700
                valX = valX - 1250
            else:
                # pygame.draw.rect(screen, (0, 250, 0), cardLocations[x])
                valX = valX + 500

        # rendering the cards
        for x in range(11):
            screen.blit(currentCards[x], cardLocations[x])

        # New Pack Button
        # if mouse is over button1
        if button_1.collidepoint((mx, my)):
            # and it is clicked
            if click:
                # the current pack image becomes whatever the generate_pack() function spits out
                currentPackImg = generate_pack()
                # then we create the 11 cards that we will need and make them blank
                for x in range(11):
                    currentCards[x] = blankCard
                # finally we generate a card number list and store that for later
                cardNumList = getCardNums()
                print(cardNumList)

        # If you hover over the pack itself
        if packImgRect.collidepoint((mx, my)):
            # and click it
            if click:
                # and the current pack image is NOT blank
                if currentPackImg != blankPack:
                    # set the click value to false, play the pack opening sound
                    # set a delay (for the sound to finish) then change the cards
                    # from a blank image to the card back image
                    click = False
                    pygame.mixer.Sound.play(packOpeningSound)
                    currentPackImg = blankPack
                    pygame.time.delay(1000)

                    # the reason for the click=False is so that clicking the pack
                    # does not also click a card and ruin the opening
                    for x in range(11):
                        click = False
                        currentCards[x] = cardBack

        # This little guy makes sure that when you hover over a card
        # and the card back is displayed, the card back is highlighted
        # its a nice touch!
        for x in range(11):
            if cardLocations[x].collidepoint((mx, my)):
                if currentCards[x] == cardBack:
                    currentCards[x] = cardBackHL

        # This basically undoes the code from above. It makes it
        # so that the highlight goes away when you stop hovering
        # Otherwise everything would always be highlighted!
        for y in range(11):
            if currentCards[y] == cardBackHL:
                if not cardLocations[y].collidepoint((mx, my)):
                    currentCards[y] = cardBack

        # This is the real meat and potatoes of this code.
        # When you click a card, it calls the 'getCard()' function
        # using the card list from before. Then it stores all the
        # new cards into the currentCards array to display them
        for x in range(11):
            if cardLocations[x].collidepoint((mx, my)):
                if click:
                    if currentPackImg == blankPack:
                        newCard = getCard(cardNumList, x)
                        currentCards[x] = newCard

        # button rendering
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        # pygame.draw.rect(screen, (250, 0, 0), button_2)

        # Text for the button
        draw_text('New Pack', font, (255, 255, 0), screen, display_width * 0.05, display_height * 0.5)
        # draw_text('Open Pack', font, (255, 255, 0), screen, display_width * 0.05, display_height * 0.5)

        # I probably have this in here too many times but
        # its nice to make sure that its working
        click = False

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

# The infamous getCard function!
# It receives the list of numbers generated by the getCardNums function
# It then takes the x value (which is the card's numerical order) to determine
# what rarity it should be. Finally, it checks the image folder that correlates
# to the pre-determined rarity to figure out which pokemon card should be sent back!
def getCard(cardList, x):
    num = cardList[x]

    if x < 8:
        if x < 7:
            if x < 5:
                print('common')
                card = pygame.image.load('./cardImages/cardImages/smallCards/common/common(' + str(num) + ').jpg')
                card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
                return card

            else:
                print('energy')
                card = pygame.image.load('./cardImages/cardImages/smallCards/energy/energy(' + str(num) + ').jpg')
                card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
                return card
        else:
            # Worth noting. Holo Rares have a 1 in 4 chance of appearing
            holoChance = random.randint(1, 4)
            if holoChance == 4:
                print('holo rare')
                card = pygame.image.load('./cardImages/cardImages/smallCards/holo/holo(' + str(num) + ').jpg')
                card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
                return card

            else:
                print('rare')
                card = pygame.image.load('./cardImages/cardImages/smallCards/rare/rare(' + str(num) + ').jpg')
                card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
                return card

    else:
        print('uncommon')
        card = pygame.image.load('./cardImages/cardImages/smallCards/uncommon/uncommon(' + str(num) + ').jpg')
        card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
        return card

# The getCardNums function
# It creates a cardlist and runs through several iterations
# to make sure that all 11 slots are filled. It also tries
# its best to minimize duplicates wherever possible, but they
# do occasionally happen, however statistically unlikely.
# (Sometimes its kinda cool getting duplicates knowing
# how rare they are to get)
def getCardNums():
    def random_common():
        return random.randint(1, 32)

    def random_rare():
        return random.randint(1, 16)

    def random_energy():
        return random.randint(1, 6)

    def random_uncommon():
        return random.randint(1, 32)

    cardList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    cardList[0] = random_common()
    cardList[1] = random_common()
    cardList[2] = random_common()
    cardList[3] = random_common()
    cardList[4] = random_common()

    for i in range(5):
        for j in range(5):
            if cardList[i] == cardList[j]:
                cardList[i] = random_common()
    for i in range(5):
        for j in range(5):
            if cardList[i] == cardList[j]:
                cardList[i] = random_common()

    cardList[5] = random_energy()
    cardList[6] = random_energy()
    if cardList[6] == cardList[5]:
        cardList[6] = random_energy()
    if cardList[6] == cardList[5]:
        cardList[6] = random_energy()

    cardList[7] = random_rare()

    cardList[8] = random_uncommon()
    cardList[9] = random_uncommon()
    cardList[10] = random_uncommon()

    for i in range(3):
        for j in range(3):
            if cardList[i + 8] == cardList[j + 8]:
                cardList[i + 8] = random_uncommon()

    for i in range(3):
        for j in range(3):
            if cardList[i + 8] == cardList[j + 8]:
                cardList[i + 8] = random_uncommon()

    print(cardList)
    return cardList

# The generate_pack() function is simple
# Pick a number between 0 and 2 and spit out
# a pack based on the number
def generate_pack():
    packArtNum = random.randint(0, 2)
    if packArtNum == 0:
        return charizardPack
    if packArtNum == 1:
        return blastoisePack
    if packArtNum == 2:
        return venusaurPack

# options doesnt really do anything yet but here it is
def options():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('Options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


main_menu()
