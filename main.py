import pygame, sys, os, random


class Card:
    def __init__(self, name, img):
        self.name = name
        self.img = img


class Pack:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    def printName(self):
        print(self.name)


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

# pack declarations
blankPack = pygame.image.load("./card_packs/BLANK_ICON.png")
blankPack = pygame.transform.scale(blankPack, (packSizeX, packSizeY))

charizardPack = pygame.image.load("./card_packs/charizard_pack.jpg")
charizardPack = pygame.transform.scale(charizardPack, (packSizeX, packSizeY))
charizardRect = charizardPack.get_rect()

blastoisePack = pygame.image.load("./card_packs/blastoise_pack.jpg")
blastoisePack = pygame.transform.scale(blastoisePack, (packSizeX, packSizeY))
blastoiseRect = blastoisePack.get_rect()

venusaurPack = pygame.image.load("./card_packs/venusaur_pack.jpg")
venusaurPack = pygame.transform.scale(venusaurPack, (packSizeX, packSizeY))
venusaurRect = venusaurPack.get_rect()

blankCard = pygame.transform.scale(blankPack, (cardSizeX, cardSizeY))
cardBack = pygame.image.load("./cardBacks/cardback.png")
cardBack = pygame.transform.scale(cardBack, (cardSizeX, cardSizeY))

cardBackHL = pygame.image.load("./cardBacks/cardbackHighlight.png")
cardBackHL = pygame.transform.scale(cardBackHL, (cardSizeX, cardSizeY))

background_image = pygame.image.load('./backgrounds/background.png')
woodenBackground = pygame.image.load('./backgrounds/woodenBackground.png')
woodenBackground = pygame.transform.scale(woodenBackground, (1024, 768))

# For Testing Purposes
charCard = pygame.image.load('./cardImages/smallCards/holo/holo(4).jpg')
charCard = pygame.transform.scale(charCard, (cardSizeX, cardSizeY))

font = pygame.font.Font('./fonts/PocketMonk-15ze.ttf', 50)
pygame.mixer.music.load("./sounds/soundtrack.mp3")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.25)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    while True:

        screen.fill((0, 0, 0))
        screen.blit(background_image, [0,0])
        draw_text('Main Menu', font, (255, 255, 255), screen, 20, 20)

        # check for mouse location
        mx, my = pygame.mouse.get_pos()

        # button definition
        button_1 = pygame.Rect(display_width * 0.4, display_height * 0.7, 200, 50)
        button_2 = pygame.Rect(display_width * 0.4, display_height * 0.8, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        # button rendering
        pygame.draw.rect(screen, (52, 61, 235), button_1)
        pygame.draw.rect(screen, (52, 61, 235), button_2)

        draw_text('Start', font, (255, 255, 0), screen, display_width * 0.44, display_height * 0.7)
        draw_text('Options', font, (255, 255, 0), screen, display_width * 0.42, display_height * 0.8)

        click = False

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


def game():
    currentPackImg = blankPack
    currentCards = []
    packsOpened = []
    valX = display_width
    valY = display_height
    cardLocations = []
    cardNumList = []
    packOpeningSound = pygame.mixer.Sound('./sounds/packOpen.wav')

    for x in range(11):
        currentCards.append(blankCard)

    for x in range(11):
        cardNumList.append(x)

    click = False

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(woodenBackground, [0, 0])

        draw_text('Pack Opening', font, (255, 255, 255), screen, 20, 20)
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
        if button_1.collidepoint((mx, my)):
            if click:
                currentPackImg = generate_pack()
                for x in range(11):
                    currentCards[x] = blankCard
                cardNumList = getCardNums()
                print(cardNumList)

        # Open Pack Button
        # if button_2.collidepoint((mx, my)):
        #    if click:
        #        for x in range(11):
        #            currentCards[x] = blankPack
        #            currentCards[x] = cardBack

        if packImgRect.collidepoint((mx, my)):
            if click:
                if currentPackImg != blankPack:
                    click = False
                    pygame.mixer.Sound.play(packOpeningSound)
                    currentPackImg = blankPack
                    pygame.time.delay(1000)
                    for x in range(11):
                        click = False
                        currentCards[x] = cardBack

        for x in range(11):
            if cardLocations[x].collidepoint((mx, my)):
                if currentCards[x] == cardBack:
                    currentCards[x] = cardBackHL

        for y in range(11):
            if currentCards[y] == cardBackHL:
                if not cardLocations[y].collidepoint((mx, my)):
                    currentCards[y] = cardBack

        for x in range(11):
            if cardLocations[x].collidepoint((mx, my)):
                if click:
                    if currentPackImg == blankPack:
                        newCard = getCard(cardNumList, x)
                        currentCards[x] = newCard

        # button rendering
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        # pygame.draw.rect(screen, (250, 0, 0), button_2)

        draw_text('New Pack', font, (255, 255, 0), screen, display_width * 0.05, display_height * 0.5)
        # draw_text('Open Pack', font, (255, 255, 0), screen, display_width * 0.05, display_height * 0.5)

        click = False

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


def getCard(cardList, x):
    num = cardList[x]

    if x < 8:
        if x < 7:
            if x < 5:
                print('common')
                card = pygame.image.load('./cardImages/smallCards/common/common(' + str(num) + ').jpg')
                card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
                return card

            else:
                print('energy')
                card = pygame.image.load('./cardImages/smallCards/energy/energy(' + str(num) + ').jpg')
                card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
                return card
        else:
            holoChance = random.randint(1, 4)
            if holoChance == 4:
                print('holo rare')
                card = pygame.image.load('./cardImages/smallCards/holo/holo(' + str(num) + ').jpg')
                card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
                return card

            else:
                print('rare')
                card = pygame.image.load('./cardImages/smallCards/rare/rare(' + str(num) + ').jpg')
                card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
                return card

    else:
        print('uncommon')
        card = pygame.image.load('./cardImages/smallCards/uncommon/uncommon(' + str(num) + ').jpg')
        card = pygame.transform.scale(card, (cardSizeX, cardSizeY))
        return card


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


def generate_pack():
    packArtNum = random.randint(0, 2)
    if packArtNum == 0:
        return charizardPack
    if packArtNum == 1:
        return blastoisePack
    if packArtNum == 2:
        return venusaurPack


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
